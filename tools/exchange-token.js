// 用授权码换 access_token，写进 weibo-config.mjs
// 用法: node tools/exchange-token.js <CODE>
import fs from "fs";
import cfg from "../lib/weibo-config.mjs";

const code = process.argv[2];
if (!code) { console.error("用法: node tools/exchange-token.js <CODE>"); process.exit(1); }
if (!cfg.appKey || !cfg.appSecret) { console.error("先在 lib/weibo-config.mjs 填 appKey/appSecret"); process.exit(1); }

const res = await fetch("https://api.weibo.com/oauth2/access_token", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({
    client_id: cfg.appKey,
    client_secret: cfg.appSecret,
    grant_type: "authorization_code",
    code,
    redirect_uri: cfg.redirectUri || ""
  })
});
const data = await res.json();
if (data.error) { console.error("失败:", data.error, data.error_code); process.exit(1); }

console.log("access_token:", data.access_token);
console.log("expires_in:", data.expires_in, "秒");
console.log("过期时间:", new Date(Date.now() + data.expires_in * 1000).toISOString());

cfg.accessToken = data.access_token;
cfg.refreshToken = data.refresh_token || cfg.refreshToken;
cfg.expiresAt = Date.now() + data.expires_in * 1000;
fs.writeFileSync("lib/weibo-config.mjs", `export default ${JSON.stringify(cfg, null, 2)};\n`);
console.log("已写入 lib/weibo-config.mjs");
