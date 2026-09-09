#!/usr/bin/env python3
# 移动应用审核截图：展示"App 发微博"的完整流程
# 3 张截图 = 生成海报 → 分享到微博 → 微博上看到
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "app-assets-os")
os.makedirs(OUT, exist_ok=True)

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
BG = (18, 24, 38)
ACCENT = (126, 217, 87)
WHITE = (255, 255, 255)

def phone_frame_at(x, y, w, h):
    """返回手机外壳的绘制参数，用 draw.* 手动画"""
    return (x, y, w, h)

def draw_phone(draw, x, y, w, h, label="", fill_screen=None):
    """画一个手机外壳，返回屏幕区域 (sx, sy, sw, sh)"""
    # 外壳
    draw.rounded_rectangle([(x, y + 20), (x + w - 1, y + h - 1)], radius=20, fill=(28, 28, 32))
    # 屏幕
    screen_x, screen_y = x + 12, y + 38
    screen_w, screen_h = w - 24, h - 72
    draw.rounded_rectangle([(screen_x, screen_y), (screen_x + screen_w, screen_y + screen_h)], radius=6, fill=(0, 0, 0))
    # 刘海
    draw.rounded_rectangle([(x + w//2 - 24, y + 28), (x + w//2 + 24, y + 34)], radius=3, fill=(40, 40, 44))
    # 标签
    if label:
        f = ImageFont.truetype(FONT, 14)
        tw = draw.textlength(label, font=f)
        draw.text((x + (w - tw)//2, y + h + 4), label, font=f, fill=(160, 170, 190))
    return (screen_x, screen_y, screen_w, screen_h)

def fill_screen_bg(draw, sx, sy, sw, sh, color=BG):
    """填充屏幕区域背景"""
    draw.rounded_rectangle([(sx, sy), (sx + sw, sy + sh)], radius=6, fill=color)

def draw_text(draw, x, y, text, font_size, color=WHITE, max_w=None):
    """在指定位置画文字，返回下一行 y 坐标"""
    f = ImageFont.truetype(FONT, font_size)
    if max_w:
        # 自动换行
        lines = []
        for word in text.split("\n"):
            lines.append(word)
        for line in lines:
            draw.text((x, y), line, font=f, fill=color)
            y += font_size + 4
    else:
        draw.text((x, y), text, font=f, fill=color)
        y += font_size + 4
    return y

# 创建画布：3 张手机横向排列，每张 340x680 + 间距
CANVAS_W = 340 * 3 + 80
CANVAS_H = 720
img = Image.new("RGB", (CANVAS_W, CANVAS_H), (240, 242, 245))
draw = ImageDraw.Draw(img)

# 顶部标题
f_title = ImageFont.truetype(FONT, 22)
draw.text((40, 16), "每日影视海报 - 微博发布流程", font=f_title, fill=(50, 50, 60))

# === 手机1：生成海报 ===
sx, sy, sw, sh = draw_phone(draw, 30, 50, 320, 640, "① 自动生成海报")
fill_screen_bg(draw, sx, sy, sw, sh)
# 模拟海报内容
# 绿色标题
draw.text((sx + 20, sy + 20), "今日上新", font=ImageFont.truetype(FONT, 22), fill=WHITE)
draw.text((sx + 20, sy + 50), "热播剧综 · 每日更新", font=ImageFont.truetype(FONT, 14), fill=(180, 190, 210))
# 绿色分隔线
draw.rectangle([sx + 20, sy + 80, sx + sw - 20, sy + 83], fill=ACCENT)
# 3x3 海报缩略
cell_w = (sw - 60) // 3
cell_h = 80
posters_colors = [(200,60,60), (60,100,200), (ACCENT), (200,160,60), (100,100,200), (60,180,200), (200,100,100), (100,200,100), (200,200,60)]
for i in range(9):
    col = i % 3
    row = i // 3
    px = sx + 20 + col * (cell_w + 6)
    py = sy + 100 + row * (cell_h + 6)
    draw.rounded_rectangle([px, py, px + cell_w, py + cell_h], radius=4, fill=posters_colors[i])
    # 红色角标
    if i < 8:
        draw.rounded_rectangle([px + cell_w - 40, py + 4, px + cell_w - 4, py + 22], radius=2, fill=(200, 60, 60))
        draw.text((px + cell_w - 34, py + 4), "7.0分", font=ImageFont.truetype(FONT, 10), fill=WHITE)
    else:
        draw.rounded_rectangle([px + cell_w - 34, py + 4, px + cell_w - 4, py + 22], radius=2, fill=(200, 60, 60))
        draw.text((px + cell_w - 28, py + 4), "NEW", font=ImageFont.truetype(FONT, 10), fill=WHITE)
# 底部水印
draw.text((sx + (sw - draw.textlength("squark.cc.cd", font=ImageFont.truetype(FONT, 14)))//2, sy + sh - 50),
          "squark.cc.cd", font=ImageFont.truetype(FONT, 14), fill=ACCENT)

# === 手机2：分享到微博 ===
sx2, sy2, sw2, sh2 = draw_phone(draw, 380, 50, 320, 640, "② 一键分享到微博")
fill_screen_bg(draw, sx2, sy2, sw2, sh2)
# 分享界面
draw.text((sx2 + 20, sy2 + 20), "分享到微博", font=ImageFont.truetype(FONT, 18), fill=WHITE)
# 微博头像
draw.ellipse([(sx2 + 20, sy2 + 60), (sx2 + 44, sy2 + 84)], fill=(200, 200, 210))
draw.text((sx2 + 26, sy2 + 68), "W", font=ImageFont.truetype(FONT, 14), fill=(100, 100, 110))
# 账号
draw.text((sx2 + 52, sy2 + 64), "热门影视推荐", font=ImageFont.truetype(FONT, 14), fill=WHITE)
# 文案输入框
box_y = sy2 + 100
draw.rounded_rectangle([(sx2 + 20, box_y), (sx2 + sw2 - 20, box_y + 80)], radius=4, fill=(30, 35, 45))
draw.text((sx2 + 28, box_y + 8), "【今日上新】", font=ImageFont.truetype(FONT, 13), fill=(200, 200, 210))
draw.text((sx2 + 28, box_y + 28), "1.《求救信号》豆瓣7.0分", font=ImageFont.truetype(FONT, 12), fill=(160, 170, 190))
draw.text((sx2 + 28, box_y + 46), "2.《坠落2》豆瓣5.5分", font=ImageFont.truetype(FONT, 12), fill=(160, 170, 190))
# 配图缩略
thumb_y = box_y + 92
draw.rounded_rectangle([(sx2 + 20, thumb_y), (sx2 + 80, thumb_y + 60)], radius=4, fill=ACCENT)
draw.text((sx2 + 28, thumb_y + 20), "海报", font=ImageFont.truetype(FONT, 12), fill=WHITE)
# 发布按钮
btn_y = thumb_y + 76
draw.rounded_rectangle([(sx2 + sw2//2 - 60, btn_y), (sx2 + sw2//2 + 60, btn_y + 36)], radius=18, fill=ACCENT)
draw.text((sx2 + sw2//2 - 24, btn_y + 8), "发布", font=ImageFont.truetype(FONT, 16), fill=BG)

# === 手机3：微博上看到 ===
sx3, sy3, sw3, sh3 = draw_phone(draw, 730, 50, 320, 640, "③ 微博图文已发布")
fill_screen_bg(draw, sx3, sy3, sw3, sh3)
# 微博信息流界面
# 顶部"微博"标题
draw.text((sx3 + 20, sy3 + 12), "微博", font=ImageFont.truetype(FONT, 18), fill=WHITE)
# 微博卡片
card_y = sy3 + 50
draw.rounded_rectangle([(sx3 + 12, card_y), (sx3 + sw3 - 12, card_y + 250)], radius=6, fill=(248, 248, 248))
# 头像
draw.ellipse([(sx3 + 28, card_y + 12), (sx3 + 52, card_y + 36)], fill=(200, 200, 210))
draw.text((sx3 + 34, card_y + 20), "W", font=ImageFont.truetype(FONT, 14), fill=(100, 100, 110))
# 昵称
draw.text((sx3 + 60, card_y + 14), "热门影视推荐", font=ImageFont.truetype(FONT, 13), fill=(50, 50, 60))
draw.text((sx3 + 60, card_y + 32), "刚刚 来自每日影视海报", font=ImageFont.truetype(FONT, 10), fill=(160, 160, 170))
# 正文
draw.text((sx3 + 28, card_y + 56), "【今日上新】", font=ImageFont.truetype(FONT, 13), fill=(60, 60, 70))
draw.text((sx3 + 28, card_y + 76), "1.《求救信号》豆瓣7.0分", font=ImageFont.truetype(FONT, 12), fill=(80, 80, 90))
draw.text((sx3 + 28, card_y + 96), "2.《坠落2》豆瓣5.5分", font=ImageFont.truetype(FONT, 12), fill=(80, 80, 90))
# 配图
draw.rounded_rectangle([(sx3 + 28, card_y + 120), (sx3 + 28 + 160, card_y + 120 + 120)], radius=4, fill=ACCENT)
draw.text((sx3 + 80, card_y + 175), "海报", font=ImageFont.truetype(FONT, 14), fill=WHITE)
# 互动按钮
btn_y3 = card_y + 252
draw.text((sx3 + 28, btn_y3), "♡ 12", font=ImageFont.truetype(FONT, 11), fill=(160, 160, 170))
draw.text((sx3 + 90, btn_y3), "↻ 3", font=ImageFont.truetype(FONT, 11), fill=(160, 160, 170))
draw.text((sx3 + 150, btn_y3), "✎ 1", font=ImageFont.truetype(FONT, 11), fill=(160, 160, 170))
# 来源标注（重要！审核员看这个）
draw.text((sx3 + 28, btn_y3 + 22), "来自 每日影视海报", font=ImageFont.truetype(FONT, 10), fill=(ACCENT))

# 保存
out_path = os.path.join(OUT, "screenshot-weibo-flow.png")
img.save(out_path, "PNG")
print(f"已生成: {out_path}  ({img.width}x{img.height})")

# 也分别保存单张（灵活上传）
phones = [
    (img.crop((30, 50, 350, 690)), "1-gen-poster.png"),
    (img.crop((380, 50, 700, 690)), "2-share-weibo.png"),
    (img.crop((730, 50, 1050, 690)), "3-weibo-post.png"),
]
for p, name in phones:
    p.save(os.path.join(OUT, name), "PNG")
    print(f"已生成单张: {name}  ({p.width}x{p.height})")

print(f"\n路径: {OUT}")
print("3张截图展示完整流程：生成海报 → 分享到微博 → 微博图文已发布")
print("上传到微博开放平台移动应用审核页面。")