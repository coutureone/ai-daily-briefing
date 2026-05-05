---
name: daily-briefing
description: 为 Rion 生成每日早报。涵盖 AI 热点、Web3 动态、投资经济、GitHub 优质项目、选题素材五个板块。适合 AI/Web3 自媒体创作者。
tags: [daily, briefing, news, ai, web3, github, rion]
---

# 每日早报生成流程

## 触发条件
- 用户说"给我今日早报"、"早报"、"daily briefing"
- Cron job 定时推送

## 重要经验

**不要用 delegate_task** — 曾因超时（43秒后中断）失败。直接用 browser 工具逐站抓取。

**日期星期必须严格校验** — 曾犯错把周日写成周六（2026-04-12）。生成标题时，必须根据实际日期计算星期几，不能靠猜测或惯性填写。可用 `date +%A` 或 Python `datetime.weekday()` 验证。中文星期对照：Monday=周一、Tuesday=周二、Wednesday=周三、Thursday=周四、Friday=周五、Saturday=周六、Sunday=周日。

## 数据来源（按顺序抓取）

1. **AI 热点** → https://techcrunch.com/category/artificial-intelligence/
   - 取最近 10 条 AI 相关新闻标题 + 时间 + 摘要

2. **Web3 热点** → https://www.coindesk.com/
   - 取首页 Latest Crypto News 中最新 3 条，带情绪标签（Positive/Negative/Neutral）

3. **投资 & 经济** → https://techcrunch.com/category/venture/
   - 取最近 5 条融资/投资相关新闻

4. **GitHub 优质项目** → https://github.com/trending
   - 取今日 Trending 前 10 个，记录：名称、语言、Stars、今日新增、一句话介绍
   - scroll down 一次获取更多项目

5. **选题素材** — 根据以上热点，人工合成 5 个选题建议

## 输出格式（纯文本，不用 Markdown，因为是 Telegram）

```
==== 🌅 Rion 每日早报 · YYYY.MM.DD ====

━━━━━━━━━━━━━━━━━━
🤖 AI 热点（10条）
━━━━━━━━━━━━━━━━━━

1. [标题]
来源：[来源] | [时间]
[1-2句摘要]

...（共10条）

━━━━━━━━━━━━━━━━━━
🔗 Web3 热点（3条）
━━━━━━━━━━━━━━━━━━

1. [标题]
来源：CoinDesk | [时间]
[1-2句摘要]

...（共3条）

━━━━━━━━━━━━━━━━━━
💰 投资 & 经济（5条）
━━━━━━━━━━━━━━━━━━

1. [标题]
来源：[来源] | [时间]
[1-2句摘要]

...（共5条）

━━━━━━━━━━━━━━━━━━
⭐ GitHub 优质项目（10条）
━━━━━━━━━━━━━━━━━━

1. owner/repo-name
语言：[语言] | ⭐ [总Stars] | 今日新增 [N]
[一句话介绍]

...（共10条）

━━━━━━━━━━━━━━━━━━
💡 今日选题素材（5个）
━━━━━━━━━━━━━━━━━━

1. 「[选题标题]」
热点：[关联热点] → [一句话说明为何适合创作]

...（共5个）

━━━━━━━━━━━━━━━━━━
🕐 YYYY.MM.DD 早报完毕
━━━━━━━━━━━━━━━━━━
```

## 选题素材原则
- 结合当天最热点事件
- 角度要适合 AI/Web3 中文自媒体受众
- 可以带澳洲/华人视角
- 有对比测评、科普、争议性话题优先

## Cron Job 信息
- Job ID: 2a069af47d3e
- 名称: Rion每日早报
- 模型: anthropic/claude-haiku-4-5
- 定时: 每天 21:00 (UTC+10，即 AEDT 早上 8:00)
- 推送: origin (Telegram)
