// 每日自动发文入口
// 用法: node tools/post.js
import { main } from "../lib/post.js";

main()
  .then(r => {
    if (r.success) {
      console.log("✅ 每日发文完成");
    } else if (r.skipped) {
      console.log("⏭️ 跳过:", r.reason);
    }
  })
  .catch(async e => {
    console.error("❌ 流水线失败:", e.message);
    // 入口静默退出，lib/post.js 内部已处理 pushplus 告警
    // 这里再打一次确保进程退出码正确
    process.exit(1);
  });