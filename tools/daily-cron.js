// 每日定时发文的检查脚本 —— 被 cron 调用
// 功能：判断今日是否已经发过文（避免重复发），如果未发则执行流水线
import { readFileSync, existsSync, writeFileSync } from "fs";
import { main } from "../lib/post.js";

const STATE_FILE = new URL("../data/post-state.json", import.meta.url).pathname;
const TZ_OFFSET = 8 * 60 * 60 * 1000; // UTC+8

function today() {
  // 北京时间日期
  const now = new Date(Date.now() + TZ_OFFSET);
  return now.toISOString().slice(0, 10);
}

function alreadyPosted() {
  if (!existsSync(STATE_FILE)) return false;
  try {
    const state = JSON.parse(readFileSync(STATE_FILE, "utf8"));
    return state.date === today() && state.posted === true;
  } catch { return false; }
}

function markPosted(id) {
  writeFileSync(STATE_FILE, JSON.stringify({ date: today(), posted: true, id: id || null }));
}

// 入口
if (alreadyPosted()) {
  console.log(`今日 (${today()}) 已发过，跳过`);
  process.exit(0);
}

main()
  .then(r => {
    if (r.success) {
      markPosted(r.id);
      console.log("✅ 每日发文完成");
    } else if (r.skipped) {
      console.log("⏭️ 跳过:", r.reason);
    }
  })
  .catch(async e => {
    console.error("❌ 流水线失败:", e.message);
    process.exit(1);
  });