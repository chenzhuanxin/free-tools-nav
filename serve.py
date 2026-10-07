#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
免费工具集导航 - 本地服务
=========================================
作用：
  1. 以 HTTP 方式托管 index.html（避免 file:// 的 CORS 限制）
  2. 提供 /api/proxy 转发接口，用于「m3u8 聚合搜索」跨域访问各资源站采集接口

用法：
  双击本文件（或运行 python serve.py），浏览器会自动打开 http://127.0.0.1:8765/
  之后在网页里使用「全网 M3U8 资源聚合搜索」即可正常返回结果并导出 Excel。

依赖：仅 Python 标准库，无需安装任何第三方包。
"""
import http.server
import socketserver
import urllib.request
import urllib.parse
import urllib.error
import json
import os
import sys
import re
import io
import zipfile
import threading
import webbrowser
from xml.sax.saxutils import escape as xml_escape

PORT = 8765
HOST = "127.0.0.1"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 端口被占用时依次尝试的备选端口
FALLBACK_PORTS = [8766, 8899, 9123, 9527, 18080, 28888, 0]  # 0 = 由系统自动分配

# 允许转发的目标域名白名单（资源站接口 + 常见影视域名）
ALLOW_SUFFIX = (
    "api.php", "provide/vod", "zyapi", "lziapi", "guangsuapi",
    "zuidapi", "apiyhzy", "sdzyapi", "jyzyapi", "iqiyizyapi", "tyyszyapi",
    "hongniuzy", "360zyzz", "wolongzyw", "wujinapi", "wsyzy"
)


def is_allowed(url: str) -> bool:
    try:
        host = urllib.parse.urlparse(url).hostname or ""
    except Exception:
        return False
    if not host:
        return False
    low = url.lower()
    return any(s in low for s in ALLOW_SUFFIX)


def ascii_url(url: str) -> str:
    """把 URL 中的非 ASCII 字符（如中文搜索词）重新做百分号编码。

    urllib 在发送请求时会把整条 URL 用 ASCII 编码，直接塞中文会抛
    "'ascii' codec can't encode characters"。这里按结构拆分后逐段 quote，
    保留 :/?#[]@!$&'()*+,;= 这些 URL 结构字符，只编码其余部分。
    """
    try:
        parts = urllib.parse.urlsplit(url)
    except Exception:
        return url
    # path / query / fragment 分别做“非 ASCII 才编码”的处理，
    # 已有的 %XX 不会被二次编码（quote 的 safe 中包含 %）。
    safe = ":/?#[]@!$&'()*+,;=%"
    scheme = parts.scheme
    netloc = parts.netloc.encode("idna").decode("ascii") if parts.netloc else ""
    path = urllib.parse.quote(parts.path, safe=safe)
    query = urllib.parse.quote(parts.query, safe=safe)
    fragment = urllib.parse.quote(parts.fragment, safe=safe)
    return urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    """静态文件 + /api/proxy 转发"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    # ---------- CORS ----------
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/xlsx":
            self.handle_xlsx()
            return
        self.reply_json(404, {"error": "not found"})

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/proxy":
            self.handle_proxy(parsed)
            return

        # 默认首页
        if parsed.path in ("/", ""):
            self.path = "/index.html"
        elif parsed.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        return super().do_GET()

    # ---------- 标准 xlsx 导出 ----------
    def handle_xlsx(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            if length <= 0 or length > 32 * 1024 * 1024:
                self.reply_json(400, {"error": "bad body"})
                return
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
            heads = payload.get("heads") or []
            rows = payload.get("rows") or []
            filename = str(payload.get("filename") or "export")
            if not isinstance(heads, list) or not isinstance(rows, list) or not heads:
                self.reply_json(400, {"error": "invalid heads/rows"})
                return
            data = build_xlsx(heads, rows)
        except Exception as e:
            self.reply_json(500, {"error": "xlsx build failed", "detail": str(e)})
            return

        # 文件名放到响应头（RFC 5987，兼容中文）
        safe_name = re.sub(r'[\\/:*?"<>|\r\n]+', "_", filename)
        ascii_name = re.sub(r"[^A-Za-z0-9_.-]", "_", safe_name) + ".xlsx"
        quoted = urllib.parse.quote(safe_name + ".xlsx", safe="")
        self.send_response(200)
        self.send_header("Content-Type",
                         "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.send_header("Content-Disposition",
                         "attachment; filename=\"%s\"; filename*=UTF-8''%s" % (ascii_name, quoted))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # ---------- 转发逻辑 ----------
    def handle_proxy(self, parsed):
        qs = urllib.parse.parse_qs(parsed.query)
        target = (qs.get("url") or [""])[0]
        if not target:
            self.reply_json(400, {"error": "missing url param"})
            return
        target = urllib.parse.unquote(target)
        if not target.startswith("http"):
            self.reply_json(400, {"error": "invalid url"})
            return
        if not is_allowed(target):
            self.reply_json(403, {"error": "domain not in whitelist"})
            return

        # 关键：把中文搜索词等非 ASCII 字符重新百分号编码，保证 urllib 能发送
        safe_target = ascii_url(target)

        referer = target.split("/api.php")[0] + "/"
        req = urllib.request.Request(safe_target, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": ascii_url(referer),
        })
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read()
                ctype = resp.headers.get("Content-Type", "application/json; charset=utf-8")
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except urllib.error.HTTPError as e:
            body = e.read() if hasattr(e, "read") else b""
            self.reply_json(e.code, {"error": "upstream %d" % e.code,
                                     "body": body[:400].decode("utf-8", "ignore")})
        except Exception as e:
            self.reply_json(502, {"error": "proxy failed", "detail": str(e)})

    def reply_json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        msg = fmt % args
        if "/api/proxy" in msg:
            sys.stdout.write("  [代理] %s\n" % msg)
        else:
            sys.stdout.write("  [静态] %s\n" % msg)
        sys.stdout.flush()


class ThreadedServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


# ==========================================================
#  标准 XLSX 生成（纯标准库，无第三方依赖）
# ==========================================================
def col_letter(n: int) -> str:
    """1-based 列号 -> Excel 列字母（1->A, 27->AA）"""
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _is_num(v) -> bool:
    if isinstance(v, bool):
        return False
    if isinstance(v, (int, float)):
        return True
    if isinstance(v, str):
        t = v.strip()
        # 纯数字（含小数/负号）才当数值，避免把 "2024" 之类年份变成数字后丢前导零
        return bool(re.fullmatch(r"-?\d+(\.\d+)?", t))
    return False


def build_xlsx(heads, rows) -> bytes:
    """把表头 + 二维数据写成最小可用的 .xlsx 字节流。

    策略：所有单元格都用 inlineStr（内联字符串），不做共享字符串表，
    数字型单元格用 n 类型以便 Excel 直接当数值参与计算。
    """
    ncols = len(heads)

    def cell(ref, value, style=0):
        s = ' s="%d"' % style if style else ''
        if value is None:
            return '<c r="%s"%s/>' % (ref, s)
        if _is_num(value):
            return '<c r="%s"%s><v>%s</v></c>' % (ref, s, str(value).strip())
        txt = xml_escape(str(value))
        return ('<c r="%s"%s t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>'
                % (ref, s, txt))

    xml = []
    xml.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
    xml.append('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
    # 冻结首行 + 自动筛选
    xml.append('<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" '
               'activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>')
    xml.append('<sheetFormatPr defaultRowHeight="16"/>')
    # 列宽（首列窄，其余自适应一个适中宽度）
    xml.append('<cols>')
    for i in range(1, ncols + 1):
        w = 6 if i == 1 else (46 if i == 2 else 20)
        xml.append('<col min="%d" max="%d" width="%d" customWidth="1"/>' % (i, i, w))
    xml.append('</cols>')
    xml.append('<sheetData>')

    # 表头行（style=1：加粗白字蓝底）
    xml.append('<row r="1" ht="20" customHeight="1">')
    for i, h in enumerate(heads, 1):
        xml.append(cell('%s1' % col_letter(i), h, style=1))
    xml.append('</row>')

    # 数据行
    for ri, row in enumerate(rows, start=2):
        xml.append('<row r="%d">' % ri)
        for ci in range(1, ncols + 1):
            v = row[ci - 1] if ci - 1 < len(row) else ''
            xml.append(cell('%s%d' % (col_letter(ci), ri), v))
        xml.append('</row>')
    xml.append('</sheetData>')
    xml.append('<autoFilter ref="A1:%s%d"/>' % (col_letter(ncols), max(1, len(rows) + 1)))
    xml.append('</worksheet>')
    sheet_xml = "".join(xml)

    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="2">'
        '<font><sz val="11"/><name val="\u5fae\u8f6f\u96c5\u9ed1"/></font>'
        '<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="\u5fae\u8f6f\u96c5\u9ed1"/></font>'
        '</fonts>'
        '<fills count="3">'
        '<fill><patternFill patternType="none"/></fill>'
        '<fill><patternFill patternType="gray125"/></fill>'
        '<fill><patternFill patternType="solid"><fgColor rgb="FF4F7CFF"/><bgColor indexed="64"/></patternFill></fill>'
        '</fills>'
        '<borders count="2">'
        '<border><left/><right/><top/><bottom/><diagonal/></border>'
        '<border><left style="thin"><color rgb="FFCCCCCC"/></left>'
        '<right style="thin"><color rgb="FFCCCCCC"/></right>'
        '<top style="thin"><color rgb="FFCCCCCC"/></top>'
        '<bottom style="thin"><color rgb="FFCCCCCC"/></bottom><diagonal/></border>'
        '</borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="2">'
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
        '<xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">'
        '<alignment horizontal="center" vertical="center"/></xf>'
        '</cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        '</styleSheet>')

    wb_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets></workbook>')

    wb_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        '</Relationships>')

    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
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

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", wb_xml)
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        z.writestr("xl/styles.xml", styles_xml)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml)
    return buf.getvalue()


def main():
    os.chdir(BASE_DIR)

    httpd = None
    used_port = None
    for p in [PORT] + FALLBACK_PORTS:
        try:
            httpd = ThreadedServer((HOST, p), ProxyHandler)
            used_port = httpd.server_address[1]
            break
        except OSError:
            continue

    if httpd is None:
        print("\n[错误] 无法绑定任何可用端口，请检查系统防火墙或端口占用情况。\n")
        input("按回车键退出…")
        return

    url = "http://%s:%d/" % (HOST, used_port)
    print("=" * 62)
    print("  免费工具集导航 · 本地服务已启动")
    print("=" * 62)
    print("  网页地址 : %s" % url)
    print("  代理接口 : %sapi/proxy?url=xxx" % url)
    print("  数据目录 : %s" % BASE_DIR)
    print("-" * 62)
    print("  ★ 关闭本窗口即可停止服务")
    print("  ★ m3u8 聚合搜索需通过本服务打开网页才能正常工作")
    print("=" * 62)
    print()

    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止。")
        httpd.shutdown()


if __name__ == "__main__":
    main()
