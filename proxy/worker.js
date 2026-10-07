/**
 * 免费工具集导航 · M3U8 聚合搜索代理
 * ---------------------------------------------------------------
 * 作用：给「在线托管」的导航页（如 GitHub Pages）提供一个可跨域访问
 *       各影视资源站采集接口的中转服务。
 *
 * 部署（全程免费，约 2 分钟，无需域名 / 无需信用卡）：
 *   1. 打开 https://dash.cloudflare.com/ 注册或登录
 *   2. 左侧菜单 → Compute (Workers) → Create → Start with Hello World
 *   3. 把本文件全部内容覆盖进去，右上角 Deploy
 *   4. 复制分配给你的地址，形如：
 *        https://xxx-xxx.your-name.workers.dev
 *   5. 回到导航页 → 影音娱乐 › M3U8 影视资源站 → 点「⚙ 代理设置」
 *      把这个地址粘进去，确定。即可稳定搜索。
 *
 * 免费额度：10 万次请求 / 天，个人使用绰绰有余。
 * ---------------------------------------------------------------
 */

// 仅允许转发到已知的资源站域名，避免被当成开放代理滥用
const ALLOW_HOSTS = [
  'guangsuapi.com', 'lziapi.com', 'hongniuzy2.com', '360zyzz.com',
  'zuidapi.com', 'iqiyizyapi.com', 'jyzyapi.com', 'sdzyapi.com',
  'tyyszyapi.com', 'wsyzy.net', 'wolongzyw.com'
];

function hostAllowed(u) {
  try {
    const h = new URL(u).hostname.toLowerCase();
    return ALLOW_HOSTS.some(d => h === d || h.endsWith('.' + d));
  } catch (e) {
    return false;
  }
}

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Max-Age': '86400'
};

export default {
  async fetch(request) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }

    const reqUrl = new URL(request.url);
    let target = reqUrl.searchParams.get('url');

    // 兼容直接拼在路径后的写法：/https://api.xxx.com/...
    if (!target) {
      const raw = reqUrl.pathname.replace(/^\/+/, '');
      if (/^https?:\/\//i.test(raw)) target = raw + reqUrl.search;
    }

    if (!target) {
      return new Response(
        JSON.stringify({ error: 'missing url param', usage: '?url=<encoded target>' }, null, 2),
        { status: 400, headers: { ...CORS, 'Content-Type': 'application/json;charset=utf-8' } }
      );
    }

    if (!hostAllowed(target)) {
      return new Response(
        JSON.stringify({ error: 'target host not allowed', target }, null, 2),
        { status: 403, headers: { ...CORS, 'Content-Type': 'application/json;charset=utf-8' } }
      );
    }

    try {
      const upstream = await fetch(target, {
        method: 'GET',
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                        '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
          'Accept': 'application/json,text/plain,*/*',
          'Accept-Language': 'zh-CN,zh;q=0.9'
        },
        redirect: 'follow'
      });

      const body = await upstream.arrayBuffer();
      return new Response(body, {
        status: upstream.status,
        headers: {
          ...CORS,
          'Content-Type': upstream.headers.get('Content-Type') || 'application/json;charset=utf-8',
          'Cache-Control': 'no-store'
        }
      });
    } catch (e) {
      return new Response(
        JSON.stringify({ error: 'upstream fetch failed', detail: String(e) }, null, 2),
        { status: 502, headers: { ...CORS, 'Content-Type': 'application/json;charset=utf-8' } }
      );
    }
  }
};
