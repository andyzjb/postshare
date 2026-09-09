// 干跑：生成文案但不发，验证全链路
import { main } from "./gen-daily.js";

const text = await main();
if (text) {
  console.log("\n---检查---");
  console.log(`长度: ${text.length} 字`);
  console.log("未发现外链:", !text.includes("http"));
}
