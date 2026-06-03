# AI Daily Briefing 🌅

为 AI 自媒体创作者打造的中文每日早报生成工具。自动抓取中文 AI 热点资讯，并推送到钉钉群。

## ✨ 特性

- 🤖 **中文 AI 热点**：自动抓取量子位、InfoQ 中文等 RSS 源
- 🧹 **AI 关键词过滤**：只保留 AI、大模型、智能体、机器人等相关内容
- 📮 **钉钉推送**：通过 GitHub Actions 每天北京时间 08:00 自动推送

## 🚀 快速开始

### 方式一：作为 Hermes Agent Skill 使用（推荐）

如果你使用 [Hermes Agent](https://github.com/NousResearch/hermes)：

```bash
# 安装 skill
cd ~/.hermes/skills/research
git clone https://github.com/Rion-Wu-tech/ai-daily-briefing.git daily-briefing

# 使用
# 在 Hermes 中直接说："给我今日早报"
```

### 方式二：使用 Claude Code 生成简报

```bash
# 手动运行
claude --acp --stdio << 'EOF'
Load the daily-briefing skill and generate today's briefing for Rion
EOF

# 或通过 Hermes cron 定时运行（每天早上 8:30）
hermes cron create \
  --schedule "30 8 * * *" \
  --prompt "Load daily-briefing skill and generate today's briefing" \
  --acp-command claude \
  --acp-args "--acp,--stdio" \
  --deliver telegram
```

### 方式三：使用 Codex 生成简报

```bash
# 手动运行
codex --acp --stdio << 'EOF'
Load the daily-briefing skill and generate today's briefing for Rion
EOF

# 或通过 Hermes cron 定时运行（每天早上 8:30）
hermes cron create \
  --schedule "30 8 * * *" \
  --prompt "Load daily-briefing skill and generate today's briefing" \
  --acp-command codex \
  --acp-args "--acp,--stdio" \
  --deliver telegram
```

### 方式四：独立 Python 脚本

```bash
# 克隆仓库
git clone https://github.com/Rion-Wu-tech/ai-daily-briefing.git
cd ai-daily-briefing

# 安装依赖
pip install -r requirements.txt

# 运行
python briefing.py
```

> 💡 **更多运行方案**：查看 [DAILY_BRIEFING_SETUP.md](./DAILY_BRIEFING_SETUP.md) 了解完整的 Codex、Claude Code、混合方案等详细配置

## 📋 输出示例

```
### 🌅 AI 中文早报 · 2026.06.03 周三

#### 🤖 今日 AI 热点

1. **[OpenAI挖走中科大少年班校友！12岁上大学，哈佛史上最年轻正教授](https://www.qbitai.com/)**

   来源：量子位 | 06-02 22:54

---
🕐 2026.06.03 AI 早报完毕
```

## 🛠️ 配置

### Hermes Skill 配置

编辑 `SKILL.md` 中的 frontmatter：

```yaml
---
name: daily-briefing
description: 为 Rion 生成每日早报...
tags: [daily, briefing, news, ai, zh]
---
```

### 独立脚本配置

编辑 `config.yaml`：

```yaml
sources:
  ai_news_rss:
    - name: "量子位"
      url: "https://www.qbitai.com/feed"
    - name: "InfoQ 中文"
      url: "https://www.infoq.cn/feed"

output:
  format: "markdown"
  language: "zh"
```

## 📅 定时任务

### Hermes Cron Job

```bash
# 在 Hermes 中设置定时任务
# 每天早上 8:00 (AEDT) 自动推送
```

### Linux Cron

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天早上 8:00）
0 8 * * * cd ~/ai-daily-briefing && python briefing.py
```

### GitHub Actions + 钉钉群机器人

本仓库已包含 `.github/workflows/daily-dingtalk.yml`，会在每天北京时间 08:00 自动生成早报并发送到钉钉群，也支持在 GitHub Actions 页面手动运行。

配置步骤：

1. 在钉钉群中添加「自定义机器人」，复制 Webhook。
2. 安全设置建议选择「加签」，复制 Secret。
3. 在 GitHub 仓库中打开 `Settings -> Secrets and variables -> Actions`。
4. 添加仓库 Secret：
   - `DINGTALK_WEBHOOK`：钉钉机器人 Webhook
   - `DINGTALK_SECRET`：钉钉机器人加签 Secret；如果没有开启加签，可以不填
5. 打开 `Actions -> Daily DingTalk Briefing -> Run workflow` 手动测试一次。

GitHub Actions 的定时任务使用 UTC 时间；`0 0 * * *` 对应北京时间每天 08:00。

## 🎯 适用人群

- AI 自媒体创作者
- 科技内容创作者
- 需要每日科技资讯的从业者
- 想要快速了解行业动态的开发者

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发计划

- [ ] 支持更多数据源（Hacker News, Product Hunt）
- [ ] 支持自定义模板
- [ ] 添加邮件推送功能
- [ ] Web 界面
- [ ] 多语言支持

## 📄 开源协议

MIT License

## 👤 作者

**Rion Wu**
- X/Twitter: [@rionaifantasy]
- GitHub: [@Rion-Wu-tech](https://github.com/Rion-Wu-tech)

## 🙏 致谢

- [Hermes Agent](https://github.com/NousResearch/hermes) - 强大的 AI Agent 框架
- [量子位](https://www.qbitai.com/) - 中文 AI 新闻来源
- [InfoQ 中文](https://www.infoq.cn/) - 中文技术与 AI 新闻来源

---

如果这个项目对你有帮助，请给个 ⭐️ Star！
