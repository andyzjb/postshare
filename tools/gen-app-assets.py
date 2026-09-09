#!/usr/bin/env python3
# 生成微博开放平台应用审核所需的介绍图
# 这次重点展示"海报→发微博→微博展现"这条链
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "app-assets")
os.makedirs(OUT, exist_ok=True)

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
BG = (18, 24, 38)
ACCENT = (126, 217, 87)
WHITE = (255, 255, 255)
LIGHT = (180, 190, 210)

def make_intro_img(title, desc_lines, filename, show_weibo=True):
    """生成 450x300 介绍图，带微博相关元素"""
    W, H = 450, 300
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft = ImageFont.truetype(FONT, 26)
    fs = ImageFont.truetype(FONT, 18)
    fsm = ImageFont.truetype(FONT, 14)

    # 顶部标题
    draw.text((20, 14), title, font=ft, fill=WHITE)
    draw.rectangle([20, 48, 430, 52], fill=ACCENT)

    # 描述行
    y = 66
    for line in desc_lines:
        draw.text((20, y), line, font=fs, fill=LIGHT)
        y += 26

    # 底部：模拟微博界面卡片
    if show_weibo:
        card_y = H - 110
        card_h = 100
        # 微博卡片背景
        draw.rounded_rectangle([20, card_y, 430, card_y + card_h], radius=6, fill=(248, 248, 248))

        # 微博头像（圆形）
        avatar_x, avatar_y = 34, card_y + 12
        draw.ellipse([avatar_x, avatar_y, avatar_x + 24, avatar_y + 24], fill=(200, 200, 210))
        draw.text((avatar_x + 6, avatar_y + 6), "W", font=ImageFont.truetype(FONT, 16), fill=(100, 100, 110))

        # 微博昵称
        draw.text((avatar_x + 34, avatar_y + 2), "热门影视推荐", font=ImageFont.truetype(FONT, 14), fill=(50, 50, 60))
        draw.text((avatar_x + 34, avatar_y + 20), "刚刚 来自微博开放平台", font=ImageFont.truetype(FONT, 10), fill=(160, 160, 170))

        # 微博正文（缩略）
        draw.text((avatar_x, avatar_y + 36), "【今日上新】1.《逃出布迪秀》豆瓣7.4分...", font=ImageFont.truetype(FONT, 12), fill=(60, 60, 70))

        # 微博配图缩略（小方块）
        thumb_x, thumb_y = avatar_x, avatar_y + 56
        draw.rounded_rectangle([thumb_x, thumb_y, thumb_x + 36, thumb_y + 36], radius=3, fill=(200, 60, 60))
        draw.rounded_rectangle([thumb_x + 40, thumb_y, thumb_x + 76, thumb_y + 36], radius=3, fill=(60, 100, 200))
        draw.rounded_rectangle([thumb_x + 80, thumb_y, thumb_x + 116, thumb_y + 36], radius=3, fill=(ACCENT))

        # 底部互动按钮
        btn_y = thumb_y + 40
        draw.text((thumb_x, btn_y), "♡ 赞 12", font=ImageFont.truetype(FONT, 10), fill=(160, 160, 170))
        draw.text((thumb_x + 70, btn_y), "↻ 转发 3", font=ImageFont.truetype(FONT, 10), fill=(160, 160, 170))
        draw.text((thumb_x + 150, btn_y), "✎ 评论 1", font=ImageFont.truetype(FONT, 10), fill=(160, 160, 170))

    img.save(os.path.join(OUT, filename), "PNG")
    print(f"  {filename}  ({W}x{H})  {'✓ 含微博界面' if show_weibo else ''}")

# === 介绍图 ===
print("生成审核介绍图...")

make_intro_img("1. 每日生成海报",
    ["每日自动从热门影视中精选9部作品",
     "PIL拼图生成1080×1600竖版海报",
     "包含评分角标、片名、底部网址水印"],
    "intro-1.png",
    show_weibo=False)

make_intro_img("2. 自动发布微博图文",
    ["海报生成后自动拼接文案",
     "通过微博开放平台API发布图文微博",
     "每日定时自动发布，无需人工干预"],
    "intro-2.png",
    show_weibo=True)

make_intro_img("3. 微博展示效果",
    ["微博信息流中展示海报+文案",
     "点击跳转squark.cc.cd浏览完整片库",
     "手机电脑均可访问"],
    "intro-3.png",
    show_weibo=True)

print(f"\n全部生成完成，路径: {OUT}")
print("第1张展示海报生成，第2-3张展示微博发布流程和效果。")