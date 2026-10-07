# -*- coding: utf-8 -*-
"""测试用 HLS 源生成器：起一个本地 HTTP 服务，提供 AES-128 加密的 m3u8

被 test_api.py / test_e2e.py 复用。
"""
import io
import os
import ssl
import sys
import json
import shutil
import hashlib
import threading
import http.server
import socketserver

DIR = os.path.join(os.environ.get("TEMP", "/tmp"), "m3u8tool_fixture")
KEY = bytes.fromhex("000102030405060708090A0B0C0D0E0F")
SEGS = 6
SEG_SIZE = 64 * 1024


def _encrypt_cbc(data, key, iv):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(data, 16))


def build():
    """生成测试文件，返回 (目录, meta)"""
    shutil.rmtree(DIR, ignore_errors=True)
    os.makedirs(DIR, exist_ok=True)

    plain = {}
    for i in range(SEGS):
        body = ("SEGMENT-%03d-" % i).encode() * (SEG_SIZE // 12 + 2)
        plain[i] = body[:SEG_SIZE]

    with open(os.path.join(DIR, "key.bin"), "wb") as f:
        f.write(KEY)

    for i in range(SEGS):
        ct = _encrypt_cbc(plain[i], KEY, i.to_bytes(16, "big"))
        with open(os.path.join(DIR, "seg%d.ts" % i), "wb") as f:
            f.write(ct)

    lines = ["#EXTM3U", "#EXT-X-VERSION:3", "#EXT-X-TARGETDURATION:10",
             "#EXT-X-MEDIA-SEQUENCE:0",
             '#EXT-X-KEY:METHOD=AES-128,URI="key.bin"']
    for i in range(SEGS):
        lines += ["#EXTINF:10.0,", "seg%d.ts" % i]
    lines.append("#EXT-X-ENDLIST")
    with open(os.path.join(DIR, "index.m3u8"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    with open(os.path.join(DIR, "master.m3u8"), "w", encoding="utf-8") as f:
        f.write("\n".join([
            "#EXTM3U",
            "#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x360", "index.m3u8",
            "#EXT-X-STREAM-INF:BANDWIDTH=2000000,RESOLUTION=1280x720", "index.m3u8",
        ]))

    meta = {"seg_size": SEG_SIZE, "segs": SEGS,
            "sha": {str(i): hashlib.sha256(plain[i]).hexdigest() for i in range(SEGS)}}
    return DIR, meta


class _H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=DIR, **kw)

    def log_message(self, *a):
        pass


def make_fixture_server():
    """构建测试源并启动服务，返回 (server, master_m3u8_url)"""
    build()
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), _H)
    srv.daemon_threads = True
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, "http://127.0.0.1:%d/master.m3u8" % port


if __name__ == "__main__":
    d, m = build()
    print("fixture:", d)
    print("segs=%d seg_size=%d" % (m["segs"], m["seg_size"]))
