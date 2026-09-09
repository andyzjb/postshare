// 生成今日微博文案（先文字版，图文后加）
import { loadMovies, recentMovies, fmtMovie } from "../lib/datasource.mjs";

const SITE = "popvideos"; // 站名口令，不带链接（带外链降权）

export function genText(movies) {
  if (!movies.length) return null;
  const lines = [`【今日上新】`];
  movies.forEach((m, i) => lines.push(`${i + 1}. ${fmtMovie(m)}`));
  lines.push("");
  lines.push(`更多热播影视，搜「${SITE}」即可访问，免费无广告，手机电脑都能看。`);
  const text = lines.join("\n");
  // 微博正文 140 字内完整展示，超长会被折叠
  return text.length <= 140 ? text : text.slice(0, 137) + "...";
}

export async function main() {
  const data = await loadMovies();
  const movies = recentMovies(data, 3, 10);
  console.log(`最近3天新上: ${movies.length} 部`);
  const text = genText(movies);
  console.log("---文案---");
  console.log(text || "（无新上内容，今日可跳过）");
  return text;
}

// 被直接运行时执行
if (process.argv[1] && process.argv[1].endsWith("gen-daily.js")) {
  main().catch(e => { console.error(e.message); process.exit(1); });
}
