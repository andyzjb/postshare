// popvideos 数据源
// 测试阶段从 .6 拉公开 API；数据只读，零侵入
import fs from "fs";

const API_URL = process.env.POPVIDEOS_API || "http://192.168.1.6:8080/api/movies";
const CACHE = process.env.CACHE_FILE || "data/movies-cache.json";

export async function loadMovies() {
  try {
    const res = await fetch(API_URL, { signal: AbortSignal.timeout(10000) });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    fs.mkdirSync("data", { recursive: true });
    fs.writeFileSync(CACHE, JSON.stringify(data));
    return data;
  } catch (e) {
    // 拉不到就用缓存（发微博不能因为 .6 抖动就中断）
    if (fs.existsSync(CACHE)) {
      console.warn(`[warn] API failed (${e.message}), using cache`);
      return JSON.parse(fs.readFileSync(CACHE, "utf8"));
    }
    throw e;
  }
}

// 取最近 N 天新上的资源（createdAt 毫秒时间戳）
export function recentMovies(data, days = 3, limit = 10) {
  const cutoff = Date.now() - days * 86400 * 1000;
  const all = Object.values(data.categories || {}).flat();
  const seen = new Set();
  return all
    .filter(m => m.createdAt && m.createdAt >= cutoff && !seen.has(m.fid) && seen.add(m.fid))
    .sort((a, b) => b.createdAt - a.createdAt)
    .slice(0, limit);
}

export function fmtMovie(m) {
  const parts = [`《${m.title}》`];
  if (m.year) parts.push(`(${m.year})`);
  if (m.rating) parts.push(`豆瓣${m.rating}分`);
  if (Array.isArray(m.genres) && m.genres.length) parts.push(m.genres.slice(0, 2).join("/"));
  return parts.join(" ");
}
