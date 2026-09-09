#!/usr/bin/env python3
# Linux 桌面应用图标 + 应用截图
# 图标风格：圆形/圆角方形，深蓝底 + 绿色场记板 + 影视元素
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "app-assets-os")
os.makedirs(OUT, exist_ok=True)

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
BG = (18, 24, 38)
ACCENT = (126, 217, 87)
WHITE = (255, 255, 255)

def make_linux_icon(size):
    """Linux 桌面应用图标：圆角方形，深蓝底 + 绿色场记板"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    r = size // 6
    draw.rounded_rectangle([(0, 0), (size - 1, size - 1)], radius=r, fill=BG)

    # 场记板
    board_w = size * 0.62
    board_h = size * 0.52
    bx = (size - board_w) / 2
    by = (size - board_h) / 2 - size * 0.02

    # 板身（白色）
    draw.rounded_rectangle([bx, by, bx + board_w, by + board_h], radius=4, fill=(245, 245, 250))

    # 三条深色条纹
    stripe_h = board_h * 0.08
    for i in range(3):
        sy = by + 4 + i * (stripe_h + 3)
        draw.rectangle([bx + 5, sy, bx + board_w - 5, sy + stripe_h], fill=(40, 50, 70))

    # 右侧三角（打开状态）
    tri_h = board_h * 0.32
    tri_w = board_w * 0.10
    draw.polygon([(bx + board_w - 2, by + 4),
                  (bx + board_w + tri_w, by + tri_h / 2 + 4),
                  (bx + board_w - 2, by + tri_h + 4)], fill=(180, 190, 210))

    # 绿色小圆点装饰（在板子右下角，表示"在线/活跃"）
    dot_r = size * 0.04
    dot_x = bx + board_w - dot_r - 6
    dot_y = by + board_h - dot_r - 6
    draw.ellipse([dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r], fill=ACCENT)

    return img

def make_linux_screenshot():
    """Linux 桌面截图：模拟 GNOME/KDE 桌面，展示应用界面"""
    W, H = 720, 480
    img = Image.new("RGB", (W, H), (35, 38, 45))
    draw = ImageDraw.Draw(img)

    # 顶部面板（系统栏）
    draw.rectangle([(0, 0), (W, 32)], fill=(28, 30, 36))
    draw.text((12, 6), "  Activities   每日影视海报  —  ×  □  —", font=ImageFont.truetype(FONT, 12), fill=(200, 200, 210))

    # 应用窗口
    win_x, win_y, win_w, win_h = 40, 48, W - 80, H - 64
    draw.rounded_rectangle([win_x, win_y, win_x + win_w, win_y + win_h], radius=8, fill=(18, 24, 38))
    # 窗口标题栏
    draw.rounded_rectangle([win_x, win_y, win_x + win_w, win_y + 36], radius=8, fill=(22, 28, 42))
    draw.rectangle([win_x, win_y + 20, win_x + win_w, win_y + 36], fill=(22, 28, 42))
    draw.text((win_x + 16, win_y + 10), "  🎬  每日影视海报  — 每日自动发布微博图文", font=ImageFont.truetype(FONT, 12), fill=(180, 190, 210))

    # 窗口内容：左侧导航 + 右侧内容
    # 左侧栏
    nav_x = win_x + 12
    nav_y = win_y + 48
    nav_items = ["📊 今日概览", "📅 发布记录", "⚙ 设置"]
    for i, item in enumerate(nav_items):
        draw.rounded_rectangle([nav_x, nav_y + i * 32, nav_x + 140, nav_y + i * 32 + 26], radius=4,
                               fill=(30, 40, 60) if i == 0 else (0, 0, 0, 0))
        draw.text((nav_x + 10, nav_y + i * 32 + 4), item, font=ImageFont.truetype(FONT, 12),
                  fill=WHITE if i == 0 else (160, 170, 190))

    # 右侧内容：海报预览
    cx = nav_x + 160
    cy = nav_y

    # 今日状态
    draw.text((cx, cy), "今日状态", font=ImageFont.truetype(FONT, 16), fill=WHITE)
    draw.text((cx, cy + 24), "✅ 海报已生成  |  ✅ 文案已就绪  |  ⏳ 等待发布 (10:00)", font=ImageFont.truetype(FONT, 11), fill=(160, 170, 190))

    # 海报缩略预览
    py = cy + 52
    draw.rounded_rectangle([cx, py, cx + 110, py + 150], radius=4, fill=(ACCENT[0]//2, ACCENT[1]//2, ACCENT[2]//2))
    draw.text((cx + 30, py + 60), "海报", font=ImageFont.truetype(FONT, 14), fill=WHITE)

    # 文案预览
    draw.text((cx + 130, py + 4), "今日发布文案：", font=ImageFont.truetype(FONT, 12), fill=(180, 190, 210))
    draw.text((cx + 130, py + 26), "【今日上新】", font=ImageFont.truetype(FONT, 12), fill=WHITE)
    draw.text((cx + 130, py + 46), "1.《求救信号》豆瓣7.0分", font=ImageFont.truetype(FONT, 11), fill=(180, 190, 210))
    draw.text((cx + 130, py + 64), "2.《坠落2》豆瓣5.5分", font=ImageFont.truetype(FONT, 11), fill=(180, 190, 210))
    draw.text((cx + 130, py + 82), "3.《怒之杀》豆瓣5.8分", font=ImageFont.truetype(FONT, 11), fill=(180, 190, 210))

    # 发布按钮
    btn_y = py + 120
    draw.rounded_rectangle([cx + 130, btn_y, cx + 280, btn_y + 32], radius=16, fill=ACCENT)
    draw.text((cx + 170, btn_y + 6), "📤 立即发布", font=ImageFont.truetype(FONT, 13), fill=BG)

    # 底部状态栏
    draw.rectangle([(win_x, win_y + win_h - 28), (win_x + win_w, win_y + win_h)], fill=(22, 28, 42))
    draw.text((win_x + 12, win_y + win_h - 22), "上次发布: 2026-09-08 10:00 ✅  |  下次发布: 2026-09-09 10:00", font=ImageFont.truetype(FONT, 10), fill=(120, 130, 150))

    return img


# === 生成 Linux 图标（多尺寸） ===
print("生成 Linux 桌面图标...")
for size in [64, 128, 256, 512]:
    ico = make_linux_icon(size)
    name = f"icon-{size}.png"
    ico.save(os.path.join(OUT, name), "PNG")
    print(f"  {name}  ({size}x{size})")

# 生成一张 512x512 作为主图标（用于 GitHub 仓库和微博）
main_ico = make_linux_icon(512)
main_ico.save(os.path.join(OUT, "icon.png"), "PNG")
print(f"  icon.png  (512x512)")

# === 生成 Linux 桌面截图 ===
print("生成 Linux 桌面截图...")
screenshot = make_linux_screenshot()
screenshot.save(os.path.join(OUT, "screenshot-linux.png"), "PNG")
print(f"  screenshot-linux.png  ({screenshot.width}x{screenshot.height})")

print(f"\n全部生成完成，路径: {OUT}")
print("图标: icon-64/128/256/512.png + icon.png (主图标)")
print("截图: screenshot-linux.png (GNOME/KDE 风格桌面截图)")
print("上传到微博开放平台桌面+Linux应用审核页面。")