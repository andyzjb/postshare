#!/usr/bin/env python3
# 微博每日海报生成器 —— 纯 PIL 拼图，不用 AI
# 从 popvideos /api/movies 拉最近新上的资源，取海报拼 3x3 网格 + 标题栏 + 底部站名水印
import json, math, os, sys, urllib.request

API = os.environ.get("POPVIDEOS_API", "http://192.168.1.6:8080")
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "..", "data", "poster.jpg")
# Noto Sans CJK Bold — 粗体醒目，比文泉驿好看
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
CACHE = os.path.join(BASE, "..", "data", "poster-cache")

# 画布
W, H = 1080, 1600          # 3:4 拉长一点给标题留空间
COLS, ROWS = 3, 3
CELL_W, CELL_H = (W - 40) // COLS, 380   # 每个格子
HEADER_H = 150
FOOTER_H = 140

BG = (18, 24, 38)          # 深蓝黑，跟站点主题一致
ACCENT = (126, 217, 87)    # 荧光绿（站点同款）

def fetch_movies():
    with urllib.request.urlopen(f"{API}/api/movies", timeout=10) as r:
        return json.load(r)

def recent(data, days=3, limit=9):
    cutoff = now_ms() - days * 86400 * 1000
    all_ = []
    for v in (data.get("categories") or {}).values():
        all_.extend(v)
    seen, out = set(), []
    for m in sorted(all_, key=lambda x: x.get("createdAt") or 0, reverse=True):
        if m.get("createdAt") and m["createdAt"] >= cutoff and m["fid"] not in seen and m.get("poster"):
            seen.add(m["fid"])
            out.append(m)
            if len(out) >= limit:
                break
    return out

def now_ms():
    import time
    return int(time.time() * 1000)

def download_poster(url, fid):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"{fid}.jpg")
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return path
    # URL 里的中文/空格需要百分号编码
    import urllib.parse
    safe_url = urllib.parse.quote(url, safe=":/?&=%.")
    with urllib.request.urlopen(safe_url, timeout=15) as r, open(path, "wb") as f:
        f.write(r.read())
    return path

def fit_cover(img, w, h):
    """居中裁剪填满目标尺寸（cover 模式，不留黑边）"""
    scale = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * scale), int(img.height * scale)))
    x = (img.width - w) // 2
    y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))

def main():
    from PIL import Image, ImageDraw, ImageFont
    data = fetch_movies()
    movies = recent(data)
    if len(movies) < 4:
        print(f"最近3天新上仅 {len(movies)} 部，不足以拼海报，跳过")
        sys.exit(2)

    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    f_title = ImageFont.truetype(FONT, 64)     # 主标题 64px
    f_sub = ImageFont.truetype(FONT, 32)        # 副标题
    f_foot = ImageFont.truetype(FONT, 44)       # 底部网址
    f_foot_sub = ImageFont.truetype(FONT, 28)   # 底部说明
    f_badge = ImageFont.truetype(FONT, 28)      # 角标
    f_movie_title = ImageFont.truetype(FONT, 24)  # 影片名称

    # === 顶部标题栏 ===
    draw.text((40, 24), "今日上新", font=f_title, fill=(255, 255, 255))
    draw.text((40, 96), "热播剧综 · 每日更新 · 免费观看", font=f_sub, fill=(180, 190, 210))
    draw.rectangle([40, HEADER_H - 6, W - 40, HEADER_H], fill=ACCENT)

    # === 海报网格 ===
    grid_top = HEADER_H
    cell_actual_h = (H - HEADER_H - FOOTER_H) // ROWS
    for i, m in enumerate(movies[: COLS * ROWS]):
        row, col = divmod(i, COLS)
        x0 = 20 + col * ((W - 40) // COLS)
        y0 = grid_top + 12 + row * cell_actual_h
        cw = (W - 40) // COLS - 12
        ch = cell_actual_h - 48   # 留底部给影片名

        try:
            p = download_poster(API + m["poster"], m["fid"])
            img = fit_cover(Image.open(p).convert("RGB"), cw, ch)
            canvas.paste(img, (x0, y0))
        except Exception as e:
            print(f"[warn] 海报失败 {m.get('title')}: {e}")
            draw.rectangle([x0, y0, x0 + cw, y0 + ch], fill=(40, 50, 70))
            draw.text((x0 + 12, y0 + ch // 2 - 20), m.get("title", "")[:8], font=ImageFont.truetype(FONT, 28), fill=(120, 130, 150))

        # 角标：豆瓣分或"新"
        badge = f"{m['rating']}分" if m.get("rating") else "NEW"
        bw = draw.textlength(badge, font=f_badge)
        bx, by = x0 + cw - bw - 16, y0 + 12
        draw.rectangle([bx - 8, by - 4, bx + bw + 8, by + 34], fill=(200, 60, 60))
        draw.text((bx, by), badge, font=f_badge, fill=(255, 255, 255))

        # 影片名称（海报下方居中）
        title = m.get("title", "")
        # 截断过长的标题
        if len(title) > 12:
            title = title[:10] + ".."
        tw = draw.textlength(title, font=f_movie_title)
        tx = x0 + (cw - tw) // 2
        ty = y0 + ch + 8
        draw.text((tx, ty), title, font=f_movie_title, fill=(220, 225, 235))

    # === 底部水印栏 ===
    fy = H - FOOTER_H + 24
    draw.rectangle([40, fy - 14, W - 40, fy - 8], fill=(60, 70, 90))

    # 网址
    site = "squark.cc.cd"
    sw = draw.textlength(site, font=f_foot)
    draw.text(((W - sw) // 2, fy), site, font=f_foot, fill=ACCENT)

    # 说明
    sub = "免费无广告 · 手机电脑都能看"
    sw2 = draw.textlength(sub, font=f_foot_sub)
    draw.text(((W - sw2) // 2, fy + 60), sub, font=f_foot_sub, fill=(180, 190, 210))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    canvas.save(OUT, "JPEG", quality=88)
    print(f"海报已生成: {OUT}  ({os.path.getsize(OUT)//1024}KB, {len(movies)}部)")

if __name__ == "__main__":
    main()