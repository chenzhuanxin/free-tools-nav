# 在线托管时的 m3u8 搜索代理（免费，2 分钟部署）

## 为什么需要它

导航页放在 **GitHub Pages** 这类静态托管上时，浏览器受**同源策略**限制，
无法直接读取各影视资源站的采集接口。

实测 7 个可搜索资源站中，**只有「量子资源」返回了 `Access-Control-Allow-Origin: *`**
（可直连），其余 6 个必须通过代理中转。

公共 CORS 代理在 2026 年已大面积失效（实测 4 个中 3 个挂了），所以推荐自建一个，
**免费、稳定、不共享**。

## 部署步骤（Cloudflare Workers，免费 10 万次/天）

### 1. 注册 Cloudflare
打开 <https://dash.cloudflare.com/sign-up>，用邮箱注册并验证。无需绑定信用卡。

### 2. 创建 Worker
左侧菜单 → **Compute (Workers)** → **Create** → 选 **Start with Hello World** → **Deploy**

### 3. 粘贴代码
点 **Edit code**，把本目录 `worker.js` 的**全部内容**覆盖掉默认代码，右上角 **Deploy**。

### 4. 复制地址
部署完成后会分配一个地址，形如：

```
https://m3u8-proxy.your-name.workers.dev
```

### 5. 填进导航页
打开导航页 → 影音娱乐 › **M3U8 影视资源站** → 点 **⚙ 代理设置** → 粘贴地址 → 确定。

地址会存在浏览器本地，下次打开自动生效。想换或清除，再点一次「代理设置」即可。

## 验证代理是否可用

在浏览器直接访问（把地址换成你自己的）：

```
https://你的worker地址/?url=https%3A%2F%2Fcj.lziapi.com%2Fapi.php%2Fprovide%2Fvod%3Fac%3Dlist%26pg%3D1
```

看到一段 JSON（含 `"list"` 或 `"code"`）就说明代理正常。

## 安全说明

`worker.js` 内置了 **域名白名单**，只允许转发到下方已知资源站，
不会被别人拿去当开放代理刷流量：

```
guangsuapi.com  lziapi.com      hongniuzy2.com  360zyzz.com
zuidapi.com     iqiyizyapi.com  jyzyapi.com     sdzyapi.com
tyyszyapi.com   wsyzy.net       wolongzyw.com
```

如需增删，编辑 `worker.js` 顶部的 `ALLOW_HOSTS` 数组后重新 Deploy。

## 本地使用（无需代理）

如果只是自己用，直接双击 `serve.py` 打开 `http://127.0.0.1:8765`，
本地服务自带 `/api/proxy`，**不需要任何代理配置**，且 Excel 导出为标准 .xlsx。
