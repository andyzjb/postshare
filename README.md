# 每日影视海报

> 一款运行于 Linux 桌面的影视海报自动生成工具，对接微博开放平台，每日定时发布图文微博。

每日自动生成影视海报并发布微博。

## 功能介绍

「每日影视海报」是一个运行在 Linux 桌面环境的自动化工具，通过微博开放平台 API，每日精选热门影视作品，自动生成竖版海报并定时发布图文微博。

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

![应用概览](data/app-assets-os/screenshot-1-overview.jpg)

![分享到微博](data/app-assets-os/screenshot-2-weibo.jpg)

![发布界面](data/app-assets-os/screenshot-3-phone.jpg)

## 技术栈

- Python 3 + Pillow（海报生成）
- Node.js（文案生成 + 微博 API 调用）
- 微博开放平台（图文发布）