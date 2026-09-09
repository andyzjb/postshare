// 每日自动发文流水线：生成海报 → 拼文案 → 图文发布 → 失败告警
// 被 tools/post.js 调用（或直接 node lib/post.js）
import { spawnSync } from "child_process";
import { readFileSync } from "fs";
import { postWithPic } from "./weibo-api.mjs";
import cfg from "./weibo-config.mjs";

const ROOT = new URL("..", import.meta.url).pathname;

function runScript(script, args = []) {
  const res = spawnSync(script, args, {
    cwd: ROOT,
    timeout: 60_000,
    stdio: ["ignore", "pipe", "pipe"],
    env: { ...process.env }
  });
  const out = res.stdout.toString().trim();
  const err = res.stderr.toString().trim();
  if (res.error) throw new Error(`进程异常: ${res.error.message}`);
  if (res.status !== 0) throw new Error(`退出码 ${res.status}\n${err || out}`);
  return out;
}

async function pushplusAlert(title, msg) {
  if (!cfg.pushplusToken) {
    console.warn("[warn] pushplusToken 未配置，跳过告警");
    return;
  }
  try {
    const res = await fetch("https://www.pushplus.plus/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        token: cfg.pushplusToken,
        title,
        content: msg,
        template: "text"
      }),
      signal: AbortSignal.timeout(10_000)
    });
    const data = await res.json();
    if (data.code !== 200) console.warn("[warn] pushplus 推送失败:", data.msg);
  } catch (e) {
    console.warn("[warn] pushplus 网络异常:", e.message);
  }
}

export async function main() {
  // 1. 生成海报
  console.log("[1/3] 生成海报...");
  const posterOut = runScript("python3", ["tools/gen-poster.py"]);
  console.log("  ", posterOut);

  const posterPath = `${ROOT}data/poster.jpg`;
  let posterBuffer;
  try {
    posterBuffer = readFileSync(posterPath);
  } catch {
    throw new Error("海报文件未生成: data/poster.jpg");
  }
  if (posterBuffer.length < 1000) throw new Error("海报文件过小，可能无效");

  // 2. 生成文案
  console.log("[2/3] 生成文案...");
  const textOut = runScript("node", ["tools/gen-daily.js"]);
  const textLines = textOut.split("\n");
  const text = textLines.find(l => l.startsWith("【今日上新】"));
  if (!text) {
    console.log("  今日无新上内容，跳过发文");
    return { skipped: true, reason: "no_new_movies" };
  }
  console.log("  文案:", text.slice(0, 60) + "...");

  // 3. 发微博
  console.log("[3/3] 发布微博...");
  const result = await postWithPic(text, posterBuffer);
  console.log("  已发布, id:", result.idstr);

  return { success: true, id: result.idstr, text };
}

// 被直接运行时执行
if (process.argv[1] && process.argv[1].endsWith("lib/post.js")) {
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
      await pushplusAlert("popvideos 微博发文失败", e.message);
      process.exit(1);
    });
}