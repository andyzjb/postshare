# 微博开放平台 OAuth 授权指引（一次性操作）

## 1. 注册开发者
https://open.weibo.com → 接入微连接 → 网站接入（或移动应用）
- 创建应用后拿到 App Key / App Secret
- 授权回调地址随便填一个你能控制的域名，比如 https://squark.cc.cd/oauth/weibo
- 应用需要实名认证 + 审核（个人开发者一般 1-3 天）

## 2. 拿授权码（浏览器操作）
审核通过后，浏览器打开（替换 YOUR_APP_KEY 和回调地址）：
```
https://api.weibo.com/oauth2/authorize?client_id=YOUR_APP_KEY&response_type=code&redirect_uri=YOUR_CALLBACK
```
登录你要发微博的账号（建议小号），授权后页面跳到回调地址，地址栏里 `?code=XXXXX` 就是授权码（10 分钟内有效，只用一次）。

## 3. 换 access_token（把 code 填进来跑）
```
node tools/exchange-token.js <CODE>
```
会输出 access_token 和过期时间（一般 2 周到几个月），自动写进 lib/weibo-config.mjs。

## 4. token 续期
微博官方 access_token 有效期较长，过期前用 refresh_token 换新：
```
node tools/refresh-token.js
```
（cron 里可以每周跑一次自动续期）

## 5. 验证
```
npm run dry   # 只生成文案不发
npm run post  # 真发一条
```