#!/usr/bin/env python3
# Linux 桌面截图：展示应用界面 + 微博发布流程
# GNOME 风格，深色主题，突出微博功能
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "app-assets-os")
os.makedirs(OUT, exist_ok=True)

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
BG = (18, 24, 38)
ACCENT = (126, 217, 87)
WHITE = (255, 255, 255)

def make_screenshot():
    W, H = 720, 480
    img = Image.new("RGB", (W, H), (35, 38, 45))
    draw = ImageDraw.Draw(img)

    # 顶部系统栏 (GNOME 风格)
    draw.rectangle([(0, 0), (W, 30)], fill=(28, 30, 36))
    draw.text((12, 6), "  Activities   每日影视海报", font=ImageFont.truetype(FONT, 12), fill=(200, 200, 210))

    # 应用窗口
    win_x, win_y, win_w, win_h = 30, 40, W - 60, H - 55
    draw.rounded_rectangle([win_x, win_y, win_x + win_w, win_y + win_h], radius=8, fill=(18, 24, 38))

    # 窗口标题栏
    draw.rounded_rectangle([win_x, win_y, win_x + win_w, win_y + 34], radius=8, fill=(22, 28, 42))
    draw.rectangle([win_x, win_y + 20, win_x + win_w, win_y + 34], fill=(22, 28, 42))
    draw.text((win_x + 14, win_y + 10), "  🎬  每日影视海报  —  每日自动发布微博图文", font=ImageFont.truetype(FONT, 12), fill=(180, 190, 210))

    # ===== 窗口内容 =====
    # 左侧导航栏
    nav_x = win_x + 14
    nav_y = win_y + 46
    nav_items = ["📊 今日概览", "📅 历史记录", "⚙ 设置"]
    for i, item in enumerate(nav_items):
        fill_color = (30, 40, 60) if i == 0 else None
        if fill_color:
            draw.rounded_rectangle([nav_x, nav_y + i * 30, nav_x + 130, nav_y + i * 30 + 24], radius=4, fill=fill_color)
        draw.text((nav_x + 8, nav_y + i * 30 + 4), item, font=ImageFont.truetype(FONT, 12),
                  fill=WHITE if i == 0 else (160, 170, 190))

    cx = nav_x + 150
    cy = nav_y

    # 今日状态
    draw.text((cx, cy), "今日状态", font=ImageFont.truetype(FONT, 16), fill=WHITE)

    # 三个状态标签
    status_y = cy + 26
    labels = ["✅ 海报已生成", "✅ 文案已就绪", "⏳ 10:00 定时发布"]
    for i, label in enumerate(labels):
        lx = cx + i * 130
        draw.rounded_rectangle([lx, status_y, lx + 118, status_y + 22], radius=4, fill=(25, 35, 55))
        draw.text((lx + 8, status_y + 3), label, font=ImageFont.truetype(FONT, 10), fill=ACCENT if "✅" in label else (200, 180, 100))

    # ===== 重点：展示微博发布功能 =====
    # 左侧：海报预览缩略
    py = cy + 60
    draw.rounded_rectangle([cx, py, cx + 100, py + 140], radius=6, fill=(ACCENT[0]//3, ACCENT[1]//3, ACCENT[2]//3))
    draw.text((cx + 28, py + 60), "海报", font=ImageFont.truetype(FONT, 14), fill=WHITE)

    # 右侧：文案预览 + 微博发布按钮
    tx = cx + 120
    # 文案框
    draw.rounded_rectangle([tx, py, tx + 300, py + 80], radius=6, fill=(25, 30, 45))
    draw.text((tx + 12, py + 8), "【今日上新】", font=ImageFont.truetype(FONT, 13), fill=WHITE)
    draw.text((tx + 12, py + 30), "1.《求救信号》豆瓣7.0分  喜剧/动作", font=ImageFont.truetype(FONT, 11), fill=(180, 190, 210))
    draw.text((tx + 12, py + 50), "2.《坠落2》豆瓣5.5分  惊悚/冒险", font=ImageFont.truetype(FONT, 11), fill=(180, 190, 210))

    # 微博图标 + 来源说明
    src_y = py + 90
    draw.text((tx, src_y), "📱 发布到微博  →  来源: 每日影视海报", font=ImageFont.truetype(FONT, 12), fill=ACCENT)

    # 绿色发布按钮
    btn_y = src_y + 28
    draw.rounded_rectangle([tx + 60, btn_y, tx + 180, btn_y + 32], radius=16, fill=ACCENT)
    draw.text((tx + 90, btn_y + 6), "📤 发布到微博", font=ImageFont.truetype(FONT, 13), fill=BG)

    # ===== 底部：模拟微博发布成功记录 =====
    foot_y = win_y + win_h - 80
    draw.rectangle([(win_x + 10, foot_y), (win_x + win_w - 10, foot_y + 66)], fill=(22, 28, 42))

    # 微博卡片缩略
    card_y = foot_y + 8
    draw.rounded_rectangle([cx, card_y, cx + 280, card_y + 50], radius=6, fill=(248, 248, 248))
    # 微博头像
    draw.ellipse([(cx + 8, card_y + 6), (cx + 24, card_y + 22)], fill=(200, 200, 210))
    draw.text((cx + 30, card_y + 4), "热门影视推荐", font=ImageFont.truetype(FONT, 10), fill=(50, 50, 60))
    draw.text((cx + 30, card_y + 20), "刚刚 来自每日影视海报", font=ImageFont.truetype(FONT, 9), fill=(160, 160, 170))
    draw.text((cx + 8, card_y + 34), "【今日上新】1. 求救信号 豆瓣7.0分...", font=ImageFont.truetype(FONT, 9), fill=(80, 80, 90))

    # 底部状态栏
    draw.rectangle([(win_x, win_y + win_h - 28), (win_x + win_w, win_y + win_h)], fill=(22, 28, 42))
    draw.text((win_x + 12, win_y + win_h - 22), "上次发布: 2026-09-08 10:00 ✅  |  下次: 2026-09-09 10:00  |  来源: 每日影视海报", font=ImageFont.truetype(FONT, 10), fill=(120, 130, 150))

    return img

img = make_screenshot()
out_path = os.path.join(OUT, "screenshot-linux-weibo.png")
img.save(out_path, "PNG")
print(f"生成: {out_path}  ({img.width}x{img.height})")