# AI Daily Briefing - 使用指南

## 📦 安装

### 方式一：作为 Hermes Skill

```bash
# 进入 Hermes skills 目录
cd ~/.hermes/skills/research

# 克隆仓库
git clone https://github.com/Rion-Wu-tech/ai-daily-briefing.git daily-briefing

# 在 Hermes 中使用
# 直接说："给我今日早报"
```

### 方式二：独立运行

```bash
# 克隆仓库
git clone https://github.com/Rion-Wu-tech/ai-daily-briefing.git
cd ai-daily-briefing

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行
python briefing.py
```

## ⚙️ 配置

编辑 `config.yaml` 自定义数据源和输出格式：

```yaml
sources:
  ai_news: "https://techcrunch.com/category/artificial-intelligence/"
  web3_news: "https://www.coindesk.com/"
  venture_news: "https://techcrunch.com/category/venture/"
  github_trending: "https://github.com/trending"

output:
  format: "text"  # text, markdown, json
  language: "zh"  # zh, en

limits:
  ai_news: 10
  web3_news: 3
  venture_news: 5
  github_projects: 10
  topics: 5
```

## 🔄 定时任务

### Hermes Cron Job

在 Hermes 中设置定时任务：

```bash
# 每天早上 8:00 自动生成并推送
hermes cron create "生成每日早报" --schedule "0 8 * * *" --skill daily-briefing
```

### Linux Cron

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天早上 8:00）
0 8 * * * cd ~/ai-daily-briefing && /path/to/python briefing.py
```

### Windows 任务计划程序

1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器：每天 8:00
4. 操作：启动程序 `python.exe`
5. 参数：`briefing.py`
6. 起始于：项目目录路径

## 📤 输出格式

### 文本格式（默认）

纯文本输出，适合 Telegram、微信等即时通讯工具。

### Markdown 格式

```yaml
output:
  format: "markdown"
```

生成带格式的 Markdown 文件，适合博客、公众号。

### JSON 格式

```yaml
output:
  format: "json"
```

结构化数据输出，方便二次开发和数据分析。

## 🔧 高级用法

### 自定义数据源

在 `briefing.py` 中添加新的数据源：

```python
def fetch_custom_news(self, limit: int = 5) -> List[Dict]:
    """抓取自定义新闻源"""
    url = "https://your-news-source.com"
    # 实现抓取逻辑
    return articles
```

### 集成到其他工具

```python
from briefing import DailyBriefing

# 创建实例
briefing = DailyBriefing()

# 生成早报
output = briefing.generate()

# 发送到 Telegram
# send_to_telegram(output)

# 发送邮件
# send_email(output)
```

## 🐛 常见问题

### 1. 抓取失败

**原因**：网站反爬虫、网络问题
**解决**：
- 检查网络连接
- 使用代理
- 调整 User-Agent

### 2. 数据不完整

**原因**：网站结构变化
**解决**：
- 更新 CSS 选择器
- 查看网站最新结构
- 提交 Issue

### 3. 编码问题

**原因**：系统编码设置
**解决**：
```bash
export PYTHONIOENCODING=utf-8
```

## 📝 贡献指南

欢迎提交 PR！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📧 联系方式

- GitHub: [@Rion-Wu-tech](https://github.com/Rion-Wu-tech)
- Email: rionwu98@gmail.com

## 📄 开源协议

MIT License - 详见 [LICENSE](LICENSE) 文件
