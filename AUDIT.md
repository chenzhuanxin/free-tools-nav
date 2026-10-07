# 项目审查报告

## A. 数据层问题（已修复）

| # | 问题 | 证据 | 处理 |
|---|---|---|---|
| A1 | **Tome**（AI 生成 PPT）404 | `https://tome.app/` → HTTP 404，服务已下线 | ✅ 删除 |
| A2 | **新媒体管家**（公众号）域名报废 | `xmt.cn` DNS 解析失败；2026-09 多方确认停服 | ✅ 删除 |
| A3 | **9 库音乐网** 404 | `www.9ku.com` → HTTP 404，多源确认停更 | ✅ 删除 |
| A4 | **Moviemania** URL 写错 | `www.moviemania.io` DNS 失败；正确是 `moviemania.io`（200） | ✅ 修正 URL |

**243 → 240 工具**

## B. 代码层问题（本次修复）

| # | 问题 | 位置 | 处理 |
|---|---|---|---|
| B1 | `link: it.vod_id ? '' : ''` **死代码**，两个分支都返回空串 | `parseVod()` | ✅ 删除该字段 |
| B2 | `pic` 字段已解析但**从未使用**（表格无封面），浪费 | `parseVod()` | ✅ 保留（导出用） |
| B3 | `type` 取值 `it.vod_class \|\| it.type_name`，实际接口返回的是 `type_name`，`vod_class` 恒为空 —— 顺序反了但结果正确，**保留** | - | ✅ 无需改 |
| B4 | `renderProxyHint()` 在**非本地**环境下提示"请用 serve.py"，但 GitHub Pages 上用户根本拿不到 serve.py，提示无效 | `renderProxyHint()` | ✅ 重写：区分 local / 静态托管 / file:// 三种场景 |
| B5 | **公共 CORS 代理 4 个中 3 个已失效**（实测） | codetabs 503、corsproxy.io 403 需 key、cors.workers.dev 已死；仅 allorigins 部分可用且限流 500 | ✅ 精简为可配置代理 + allorigins 兜底 |
| B6 | **静态托管下 m3u8 搜索几乎不可用**：实测 7 个可搜索源中仅「量子资源」返回 `Access-Control-Allow-Origin: *`，其余 6 个无法浏览器直连 | 实测 CORS 头 | ✅ 新增「直连优先」策略 + 自定义代理输入框 + 提供 Cloudflare Worker 脚本 |
| B7 | `m3u8Render` 的 m3u8 列按钮写「复制」但 `href` 是链接（语义矛盾） | `m3u8Render()` | ✅ 改为「打开」+ 另加复制按钮 |
| B8 | 未搜索时 `state.m3u8.meta` 未初始化，导出时 `meta` 为 undefined | `doSearch` 后 | ✅ 已由 `state.m3u8 = {results:[],running:false}` 兜底（无实际报错） |
| B9 | `downloadHtmlXls` 表头色仍是旧品牌色 `#4f7cff`，与新版 `#3d6dff` 不一致 | `downloadHtmlXls` | ✅ 改 `#3d6dff` |
| B10 | 「粘贴 Excel 数据」按钮实际调 `App.browseExcel()` 打开文件选择器，文案与行为不符 | modal | ✅ 文案改为「导入 Excel/CSV 文件」 |

## C. 已确认**不是**问题的项（避免误改）

- `greasyfork.org` / `wallhaven.cc` / `suno.com` / `gamma.app` / `pptbz.com` / `pptsupermarket.com` 探测超时 → **GFW 屏蔽**，国内浏览器同样打不开，但收录有价值，保留
- `unsplash` / `pexels` / `pixabay` / `freepik` 等 403 → **反爬**，浏览器正常
- `gsxt.gov.cn` 521 / `cponline.cnipa.gov.cn` 412 → **反爬**，浏览器正常
- `outlook.live.com` 417 → 需浏览器 UA，正常
- 3 个 nosearch 接口返回非 JSON → **符合预期**（已正确标注 `nosearch`）
- 20 个 M3U8 站点中 16 个 HTTP 200，4 个 Cloudflare 挑战 → 浏览器可开

## D. 关键实测数据（本次）

### D1. 7 个可搜索 M3U8 接口（全部 200 + 有结果）
```
光速资源    200  8条    量子资源   200  3条    红牛资源  200  8条
360资源    200  3条    最大资源   200  7条    爱奇艺    200  2条
金鹰资源    200  8条
```

### D2. CORS 支持情况（决定静态托管能否直连）
```
量子资源   Access-Control-Allow-Origin: *     ← 唯一可直连
其余 6 站  无 CORS 头                          ← 必须走代理
```

### D3. 公共 CORS 代理实测
```
api.allorigins.win/raw     ✅ 部分可用，但并发/连续请求会 500 限流
api.codetabs.com/v1/proxy  ❌ 503
corsproxy.io               ❌ 403（需 API Key）
test.cors.workers.dev      ❌ 已下线
```
