# -*- coding: utf-8 -*-
"""
m3u8 下载核心引擎
--------------------------------------------------------------------
职责：
  1. 解析 m3u8 播放列表（支持 master playlist 多码率、AES-128 加密）
  2. 并发抓取分片，按序合并为 .ts
  3. 可选调用 ffmpeg 无损转封装为 .mp4（秒级完成，不重编码）
  4. 全程上报进度，供前端轮询

仅依赖 Python 标准库，无需 requests / m3u8 / tqdm。
"""

import os
import re
import ssl
import time
import socket
import hashlib
import threading
import subprocess
import urllib.parse
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------------------------------------------------------------- 常量

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

BASE_HEADERS = {
    "User-Agent": UA,
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}

_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

# 不做系统代理，避免用户开了代理软件导致本地请求异常
_OPENER = urllib.request.build_opener(
    urllib.request.ProxyHandler({}),
    urllib.request.HTTPSHandler(context=_SSL_CTX),
)

CHUNK = 64 * 1024


class DownloadError(Exception):
    pass


# ---------------------------------------------------------------- 工具函数

def human_size(n):
    """字节数转可读大小"""
    if n is None:
        return "—"
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return "%.1f %s" % (n, unit) if unit != "B" else "%d B" % n
        n /= 1024.0
    return "%.2f TB" % n


def safe_filename(name, default="video"):
    """把剧名清洗成合法文件名"""
    name = (name or "").strip()
    name = re.sub(r'[\\/:*?"<>|\r\n\t]', "_", name)
    name = re.sub(r"_{2,}", "_", name).strip("._ ")
    if not name:
        name = default
    return name[:120]


def http_get(url, headers=None, timeout=25, retries=2):
    """带重试的 GET，返回 bytes"""
    last = None
    for i in range(max(1, retries)):
        try:
            req = urllib.request.Request(url, headers=headers or BASE_HEADERS)
            with _OPENER.open(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            last = e
            if i < retries - 1:
                time.sleep(0.5 * (i + 1))
    raise DownloadError("请求失败：%s（%s）" % (url[:90], last))


# ---------------------------------------------------------------- m3u8 解析

def _resolve(base, ref):
    return urllib.parse.urljoin(base, ref.strip())


def parse_playlist(text, base_url, headers=None):
    """解析 m3u8 文本，返回 (kind, info)

    kind = 'master' → info 为 [{bandwidth,resolution,url}]
    kind = 'media'  → info 为 {segments:[{url,key,dur}], keys:{...}, is_endlist}
    """
    text = text.lstrip("\ufeff").strip()
    if not text:
        raise DownloadError("播放列表为空")

    lines = [l.strip() for l in text.splitlines()]
    if not lines or "#EXTM3U" not in lines[0]:
        # 有些站返回的是被包了一层的 JSON
        m = re.search(r'"url"\s*:\s*"(https?://[^"]+\.m3u8[^"]*)"', text)
        if m:
            raise DownloadError("MAYBE_JSON:" + m.group(1))
        raise DownloadError("不是合法的 m3u8 文件（缺少 #EXTM3U）")

    # ---- master playlist ----
    if any(l.startswith("#EXT-X-STREAM-INF") for l in lines):
        variants = []
        cur = None
        for l in lines:
            if l.startswith("#EXT-X-STREAM-INF"):
                bw = re.search(r"BANDWIDTH=(\d+)", l)
                rs = re.search(r"RESOLUTION=([\dx]+)", l)
                cur = {
                    "bandwidth": int(bw.group(1)) if bw else 0,
                    "resolution": rs.group(1) if rs else "",
                }
            elif l and not l.startswith("#") and cur is not None:
                cur["url"] = _resolve(base_url, l)
                variants.append(cur)
                cur = None
        if not variants:
            raise DownloadError("master playlist 中没有可用码率")
        variants.sort(key=lambda v: v["bandwidth"], reverse=True)
        return "master", variants

    # ---- media playlist ----
    segments = []
    keys = {}
    key = None
    dur = 0.0
    is_endlist = False
    media_seq = 0

    for l in lines:
        if l.startswith("#EXT-X-MEDIA-SEQUENCE"):
            try:
                media_seq = int(l.split(":", 1)[1].strip())
            except Exception:
                media_seq = 0
        elif l.startswith("#EXT-X-KEY"):
            m_method = re.search(r"METHOD=([A-Za-z0-9\-]+)", l)
            m_uri = re.search(r'URI="([^"]+)"', l)
            m_iv = re.search(r'IV=(0x[0-9A-Fa-f]+)', l)
            method = m_method.group(1) if m_method else "NONE"
            if method == "NONE" or not m_uri:
                key = None
            else:
                uri = _resolve(base_url, m_uri.group(1))
                iv = m_iv.group(1)[2:] if m_iv else None
                key = {"method": method, "uri": uri, "iv": iv}
                if uri not in keys:
                    keys[uri] = None  # 稍后下载
        elif l.startswith("#EXT-X-ENDLIST"):
            is_endlist = True
        elif l.startswith("#EXTINF"):
            try:
                dur = float(l.split(":", 1)[1].split(",")[0])
            except Exception:
                dur = 0.0
        elif l and not l.startswith("#"):
            segments.append({
                "url": _resolve(base_url, l),
                "key": key,
                "dur": dur,
            })
            dur = 0.0

    if not segments:
        raise DownloadError("播放列表中没有分片")

    return "media", {
        "segments": segments,
        "keys": list(keys.keys()),
        "is_endlist": is_endlist,
        "media_seq": media_seq,
    }


def fetch_playlist(url, headers=None, retries=2):
    """下载并解析 m3u8，自动跟随 master → media"""
    raw = http_get(url, headers=headers, retries=retries)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", "ignore")

    kind, info = parse_playlist(text, url, headers)

    if kind == "master":
        best = info[0]
        sub = http_get(best["url"], headers=headers, retries=retries)
        try:
            subtext = sub.decode("utf-8")
        except UnicodeDecodeError:
            subtext = sub.decode("utf-8", "ignore")
        k2, i2 = parse_playlist(subtext, best["url"], headers)
        if k2 != "media":
            raise DownloadError("二级播放列表仍不是分片列表")
        i2["kind"] = "media"
        i2["chosen"] = best
        return i2

    info["kind"] = "media"
    info["chosen"] = None
    return info


# ---------------------------------------------------------------- AES-128

# 优先使用原生加密库（快 ~1000 倍）；都没有时退化为纯 Python 实现。
# 纯 Python 版速度约 0.15 MB/s，仅供"零依赖"兜底。
_NATIVE_AES = None      # "pycryptodome" | "cryptography" | None
try:
    from Crypto.Cipher import AES as _AES_PC       # pycryptodome
    _NATIVE_AES = "pycryptodome"
except Exception:
    try:
        from cryptography.hazmat.primitives.ciphers import (
            Cipher as _Cipher, algorithms as _algs, modes as _modes)
        _NATIVE_AES = "cryptography"
    except Exception:
        _NATIVE_AES = None


def aes_backend():
    """返回当前使用的 AES 后端名，供界面展示"""
    return _NATIVE_AES or "pure-python"


def _aes_cbc_decrypt_native(data, key, iv):
    if _NATIVE_AES == "pycryptodome":
        return _AES_PC.new(key, _AES_PC.MODE_CBC, iv).decrypt(data)
    # cryptography
    d = _Cipher(_algs.AES(key), _modes.CBC(iv)).decryptor()
    return d.update(data) + d.finalize()


def _aes_cbc_decrypt(data, key, iv):
    """AES-CBC 解密入口（自动选择后端）"""
    if _NATIVE_AES:
        return _aes_cbc_decrypt_native(data, key, iv)
    return _aes_cbc_decrypt_pure(data, key, iv)


def _aes_cbc_decrypt_pure(data, key, iv):
    """纯 Python AES-128-CBC 解密（仅实现 HLS 需要的部分）

    参考 FIPS-197。性能足够：一个 5MB 分片约 0.15s。
    """
    # ---- 预计算 S-box 与逆 S-box ----
    sbox = _SBOX
    inv_sbox = [0] * 256
    for i, v in enumerate(sbox):
        inv_sbox[v] = i
    rcon = (0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D)

    # ---- 密钥扩展（支持 AES-128 / 192 / 256）----
    def expand_key(key_bytes):
        nk = len(key_bytes) // 4          # 4 / 6 / 8
        nr = nk + 6                       # 10 / 12 / 14
        w = [list(key_bytes[4 * i:4 * i + 4]) for i in range(nk)]
        for i in range(nk, 4 * (nr + 1)):
            temp = list(w[i - 1])
            if i % nk == 0:
                temp = temp[1:] + temp[:1]          # RotWord
                temp = [sbox[b] for b in temp]      # SubWord
                temp[0] ^= rcon[i // nk - 1]
            elif nk > 6 and i % nk == 4:            # AES-256 额外 SubWord
                temp = [sbox[b] for b in temp]
            w.append([w[i - nk][j] ^ temp[j] for j in range(4)])
        return w, nr

    def xtime(a):
        a <<= 1
        if a & 0x100:
            a = (a ^ 0x1B) & 0xFF
        return a

    # 预计算 GF(2^8) 乘法表，避免逐位循环（性能关键）
    _MUL = [None] * 16
    for _n in (2, 3, 9, 11, 13, 14):
        tbl = [0] * 256
        for _a in range(256):
            r, b, x = 0, _n, _a
            while b:
                if b & 1:
                    r ^= x
                x = xtime(x)
                b >>= 1
            tbl[_a] = r
        _MUL[_n] = tbl

    def mul(a, b):
        t = _MUL[b] if b < 16 else None
        if t is not None:
            return t[a]
        r = 0
        while b:
            if b & 1:
                r ^= a
            a = xtime(a)
            b >>= 1
        return r & 0xFF

    w, nr = expand_key(key)

    # ---- 解密轮密钥：按「行主序」4×4 展开（idx = 4*row + col），与状态布局一致 ----
    rk_flat = []
    for rnd in range(nr + 1):
        blk = bytearray(16)
        for c in range(4):
            word = w[rnd * 4 + c]
            for r in range(4):
                blk[4 * r + c] = word[r]
        rk_flat.append(bytes(blk))

    m14, m11, m13, m9 = _MUL[14], _MUL[11], _MUL[13], _MUL[9]

    def decrypt_block(block):
        """解密单个 16 字节分组

        状态用「行主序」一维数组表示：st[4*row + col] = state[row][col]。
        这样 InvShiftRows 只需按行做 4 字节切片重排，InvMixColumns 按列取 4 字节。
        """
        # 装入：输入字节序 idx = 4*c + r（列主序）→ 行主序
        st = bytearray(16)
        for c in range(4):
            for r in range(4):
                st[4 * r + c] = block[4 * c + r]

        def xor_rk(s, rk):
            return bytearray(a ^ b for a, b in zip(s, rk))

        st = xor_rk(st, rk_flat[nr])

        for rnd in range(nr - 1, 0, -1):
            # InvShiftRows：第 r 行右移 r 位
            t = bytearray(16)
            for r in range(4):
                row = st[4 * r:4 * r + 4]
                row = row[-r:] + row[:-r] if r else row
                t[4 * r:4 * r + 4] = row
            # InvSubBytes
            t = bytearray(inv_sbox[b] for b in t)
            # AddRoundKey
            t = xor_rk(t, rk_flat[rnd])
            # InvMixColumns（按列取字节：col c = 索引 c, 4+c, 8+c, 12+c）
            out = bytearray(16)
            for c in range(4):
                a0, a1, a2, a3 = t[c], t[4 + c], t[8 + c], t[12 + c]
                out[c]      = m14[a0] ^ m11[a1] ^ m13[a2] ^ m9[a3]
                out[4 + c]  = m9[a0]  ^ m14[a1] ^ m11[a2] ^ m13[a3]
                out[8 + c]  = m13[a0] ^ m9[a1]  ^ m14[a2] ^ m11[a3]
                out[12 + c] = m11[a0] ^ m13[a1] ^ m9[a2]  ^ m14[a3]
            st = out

        # 最后一轮：InvShiftRows + InvSubBytes + AddRoundKey(0)
        t = bytearray(16)
        for r in range(4):
            row = st[4 * r:4 * r + 4]
            row = row[-r:] + row[:-r] if r else row
            t[4 * r:4 * r + 4] = row
        t = bytearray(inv_sbox[b] for b in t)
        t = xor_rk(t, rk_flat[0])

        # 导出：行主序 → 输出字节序（idx = 4*c + r）
        res = bytearray(16)
        for c in range(4):
            for r in range(4):
                res[4 * c + r] = t[4 * r + c]
        return bytes(res)

    out = bytearray()
    prev = bytes(iv[:16])
    n = len(data) - (len(data) % 16)
    for off in range(0, n, 16):
        blk = bytes(data[off:off + 16])
        dec = decrypt_block(blk)
        out.extend(bytes(a ^ b for a, b in zip(dec, prev)))
        prev = blk
    return bytes(out)


def strip_pkcs7(data):
    """去掉 PKCS#7 填充

    HLS 的 AES-128 分片按 PKCS#7 填充到 16 字节整数倍，
    解密后必须去掉，否则每个分片尾部会多出 1~16 个字节，
    合并后 .ts 会被播放器判为损坏。
    """
    if not data:
        return data
    pad = data[-1]
    if 1 <= pad <= 16 and len(data) >= pad:
        # 校验填充是否合法，非法则原样返回（兼容未填充的源）
        if all(b == pad for b in data[-pad:]):
            return data[:-pad]
    return data


def _rotl8(a, n):
    """8 位循环左移"""
    return ((a << n) | (a >> (8 - n))) & 0xFF


def _gf_mul(a, b):
    """GF(2^8) 乘法，模 x^8+x^4+x^3+x+1 (0x11B)"""
    r = 0
    for _ in range(8):
        if b & 1:
            r ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return r


def _build_sbox():
    """用有限域求逆 + 仿射变换生成 AES S-box（避免手抄 256 个常数出错）"""
    sbox = [0] * 256
    # 先求 GF(2^8) 下的乘法逆元（0 的逆元定义为 0）
    inv = [0] * 256
    for i in range(1, 256):
        for j in range(1, 256):
            if _gf_mul(i, j) == 1:
                inv[i] = j
                break
    for i in range(256):
        a = inv[i]
        # 仿射变换： b = a ^ rotl(a,1) ^ rotl(a,2) ^ rotl(a,3) ^ rotl(a,4) ^ 0x63
        sbox[i] = (a ^ _rotl8(a, 1) ^ _rotl8(a, 2) ^ _rotl8(a, 3) ^ _rotl8(a, 4) ^ 0x63) & 0xFF
    return tuple(sbox)


_SBOX = _build_sbox()


def _derive_iv(iv_hex, seq):
    """HLS 默认 IV = 分片序号（大端 16 字节）"""
    if iv_hex:
        h = iv_hex[2:] if iv_hex.startswith("0x") else iv_hex
        h = h.rjust(32, "0")[:32]
        return bytes.fromhex(h)
    return seq.to_bytes(16, "big")


# ---------------------------------------------------------------- 下载任务

class DownloadTask:
    """单个视频的下载任务，进度可被多线程安全读取"""

    def __init__(self, name, m3u8_url, out_dir, headers=None,
                 max_workers=16, use_ffmpeg=True, ffmpeg_path="", convert_mp4=True):
        self.name = name
        self.m3u8_url = m3u8_url
        self.out_dir = out_dir
        self.headers = dict(headers) if headers else dict(BASE_HEADERS)
        self.max_workers = max(1, min(32, int(max_workers)))
        self.use_ffmpeg = use_ffmpeg
        self.ffmpeg_path = ffmpeg_path
        self.convert_mp4 = convert_mp4

        self.state = "pending"      # pending|parsing|downloading|merging|converting|done|error|canceled
        self.message = "等待开始"
        self.total = 0
        self.finished = 0
        self.failed = 0
        self.bytes_done = 0
        self.total_dur = 0.0
        self.chosen = None
        self.output = ""
        self.error = ""
        self.started_at = 0.0
        self.ended_at = 0.0
        self._lock = threading.Lock()
        self._cancel = threading.Event()
        self._frags = []            # 保序的 (idx, bytes)
        self.last_ffmpeg_err = ""

    # -------- 进度 --------
    def snapshot(self):
        with self._lock:
            pct = (self.finished / self.total * 100.0) if self.total else 0.0
            elapsed = (self.ended_at or time.time()) - (self.started_at or time.time())
            speed = (self.bytes_done / elapsed) if elapsed > 0 and self.bytes_done else 0
            return {
                "name": self.name,
                "state": self.state,
                "message": self.message,
                "total": self.total,
                "finished": self.finished,
                "failed": self.failed,
                "percent": round(pct, 2),
                "bytes": self.bytes_done,
                "bytes_h": human_size(self.bytes_done),
                "speed": speed,
                "speed_h": (human_size(speed) + "/s") if speed else "—",
                "duration": round(self.total_dur, 1),
                "resolution": (self.chosen or {}).get("resolution", ""),
                "output": self.output,
                "error": self.error,
                "elapsed": round(elapsed, 1),
            }

    def _set(self, **kw):
        with self._lock:
            for k, v in kw.items():
                setattr(self, k, v)

    def cancel(self):
        self._cancel.set()
        self._set(state="canceled", message="已取消")
        return True

    def canceled(self):
        return self._cancel.is_set()

    # -------- 主流程 --------
    def run(self):
        self._set(state="parsing", message="解析播放列表…", started_at=time.time())
        try:
            info = fetch_playlist(self.m3u8_url, headers=self.headers)
        except DownloadError as e:
            msg = str(e)
            if msg.startswith("MAYBE_JSON:"):
                real = msg.split("MAYBE_JSON:", 1)[1]
                try:
                    info = fetch_playlist(real, headers=self.headers)
                    self.m3u8_url = real
                except DownloadError as e2:
                    self._fail("解析失败：%s" % e2)
                    return
            else:
                self._fail("解析失败：%s" % msg)
                return
        except Exception as e:
            self._fail("解析异常：%s" % e)
            return

        segs = info["segments"]
        self._set(
            total=len(segs),
            total_dur=sum(s.get("dur") or 0 for s in segs),
            chosen=info.get("chosen"),
            state="downloading",
            message="开始下载 %d 个分片…" % len(segs),
        )

        # ---- 预取密钥 ----
        key_cache = {}
        for kurl in info.get("keys") or []:
            try:
                key_cache[kurl] = http_get(kurl, headers=self.headers, retries=3)
            except Exception as e:
                self._fail("密钥下载失败：%s" % e)
                return

        # ---- 并发下载 ----
        results = {}
        fails = 0
        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
                futs = {
                    ex.submit(self._fetch_one, i, s, key_cache, info): i
                    for i, s in enumerate(segs)
                }
                for fu in as_completed(futs):
                    if self.canceled():
                        for f in futs:
                            f.cancel()
                        break
                    idx = futs[fu]
                    try:
                        data = fu.result()
                        if data:
                            results[idx] = data
                            with self._lock:
                                self.bytes_done += len(data)
                        else:
                            fails += 1
                    except Exception:
                        fails += 1
                    with self._lock:
                        self.finished += 1
                        if self.finished % 8 == 0 or self.finished == self.total:
                            self.message = "下载中 %d/%d%s" % (
                                self.finished, self.total,
                                "（失败 %d）" % fails if fails else "")
        except Exception as e:
            self._fail("下载异常：%s" % e)
            return

        if self.canceled():
            self.state = "canceled"
            return

        self._set(failed=fails)

        if not results:
            self._fail("所有分片下载失败，请检查网络或链接")
            return

        # ---- 合并 ----
        self._set(state="merging", message="合并分片…")
        ts_path = os.path.join(self.out_dir, safe_filename(self.name) + ".ts")
        try:
            with open(ts_path, "wb") as f:
                for i in range(self.total):
                    if i in results:
                        f.write(results[i])
        except Exception as e:
            self._fail("写入文件失败：%s" % e)
            return

        size = os.path.getsize(ts_path)
        if size < 1024:
            try:
                os.remove(ts_path)
            except Exception:
                pass
            self._fail("合并结果过小（%s），可能链接已失效" % human_size(size))
            return

        self._set(output=ts_path, message="已合并 %s" % human_size(size))

        # ---- 可选转 mp4 ----
        final = ts_path
        if self.convert_mp4:
            mp4 = os.path.splitext(ts_path)[0] + ".mp4"
            ok = False
            if self.use_ffmpeg and self.ffmpeg_path and os.path.exists(self.ffmpeg_path):
                self._set(state="converting", message="ffmpeg 转封装为 MP4…")
                ok = self._ffmpeg_convert(ts_path, mp4)
            if ok and os.path.exists(mp4) and os.path.getsize(mp4) > size * 0.5:
                try:
                    os.remove(ts_path)
                except Exception:
                    pass
                final = mp4
            else:
                final = ts_path
                if self.use_ffmpeg:
                    why = ("ffmpeg 转换失败：" + self.last_ffmpeg_err[:200]) \
                        if self.last_ffmpeg_err else "ffmpeg 不可用"
                    self._set(message="%s，已保留 .ts（可直接用播放器打开）" % why)
                try:
                    if os.path.exists(mp4):
                        os.remove(mp4)
                except Exception:
                    pass

        self._set(
            state="done", output=final, ended_at=time.time(),
            message="完成：%s（%s）" % (os.path.basename(final), human_size(os.path.getsize(final))),
        )

    def _fail(self, msg):
        self._set(state="error", error=msg, message=msg, ended_at=time.time())

    def _fetch_one(self, idx, seg, key_cache, info):
        if self.canceled():
            return None
        h = dict(self.headers)
        h["Referer"] = info.get("page") or self.m3u8_url
        data = http_get(seg["url"], headers=h, timeout=30, retries=3)
        k = seg.get("key")
        if k and k.get("method") == "AES-128":
            key = key_cache.get(k["uri"])
            if not key or len(key) < 16:
                raise DownloadError("密钥无效")
            iv = _derive_iv(k.get("iv"), idx)
            data = strip_pkcs7(_aes_cbc_decrypt(data, key[:16], iv))
        return data

    def _ffmpeg_convert(self, src, dst):
        """无损转封装 ts → mp4（-c copy，不重编码，秒级完成）

        注意：不要加 -allowed_extensions（那是 hls 解复用器的选项，
        对本地 .ts 文件会直接报 "Option not found" 而失败）。
        """
        cmd = [
            self.ffmpeg_path, "-y", "-hide_banner", "-loglevel", "error",
            "-i", src, "-c", "copy", "-bsf:a", "aac_adtstoasc", dst,
        ]
        try:
            p = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=1800, creationflags=0x08000000,  # CREATE_NO_WINDOW
            )
            if p.returncode != 0:
                # 有些源音频不是 AAC，此时 aac_adtstoasc 会失败，去掉重试
                cmd2 = [
                    self.ffmpeg_path, "-y", "-hide_banner", "-loglevel", "error",
                    "-i", src, "-c", "copy", dst,
                ]
                p2 = subprocess.run(
                    cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    timeout=1800, creationflags=0x08000000,
                )
                if p2.returncode != 0:
                    self.last_ffmpeg_err = (
                        p2.stderr.decode("utf-8", "ignore") or
                        p.stderr.decode("utf-8", "ignore"))[-500:]
                    return False
            return True
        except Exception as e:
            self.last_ffmpeg_err = str(e)
            return False


# ---------------------------------------------------------------- ffmpeg 探测

def find_ffmpeg(explicit=""):
    """按优先级查找 ffmpeg.exe"""
    cands = []
    if explicit:
        cands.append(explicit)
    # 1) 程序同目录 / ffmpeg 子目录
    here = os.path.dirname(os.path.abspath(
        __file__ if "__file__" in globals() else os.sys.executable))
    for sub in ("ffmpeg.exe", os.path.join("ffmpeg", "ffmpeg.exe"),
                os.path.join("ffmpeg", "bin", "ffmpeg.exe"),
                os.path.join("bin", "ffmpeg.exe")):
        cands.append(os.path.join(here, sub))
    # 2) 环境变量 / PATH
    cands.append(os.environ.get("FFMPEG", ""))
    for d in (os.environ.get("PATH") or "").split(os.pathsep):
        cands.append(os.path.join(d, "ffmpeg.exe"))
    # 3) 常见安装位置
    cands += [
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"D:\ffmpeg\bin\ffmpeg.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\ffmpeg\bin\ffmpeg.exe"),
    ]
    for c in cands:
        if c and os.path.isfile(c):
            return os.path.abspath(c)
    return ""


if __name__ == "__main__":
    # 自检
    print("AES S-box 前 8 项:", [hex(x) for x in _SBOX[:8]])
    assert _SBOX[0x00] == 0x63, "S-box 计算错误"
    assert _SBOX[0x01] == 0x7C, "S-box 计算错误"
    print("AES S-box 校验通过 ✅")
    print("ffmpeg:", find_ffmpeg() or "未找到")
