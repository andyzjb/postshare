// 微博开放平台 API 封装
import cfg from "./weibo-config.mjs";

const API = "https://api.weibo.com/2";

function checkToken() {
  if (!cfg.accessToken) throw new Error("weibo-config.mjs 里 accessToken 为空，先跑 tools/oauth-guide.md 的授权流程");
  if (cfg.expiresAt && Date.now() > cfg.expiresAt) {
    throw new Error(`access_token 已过期 (${new Date(cfg.expiresAt).toISOString()})，用 refreshToken 续期或重新授权`);
  }
}

// 发文字微博。text 最长 2000 字（新浪会截断长文，建议 ≤140 保持完整展示）
export async function postText(text) {
  checkToken();
  const body = new URLSearchParams({ status: text, access_token: cfg.accessToken });
  const res = await fetch(`${API}/statuses/update.json`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
    signal: AbortSignal.timeout(15000)
  });
  const data = await res.json();
  if (data.error_code) throw new Error(`weibo ${data.error_code}: ${data.error}`);
  return data;
}

// 发图文微博：pic 传图片文件的本地路径或 Buffer
// 用 statuses/upload.json 上传二进制图片 + 文字
export async function postWithPic(text, picBuffer, filename = "poster.jpg") {
  checkToken();
  const fd = new FormData();
  fd.append("access_token", cfg.accessToken);
  fd.append("status", text);
  // pic 字段直接传二进制，用 Blob 包裹
  fd.append("pic", new Blob([picBuffer], { type: "image/jpeg" }), filename);
  const res = await fetch(`${API}/statuses/upload.json`, {
    method: "POST",
    body: fd,
    signal: AbortSignal.timeout(30000)
  });
  const data = await res.json();
  if (data.error_code) throw new Error(`weibo ${data.error_code}: ${data.error}`);
  return data;
}