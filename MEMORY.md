# MEMORY.md - 长期记忆

## 关于 Rion

- 00后，澳国立大学在读研究生，ADHD，i人
- AI/Web3 自媒体创作者，X 平台 10000+ 粉丝，月入 1w+ 商单
- 使用 WSL2 运行开发环境（Claude Code/Hermes/Codex），计划迁移到 Mac
- 时区：AEDT (UTC+11)

### 核心目标（2026）
- 实现财务自由，有稳定的被动收入
- 资产达到 7 位数
- 年收入 100w+ 人民币 / 20w+ 澳币

## 工作流程

### 内容创作
- 主要平台：X (Twitter)
- 内容方向：AI 技术、Web3、vibe coding
- 商单合作：文心、OKX 等

### 技术栈
- **AI Agent 工具链**：Hermes Agent v0.11.0、Claude Code、Codex
- **API 代理**：Codesome (https://cc.codesome.ai)
- **配置优化**：已完成 token 节省优化（reasoning_effort=none、smart_model_routing）

### 每日早报
结构：
1. AI 热点 10 条 + Web3 热点 3 条 + 投资经济 5 条
2. GitHub 优质项目 10 条（AI 优先 + 实用工具 + 干货教程）
3. 每日选题素材 5 个

信息源优先级：官方源 > 社区源 > 开发者源
输出格式：Telegram 纯文本（无 Markdown 表格）

## 已完成的重要任务

- 2026-03-29: 交学费
- 2026-03-30: 完成文心商单、6046 作业
- 2026-04-01: 完成 Xcrawl 推文
- 2026-04-09: 完成 OKX X 长文章
- 2026-04: 申请加入灯塔

## 技术经验

### Hermes 配置
- 修改 `config.yaml` 后需重启 gateway (`hermes gateway restart`)
- Telegram 会话需发送 `/restart` 或新消息才能更新工具实例
- `hermes doctor --fix` 可修复配置迁移问题
- 配置已从 v12 自动迁移到 v17

### 早报执行经验
- TechCrunch AI/Venture 分类页加载慢，超时可先访问主页再跳转
- CoinDesk 需关注 Latest Crypto News 板块的情绪标签
- GitHub Trending 需滚动一次获取完整 10 个项目

## 注意事项

- API Key 曾明文泄露，已提醒更换
- 日期相关内容需严格校验（曾出现周几错误）
- OKX 商单需定期补充内容（1-2 条），注意结算日

---

_最后更新: 2026-04-29_
