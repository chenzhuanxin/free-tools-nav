#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3U8 影视资源搜索下载器  ——  Python + HTML 单机工具
====================================================

设计：公歧子   微信：gongqizi0

功能：
  1. 聚合 10 个苹果CMS 采集接口，一次搜索全部资源站的 m3u8 资源
  2. 展示剧名 / 剧集 / 地区 / 年代 / 资源站 / m3u8 链接
  3. 内置下载器：多线程分片下载 + AES-128 解密 + 合并，可选 ffmpeg 无损转 MP4
  4. 导出结果为 Excel / CSV / JSON

运行：
  python m3u8tool.py               # 自动开浏览器
  python m3u8tool.py --port 8899   # 指定端口
  python m3u8tool.py --no-browser  # 不自动开浏览器（打包 exe 时常用）

打包 exe：
  pyinstaller --onefile --noconsole --name M3U8下载器 m3u8tool.py
"""

import os
import re
import sys
import json
import time
import html
import socket
import argparse
import threading
import webbrowser
import urllib.parse
import urllib.request
import urllib.error
import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# 同目录的下载引擎
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m3u8_engine as ENG   # noqa: E402

APP_NAME = "M3U8 影视资源搜索下载器"
APP_VER = "1.0.0"
AUTHOR = "公歧子"
WECHAT = "gongqizi0"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

# 资源接口清单（可被 sources.json 覆盖）
DEFAULT_SOURCES = [
    {"id": "guangsu",  "name": "光速资源",   "api": "https://api.guangsuapi.com/api.php/provide/vod/from/gsm3u8", "search": True},
    {"id": "liangzi",  "name": "量子资源",   "api": "https://cj.lziapi.com/api.php/provide/vod", "search": True},
    {"id": "hongniu",  "name": "红牛资源",   "api": "https://hongniuzy2.com/api.php/provide/vod/from/hnm3u8", "search": True},
    {"id": "s360",     "name": "360 资源",   "api": "https://360zyzz.com/api.php/provide/vod", "search": True},
    {"id": "zuida",    "name": "最大资源",   "api": "https://api.zuidapi.com/api.php/provide/vod", "search": True},
    {"id": "iqiyi",    "name": "爱奇艺资源", "api": "https://iqiyizyapi.com/api.php/provide/vod", "search": True},
    {"id": "jinying",  "name": "金鹰资源",   "api": "http://jyzyapi.com/provide/vod/from/jinyingm3u8", "search": True},
    {"id": "shandian", "name": "闪电资源",   "api": "http://sdzyapi.com/api.php/provide/vod/from/sdm3u8", "search": False},
    {"id": "tianya",   "name": "天涯影视",   "api": "https://tyyszyapi.com/api.php/provide/vod", "search": False},
    {"id": "wushui",   "name": "无水印资源", "api": "https://api.wsyzy.net/api.php/provide/vod/from/wsym3u8", "search": False},
]


# ============================================================ 基础工具

def base_dir():
    """可写目录（放配置 / 下载文件）：打包后用 EXE 所在目录，源码运行用脚本目录"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def res_dir():
    """只读资源目录（web/index.html 等）：PyInstaller 单文件解压到 _MEIPASS"""
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", base_dir())
    return base_dir()


def load_sources():
    """资源站清单：优先读用户可写目录（可自行修改），否则用打包内置的"""
    for p in (os.path.join(base_dir(), "sources.json"),        # 用户可写覆盖
              os.path.join(res_dir(), "sources.json")):        # 打包内置
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                srcs = data.get("sources") or []
                if srcs:
                    return srcs
            except Exception:
                pass
        if getattr(sys, "frozen", False) and p == os.path.join(base_dir(), "sources.json"):
            continue   # EXE 旁边没有就用内置的
    return list(DEFAULT_SOURCES)


def http_get(url, timeout=15, retries=2):
    """带重试的 GET（禁用系统代理，避免沙箱/公司代理干扰）"""
    last = None
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", UA)
            req.add_header("Accept", "*/*")
            op = urllib.request.build_opener(
                urllib.request.ProxyHandler({}),
                urllib.request.HTTPSHandler(context=_SSL_CTX))
            with op.open(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            last = e
            if i < retries:
                time.sleep(0.4 * (i + 1))
    raise last


def decode_text(raw):
    for enc in ("utf-8", "gbk", "gb18030", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "ignore")


# ============================================================ 苹果CMS 解析

def parse_vod_play_url(play_url):
    """解析 vod_play_url -> [{line: 线路名, episodes: [{name, url}]}]

    格式：线路1$$$线路2      线路之间用 $$$
          集名$URL#集名$URL  集之间用 #
    """
    lines = []
    if not play_url:
        return lines
    for raw_line in str(play_url).split("$$$"):
        eps = []
        for item in raw_line.split("#"):
            item = item.strip()
            if not item:
                continue
            if "$" in item:
                nm, u = item.split("$", 1)
            else:
                nm, u = "", item
            u = u.strip()
            if u and (".m3u8" in u.lower() or u.startswith("http")):
                eps.append({"name": nm.strip() or ("第%d集" % (len(eps) + 1)), "url": u})
        if eps:
            lines.append(eps)
    return lines


def parse_vod_item(it, src_name):
    """把一条采集记录转成前端要用的结构"""
    play_lines = parse_vod_play_url(it.get("vod_play_url"))
    lines = []
    for i, eps in enumerate(play_lines):
        lines.append({
            "line": play_lines and ("线路%d" % (i + 1)) or "",
            "episodes": eps,
        })
    return {
        "title": (it.get("vod_name") or "").strip(),
        "type": (it.get("type_name") or it.get("vod_class") or "").strip(),
        "area": (it.get("vod_area") or "").strip(),
        "year": (it.get("vod_year") or "").strip(),
        "remark": (it.get("vod_remarks") or "").strip(),
        "actor": (it.get("vod_actor") or "").strip(),
        "director": (it.get("vod_director") or "").strip(),
        "pic": (it.get("vod_pic") or "").strip(),
        "score": (it.get("vod_score") or "").strip(),
        "updated": (it.get("vod_time") or "").strip(),
        "source": src_name,
        "lines": lines,
        "ep_count": sum(len(l["episodes"]) for l in lines),
    }


def search_source(src, wd, timeout=15):
    """搜索单个资源站"""
    base = src["api"]
    qs = urllib.parse.urlencode({"ac": "detail", "wd": wd})
    url = base + ("&" if "?" in base else "?") + qs
    raw = http_get(url, timeout=timeout, retries=1)
    txt = decode_text(raw)
    # 有些接口在 JSONP 里包一层
    m = re.search(r"\{.*\}", txt, re.S)
    if not m:
        raise ValueError("接口未返回 JSON")
    data = json.loads(m.group(0))
    lst = data.get("list") or []
    return [parse_vod_item(it, src["name"]) for it in lst], data


# ============================================================ 任务管理

TASKS = {}
TASKS_LOCK = threading.Lock()
_TASK_SEQ = [0]


def new_task_id():
    with TASKS_LOCK:
        _TASK_SEQ[0] += 1
        return "t%d_%d" % (int(time.time()), _TASK_SEQ[0])


def start_download(name, m3u8_url, out_dir, opts):
    tid = new_task_id()
    referer = opts.get("referer") or m3u8_url
    headers = {"User-Agent": UA, "Referer": referer}
    task = ENG.DownloadTask(
        name=name, m3u8_url=m3u8_url, out_dir=out_dir, headers=headers,
        max_workers=int(opts.get("workers") or 16),
        use_ffmpeg=bool(opts.get("use_ffmpeg", True)),
        ffmpeg_path=opts.get("ffmpeg_path") or "",
        convert_mp4=bool(opts.get("convert_mp4", True)),
    )
    with TASKS_LOCK:
        TASKS[tid] = task
    threading.Thread(target=task.run, daemon=True).start()
    return tid


# ============================================================ HTTP 服务

MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}

OUT_DIR = [""]   # 可变，启动时写入


def parse_qs_u8(query):
    """按 UTF-8 解析查询串

    BaseHTTPRequestHandler 把 self.path 按 ISO-8859-1 解码，
    中文参数会变成乱码（转换测试 → è½¬æ¢è¯•）。
    先转回原始字节再按 UTF-8 解析即可。
    """
    if isinstance(query, str):
        query = query.encode("latin-1", "ignore")
    return urllib.parse.parse_qs(query.decode("utf-8", "ignore"), keep_blank_values=True)


class Handler(BaseHTTPRequestHandler):
    server_version = "M3U8Tool/" + APP_VER

    # ---------- 输出 ----------
    def _send(self, code, body, ctype="application/json; charset=utf-8", extra=None):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False))

    def log_message(self, fmt, *args):
        # 静音常规日志，只在出错时打印
        if args and str(args[0]).startswith("5"):
            sys.stderr.write("[HTTP] " + fmt % args + "\n")

    # ---------- GET ----------
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = parse_qs_u8(parsed.query)

        try:
            if path in ("/", "/index.html"):
                return self._page()
            if path == "/api/config":
                return self._api_config()
            if path == "/api/search":
                return self._api_search(qs)
            if path == "/api/parse":
                return self._api_parse(qs)
            if path == "/api/download":
                return self._api_download(qs)
            if path == "/api/progress":
                return self._api_progress(qs)
            if path == "/api/tasks":
                return self._api_tasks()
            if path == "/api/cancel":
                return self._api_cancel(qs)
            if path == "/api/remove":
                return self._api_remove(qs)
            if path == "/api/open":
                return self._api_open(qs)
            if path == "/api/ffmpeg":
                return self._api_ffmpeg()
            return self._send(404, "Not Found", "text/plain; charset=utf-8")
        except Exception as e:
            return self._json({"ok": False, "error": "%s: %s" % (type(e).__name__, e)}, 500)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/export":
            try:
                n = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(n).decode("utf-8") if n else "{}"
                return self._api_export(json.loads(body or "{}"))
            except Exception as e:
                return self._json({"ok": False, "error": str(e)}, 500)
        if parsed.path == "/api/ffmpeg_path":
            try:
                n = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(n).decode("utf-8") if n else "{}"
                d = json.loads(body or "{}")
                p = (d.get("path") or "").strip().strip('"')
                if p and os.path.isfile(p):
                    with open(_FFMPEG_CFG, "w", encoding="utf-8") as f:
                        json.dump({"path": p}, f)
                    return self._json({"ok": True, "path": p})
                return self._json({"ok": False, "error": "路径不存在：%s" % p})
            except Exception as e:
                return self._json({"ok": False, "error": str(e)}, 500)
        return self._send(404, "Not Found", "text/plain; charset=utf-8")

    # ---------- 页面 ----------
    def _page(self):
        return self._send(200, PAGE_HTML, "text/html; charset=utf-8")

    # ---------- API ----------
    def _api_config(self):
        return self._json({
            "ok": True,
            "app": APP_NAME, "version": APP_VER,
            "author": AUTHOR, "wechat": WECHAT,
            "sources": load_sources(),
            "out_dir": OUT_DIR[0],
            "aes_backend": ENG.aes_backend(),
            "ffmpeg": _ffmpeg_cfg_path(),
        })

    def _api_search(self, qs):
        wd = (qs.get("wd") or [""])[0].strip()
        if not wd:
            return self._json({"ok": False, "error": "请输入搜索关键词"})
        only = qs.get("sources")     # 逗号分隔的 id
        only_ids = set(x for x in (only[0].split(",") if only else []) if x)
        srcs = load_sources()
        if only_ids:
            srcs = [s for s in srcs if s["id"] in only_ids]

        results, errors = [], []
        lock = threading.Lock()

        def worker(s):
            if not s.get("search", True):
                with lock:
                    errors.append({"source": s["name"], "error": "该接口不支持关键词搜索"})
                return
            try:
                items, _ = search_source(s, wd)
                with lock:
                    results.extend(items)
            except Exception as e:
                with lock:
                    errors.append({"source": s["name"], "error": str(e)[:120]})

        ths = [threading.Thread(target=worker, args=(s,)) for s in srcs]
        for t in ths:
            t.start()
        for t in ths:
            t.join(timeout=25)

        # 排序：有资源的、集数多的、年份新的排前面
        def key(it):
            return (-(1 if it["ep_count"] else 0), -it["ep_count"], it["year"] or "0")
        results.sort(key=key)

        return self._json({
            "ok": True, "wd": wd, "count": len(results),
            "results": results, "errors": errors,
        })

    def _api_parse(self, qs):
        url = (qs.get("url") or [""])[0]
        if not url:
            return self._json({"ok": False, "error": "缺少 url"})
        try:
            info = ENG.fetch_playlist(url, headers={"User-Agent": UA, "Referer": url})
            return self._json({
                "ok": True,
                "kind": info.get("kind"),
                "count": len(info.get("segments") or []),
                "encrypted": bool(info.get("keys")),
                "duration": round(sum((s.get("dur") or 0) for s in info.get("segments") or []), 1),
                "chosen": info.get("chosen"),
            })
        except Exception as e:
            return self._json({"ok": False, "error": str(e)})

    def _api_download(self, qs):
        g = lambda k, d="": (qs.get(k) or [d])[0]
        url = g("url").strip()
        if not url:
            return self._json({"ok": False, "error": "缺少 url"})
        name = ENG.safe_filename(g("name") or "video")
        out = g("out") or OUT_DIR[0]
        try:
            os.makedirs(out, exist_ok=True)
        except Exception as e:
            return self._json({"ok": False, "error": "输出目录不可用：%s" % e})
        opts = {
            "workers": g("workers") or 16,
            "use_ffmpeg": g("ffmpeg", "1") not in ("0", "false", ""),
            "convert_mp4": g("mp4", "1") not in ("0", "false", ""),
            "ffmpeg_path": _ffmpeg_cfg_path(),
            "referer": g("referer"),
        }
        tid = start_download(name, url, out, opts)
        return self._json({"ok": True, "id": tid, "name": name, "out": out})

    def _api_progress(self, qs):
        tid = (qs.get("id") or [""])[0]
        with TASKS_LOCK:
            t = TASKS.get(tid)
        if not t:
            return self._json({"ok": False, "error": "任务不存在"})
        snap = t.snapshot()
        snap["ok"] = True
        snap["id"] = tid
        return self._json(snap)

    def _api_tasks(self):
        with TASKS_LOCK:
            items = []
            for tid, t in TASKS.items():
                s = t.snapshot()
                s["id"] = tid
                items.append(s)
        return self._json({"ok": True, "tasks": items})

    def _api_cancel(self, qs):
        tid = (qs.get("id") or [""])[0]
        with TASKS_LOCK:
            t = TASKS.get(tid)
        if not t:
            return self._json({"ok": False, "error": "任务不存在"})
        t.cancel()
        return self._json({"ok": True})

    def _api_remove(self, qs):
        tid = (qs.get("id") or [""])[0]
        with TASKS_LOCK:
            TASKS.pop(tid, None)
        return self._json({"ok": True})

    def _api_open(self, qs):
        tid = (qs.get("id") or [""])[0]
        with TASKS_LOCK:
            t = TASKS.get(tid)
        p = ""
        if t:
            p = t.snapshot().get("output") or ""
        if not p:
            p = (qs.get("path") or [""])[0]
        if p and os.path.isfile(p):
            try:
                os.startfile(p)          # Windows
            except Exception:
                import subprocess
                subprocess.Popen(["explorer", "/select,", p])
            return self._json({"ok": True})
        if OUT_DIR[0] and os.path.isdir(OUT_DIR[0]):
            try:
                os.startfile(OUT_DIR[0])
            except Exception:
                pass
            return self._json({"ok": True, "dir": OUT_DIR[0]})
        return self._json({"ok": False, "error": "文件不存在"})

    def _api_ffmpeg(self):
        return self._json({"ok": True, "path": _ffmpeg_cfg_path()})

    def _api_export(self, payload):
        """把搜索结果导出为 Excel / CSV / JSON，直接落盘到输出目录"""
        fmt = (payload.get("format") or "xlsx").lower()
        rows = payload.get("rows") or []
        wd = ENG.safe_filename(payload.get("wd") or "搜索结果", "search")
        stamp = time.strftime("%Y%m%d_%H%M%S")
        out = OUT_DIR[0]
        os.makedirs(out, exist_ok=True)

        if fmt == "json":
            path = os.path.join(out, "%s_%s.json" % (wd, stamp))
            with open(path, "w", encoding="utf-8") as f:
                json.dump(rows, f, ensure_ascii=False, indent=2)
        elif fmt == "csv":
            import csv
            path = os.path.join(out, "%s_%s.csv" % (wd, stamp))
            cols = ["序号", "标题", "类型", "地区", "年代", "集数", "资源站", "m3u8链接", "备注", "更新时间"]
            with open(path, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f)
                w.writerow(cols)
                for i, r in enumerate(rows, 1):
                    w.writerow([i, r.get("title", ""), r.get("type", ""), r.get("area", ""),
                                r.get("year", ""), r.get("ep_count", ""), r.get("source", ""),
                                r.get("m3u8", ""), r.get("remark", ""), r.get("updated", "")])
        else:
            path = os.path.join(out, "%s_%s.xlsx" % (wd, stamp))
            build_xlsx(path, rows)

        return self._json({"ok": True, "path": path, "file": os.path.basename(path)})


# ------------------------------------------------------------ 纯标准库写 xlsx

def build_xlsx(path, rows):
    """用 zipfile 手写最小可用 OOXML 工作簿（无需 openpyxl）

    技巧：全部单元格用 inlineStr，避免处理 sharedStrings。
    """
    import zipfile

    cols = ["序号", "标题", "类型", "地区", "年代", "集数", "资源站", "m3u8链接", "备注", "更新时间"]

    def esc(s):
        s = "" if s is None else str(s)
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return s.replace('"', "&quot;")

    def col_letter(n):
        s = ""
        while n > 0:
            n, r = divmod(n - 1, 26)
            s = chr(65 + r) + s
        return s

    out = []
    out.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
    out.append('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
    out.append('<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" '
               'activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>')
    out.append('<cols><col min="1" max="1" width="6"/><col min="2" max="2" width="34"/>'
               '<col min="3" max="3" width="12"/><col min="4" max="4" width="10"/>'
               '<col min="5" max="5" width="8"/><col min="6" max="6" width="8"/>'
               '<col min="7" max="7" width="14"/><col min="8" max="8" width="60"/>'
               '<col min="9" max="9" width="18"/><col min="10" max="10" width="20"/></cols>')
    out.append('<sheetData>')

    # 表头
    out.append('<row r="1">')
    for i, c in enumerate(cols, 1):
        ref = "%s1" % col_letter(i)
        out.append('<c r="%s" t="inlineStr" s="1"><is><t>%s</t></is></c>' % (ref, esc(c)))
    out.append('</row>')

    for ri, r in enumerate(rows, 2):
        vals = [ri - 1, r.get("title", ""), r.get("type", ""), r.get("area", ""),
                r.get("year", ""), r.get("ep_count", ""), r.get("source", ""),
                r.get("m3u8", ""), r.get("remark", ""), r.get("updated", "")]
        out.append('<row r="%d">' % ri)
        for i, v in enumerate(vals, 1):
            ref = "%s%d" % (col_letter(i), ri)
            out.append('<c r="%s" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>'
                       % (ref, esc(v)))
        out.append('</row>')
    out.append('</sheetData>')
    out.append('<autoFilter ref="A1:%s%d"/>' % (col_letter(len(cols)), max(len(rows) + 1, 1)))
    out.append('</worksheet>')
    sheet = "".join(out)

    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="2">'
        '<font><sz val="11"/><name val="微软雅黑"/></font>'
        '<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="微软雅黑"/></font>'
        '</fonts>'
        '<fills count="3">'
        '<fill><patternFill patternType="none"/></fill>'
        '<fill><patternFill patternType="gray125"/></fill>'
        '<fill><patternFill patternType="solid"><fgColor rgb="FF3D6DFF"/><bgColor indexed="64"/></patternFill></fill>'
        '</fills>'
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="2">'
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
        '<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>'
        '</cellXfs>'
        '<cellStyles count="1"><cellStyle name="常规" xfId="0" builtinId="0"/></cellStyles>'
        '</styleSheet>')

    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="搜索结果" sheetId="1" r:id="rId1"/></sheets></workbook>')

    wb_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        '</Relationships>')

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        '</Types>')

    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '</Relationships>')

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        z.writestr("xl/styles.xml", styles)
        z.writestr("xl/worksheets/sheet1.xml", sheet)
    return path


# ============================================================ ffmpeg 配置

_FFMPEG_CFG = ""


def _ffmpeg_cfg_path():
    """读取用户配置的 ffmpeg 路径（存在同目录 ffmpeg.json）；没有则自动查找"""
    global _FFMPEG_CFG
    p = ""
    if _FFMPEG_CFG:
        try:
            with open(_FFMPEG_CFG, "r", encoding="utf-8") as f:
                p = (json.load(f) or {}).get("path", "")
        except Exception:
            p = ""
    if p and os.path.isfile(p):
        return p
    # 未配置或配置失效 → 自动查找
    return ENG.find_ffmpeg("")


# 前端页面（构建时由 build_page 填充）
PAGE_HTML = ""


def build_page():
    """把 web/index.html 内联进来；若缺失则用内置兜底页"""
    global PAGE_HTML
    p = os.path.join(res_dir(), "web", "index.html")
    if os.path.isfile(p):
        with open(p, "r", encoding="utf-8") as f:
            PAGE_HTML = f.read()
    else:
        PAGE_HTML = ("<!doctype html><meta charset='utf-8'>"
                     "<h1>缺少 web/index.html</h1>"
                     "<p>请把 web 目录与程序放在同一目录。</p>")
    # 注入版本等信息
    PAGE_HTML = (PAGE_HTML
                 .replace("__APP_NAME__", html.escape(APP_NAME))
                 .replace("__APP_VER__", APP_VER)
                 .replace("__AUTHOR__", html.escape(AUTHOR))
                 .replace("__WECHAT__", html.escape(WECHAT)))


# ============================================================ 启动

def pick_port(prefer):
    for p in ([prefer] if prefer else []) + [8899, 9000, 9123, 9527, 18080]:
        if not p:
            continue
        try:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("127.0.0.1", p))
            s.close()
            return p
        except OSError:
            continue
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def main():
    global _FFMPEG_CFG
    ap = argparse.ArgumentParser(description=APP_NAME)
    ap.add_argument("--port", type=int, default=0, help="监听端口（默认自动）")
    ap.add_argument("--out", default="", help="下载目录（默认 程序目录/downloads）")
    ap.add_argument("--no-browser", action="store_true", help="不自动打开浏览器")
    args = ap.parse_args()

    bd = base_dir()
    _FFMPEG_CFG = os.path.join(bd, "ffmpeg.json")

    out = args.out or os.path.join(bd, "downloads")
    os.makedirs(out, exist_ok=True)
    OUT_DIR[0] = os.path.abspath(out)

    build_page()
    port = pick_port(args.port)
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    srv.daemon_threads = True
    url = "http://127.0.0.1:%d/" % port

    print("=" * 60)
    print("  %s  v%s" % (APP_NAME, APP_VER))
    print("=" * 60)
    print("  访问地址 : %s" % url)
    print("  下载目录 : %s" % OUT_DIR[0])
    print("  AES 后端 : %s" % ENG.aes_backend())
    ff = _ffmpeg_cfg_path()
    print("  ffmpeg   : %s" % (ff or "未找到（将保留 .ts，可用播放器直接打开）"))
    print("=" * 60)
    print("  按 Ctrl+C 停止服务")
    print()

    if not args.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")
    finally:
        srv.server_close()


if __name__ == "__main__":
    # 允许被 PyInstaller 打包后正常启动
    import multiprocessing
    multiprocessing.freeze_support()
    main()
