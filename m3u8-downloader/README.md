# 🎞️ M3U8 影视资源搜索下载器

> 一键搜索全网影视资源站的 m3u8 地址，多线程下载 + AES-128 自动解密 + 无损转 MP4。
> **Python + HTML 单机工具，零配置开箱即用。**

当前版本 **v1.0.1**　设计：**公歧子**　微信：**gongqizi0**

📥 **[下载 M3U8下载器.exe](https://github.com/chenzhuanxin/free-tools-nav/releases/latest)**（约 17 MB，免安装）
📖 **[EXE 使用说明](EXE使用说明.md)** — 面向不熟悉命令行的用户，含截图级界面讲解与全部常见问题

---

## ✨ 功能

| 功能 | 说明 |
|------|------|
| 🔍 **全网聚合搜索** | 一次并发查询 7 个可搜索资源站（光速 / 量子 / 红牛 / 360 / 最大 / 爱奇艺 / 金鹰），另附 3 个浏览型接口 |
| 📋 **结果表格** | 剧名 / 类型 / 地区 / 年代 / 集数 / 资源站 / m3u8 链接，支持展开每条资源的全部剧集 |
| 🧪 **一键检测** | 下载前先解析 m3u8：分片数、时长、是否 AES 加密、画质 |
| ⬇️ **多线程下载** | 16 并发（可调 1-64），实测 43 分钟剧集 47 秒下完（约 7 MB/s） |
| 🔐 **AES-128 解密** | 内置解密链：优先 pycryptodome（≈400 MB/s），无依赖时自动退回纯 Python 实现 |
| 🎬 **无损转 MP4** | 自动探测 ffmpeg，`-c copy` 转封装秒级完成；没有 ffmpeg 保留 .ts（播放器可直接打开） |
| 📊 **导出** | 搜索结果一键导出 Excel（.xlsx）/ CSV / JSON |
| 🌐 **中文无乱码** | 服务端强制 UTF-8 解析请求，任务名 / 文件名中文完全正常 |

## 🚀 三种使用方式

### 方式一：直接双击 EXE（推荐给普通用户）

1. 到 [Releases](https://github.com/chenzhuanxin/free-tools-nav/releases/latest) 下载 `M3U8下载器.exe`
2. 双击运行 → 浏览器自动打开 `http://127.0.0.1:端口/`
3. 搜剧 → 点剧集 → 等进度条走完 → 打开文件

> 首次运行若被 SmartScreen 拦（未签名小工具的常见提示），点「更多信息 → 仍要运行」。
> **详细图文步骤、常见问题排查见 [EXE 使用说明](EXE使用说明.md)。**

> 想要 MP4：把 `ffmpeg.exe` 所在目录放到程序同目录，或在页面「下载设置」里填路径保存。
> 没有 ffmpeg 也能用：产物为 .ts 格式，PotPlayer / VLC 可直接播放。

### 方式二：运行 Python 源码

```bash
pip install pycryptodome        # 可选，AES 解密提速约 1000 倍
python m3u8tool.py              # 自动开浏览器
python m3u8tool.py --port 8899 --out D:/视频
```

参数：

| 参数 | 说明 |
|------|------|
| `--port N` | 指定端口（默认自动挑选 8899/9000/9123/9527/18080 或随机空闲端口） |
| `--out DIR` | 下载目录（默认 `程序目录/downloads`） |
| `--no-browser` | 启动后不自动打开浏览器 |

### 方式三：自己打包 EXE

```bash
pip install pyinstaller pycryptodome
C:\Python314\python.exe -m PyInstaller --workpath D:/pysbuild/build --distpath D:/pysbuild/dist m3u8tool.spec
# 产物：D:/pysbuild/dist/M3U8下载器.exe
```

## 📡 内置 HTTP 接口（可二次开发）

| 接口 | 说明 |
|------|------|
| `GET /api/config` | 程序信息、资源站清单、ffmpeg 探测结果 |
| `GET /api/search?wd=剧名` | 聚合搜索，`&sources=id1,id2` 可筛选 |
| `GET /api/parse?url=m3u8` | 解析播放列表（分片数 / 时长 / 是否加密） |
| `GET /api/download?name=&url=` | 启动下载任务，支持 workers / ffmpeg / mp4 参数 |
| `GET /api/progress?id=` | 单任务进度 |
| `GET /api/tasks` | 全部任务 |
| `GET /api/cancel?id=` | 取消任务 |
| `GET /api/remove?id=` | 从列表移除任务 |
| `GET /api/open?id=` | 打开下载的文件 / 下载目录 |
| `POST /api/export` | `{format: xlsx\|csv\|json, wd, rows}` 落盘导出 |
| `POST /api/ffmpeg_path` | 保存自定义 ffmpeg 路径到 `ffmpeg.json` |

## 🗒 更新日志

### v1.0.1
- 🐛 **修复中文乱码**：`BaseHTTPRequestHandler` 默认按 latin-1 解析请求路径，导致任务名 / 文件名出现「è½¬æ¢è¯•」这类乱码。新增 `parse_qs_u8()` 先还原字节再按 UTF-8 解析。
- 🐛 **修复 ffmpeg 自动探测**：下载接口原先只读 `ffmpeg.json`，未配置时拿到空路径导致不转 MP4。现改为「用户配置 → 自动探测」两级回退。
- 🐛 **修复打包后页面 404**：单文件 EXE 的资源被解压到 `sys._MEIPASS`，而配置/下载目录应在 EXE 旁。拆分为 `res_dir()`（只读资源）与 `base_dir()`（可写目录）。
- 🐛 **修复 xlsx 校验告警**：补 `cellStyles` 元素，openpyxl 读取不再报「no default style」。
- ✨ 新增 `?wd=关键词` 直接搜索（方便书签直达）。
- ✅ 打包后重跑 60 项接口回归测试全部通过。

### v1.0.0
- 首个版本：聚合搜索、多线程下载、AES-128 解密、ffmpeg 转封装、Excel/CSV/JSON 导出。

## 🧩 目录结构

```
m3u8-downloader/
├── m3u8tool.py        # 主程序：HTTP 服务 + 12 个 API + 内置 xlsx 写出
├── m3u8_engine.py     # 下载引擎：m3u8 解析 / 并发下载 / AES-128 解密 / ffmpeg 转封装
├── hls_fixture.py     # 测试用 HLS 加密源生成器
├── test_api.py        # 接口回归测试（60 项断言）
├── web/index.html     # 前端单页（搜索 / 设置 / 结果表 / 下载队列）
├── sources.json       # 资源站配置（可自行增删接口）
└── m3u8tool.spec      # PyInstaller 打包配置
```

## 🔬 测试与质量

- **AES 实现**：通过 FIPS-197 C.1 与 NIST SP800-38A CBC-AES128/256 官方向量
- **端到端**：本地加密 fixture 逐字节 sha256 校验一致；真实 CDN（明文 + 加密）分片解密后均为合法 MPEG-TS（`0x47` 同步字节）
- **接口回归**：`python test_api.py` 60 项断言全部通过
- **真实下载**：43 分钟 / 645 分片 / 345 MB 实测 0 失败，转出的 MP4 经 ffprobe 验证（h264 1080×606 + aac）

## ❓ 常见问题

**Q: 为什么有的资源站搜不到？**
闪电 / 天涯 / 无水印 3 个接口本身不支持关键词搜索，只能站内浏览；其余接口偶尔抖动可重试。

**Q: 下载失败提示 403？**
部分资源站有 Referer 防盗链，程序已自动带 Referer；若仍失败可换一个资源站的同款资源。

**Q: MP4 转换失败？**
确认 ffmpeg.exe 路径有效（页面顶部胶囊会显示「已就绪」）；转换失败时自动保留 .ts，不影响观看。

**Q: 能下 4K 吗？**
程序自动选 master playlist 里带宽最高的码率，资源站有 4K 就能下 4K。

---

## ⚠️ 免责声明

本工具仅用于 **个人学习、技术研究与缓存已授权内容**。请尊重版权，勿用于商业用途或传播受版权保护的影视作品；资源均来自第三方公开采集接口，与本工具无关。

## 📄 许可证

MIT License © 公歧子 (gongqizi0)
