# 每日影视海报

每日自动生成影视海报并发布微博。

## 功能

- 每日从热门影视中精选 9 部作品，自动生成 1080×1600 竖版海报
- 自动拼接微博文案（含片名、评分、类型）
- 通过微博开放平台 API 定时发布图文微博
- 失败自动 PushPlus 告警

## 使用流程

```
生成海报（Python PIL） → 拼文案（Node.js） → 发微博（微博API） → 完成
```

## 截图

![发布流程](data/app-assets-os/screenshot-weibo-flow.png)

## 技术栈

- Python 3 + Pillow（海报生成）
- Node.js（文案生成 + 微博 API 调用）
- 微博开放平台（图文发布）