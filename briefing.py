#!/usr/bin/env python3
"""
AI Daily Briefing Generator
为 AI 自媒体创作者生成中文每日早报

数据源：
- 量子位
- InfoQ 中文

作者：Rion Wu
GitHub: https://github.com/Rion-Wu-tech/ai-daily-briefing
"""

import os
import yaml
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import List, Dict
from zoneinfo import ZoneInfo
import requests
from bs4 import BeautifulSoup


DEFAULT_AI_KEYWORDS = [
    'AI', '人工智能', '大模型', '模型', '智能体', 'Agent', 'OpenAI',
    'DeepSeek', 'Qwen', '千问', '机器人', '多模态', '自动驾驶',
    '英伟达', 'NVIDIA', '文心', '豆包', 'Claude', 'Codex',
]


class DailyBriefing:
    """每日早报生成器"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """初始化"""
        self.config = self._load_config(config_path)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return self._default_config()
    
    def _default_config(self) -> dict:
        """默认配置"""
        return {
            'sources': {
                'ai_news_rss': [
                    {'name': '量子位', 'url': 'https://www.qbitai.com/feed'},
                    {'name': 'InfoQ 中文', 'url': 'https://www.infoq.cn/feed'},
                ],
                'ai_keywords': DEFAULT_AI_KEYWORDS,
            },
            'output': {
                'format': 'markdown',
                'language': 'zh'
            }
        }

    def _fetch_rss(self, url: str, source: str, limit: int) -> List[Dict]:
        """Fetch recent articles from an RSS feed."""
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'xml')
        articles = []

        for item in soup.find_all('item')[:limit]:
            title_elem = item.find('title')
            link_elem = item.find('link')
            time_elem = item.find('pubDate')
            desc_elem = item.find('description')
            title = title_elem.get_text(strip=True) if title_elem else ''

            if not title:
                continue

            articles.append({
                'title': title,
                'url': link_elem.get_text(strip=True) if link_elem else '',
                'time': time_elem.get_text(strip=True) if time_elem else 'N/A',
                'summary': desc_elem.get_text(strip=True) if desc_elem else '',
                'source': source,
            })

        return articles

    def _format_article_time(self, value: str) -> str:
        """Shorten RSS timestamps for mobile-friendly display."""
        if not value or value == 'N/A':
            return 'N/A'
        try:
            parsed = parsedate_to_datetime(value)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=ZoneInfo('UTC'))
            return parsed.astimezone(ZoneInfo('Asia/Shanghai')).strftime('%m-%d %H:%M')
        except (TypeError, ValueError):
            return value.replace('GMT', '').strip()

    def _matches_ai_keywords(self, article: Dict) -> bool:
        keywords = self.config.get('sources', {}).get('ai_keywords') or DEFAULT_AI_KEYWORDS
        text = f"{article.get('title', '')} {article.get('summary', '')}"
        return any(keyword.lower() in text.lower() for keyword in keywords)
    
    def fetch_ai_news(self, limit: int = 10) -> List[Dict]:
        """抓取 AI 热点新闻"""
        print("📡 正在抓取 AI 热点...")
        sources = self.config['sources'].get('ai_news_rss', [])
        if isinstance(sources, str):
            sources = [{'name': 'AI 新闻', 'url': sources}]
        
        try:
            articles = []
            seen_urls = set()
            seen_titles = set()

            for source in sources:
                source_name = source.get('name', 'AI 新闻')
                rss_url = source.get('url')
                if not rss_url:
                    continue

                try:
                    fetched = self._fetch_rss(rss_url, source_name, limit * 2)
                except Exception as source_error:
                    print(f"⚠️ {source_name} 抓取失败: {source_error}")
                    continue

                for article in fetched:
                    title = article.get('title', '')
                    url = article.get('url', '')
                    if url in seen_urls or title in seen_titles:
                        continue
                    if not self._matches_ai_keywords(article):
                        continue

                    seen_urls.add(url)
                    seen_titles.add(title)
                    articles.append(article)

                    if len(articles) >= limit:
                        print(f"✅ 获取到 {len(articles)} 条中文 AI 新闻")
                        return articles

            print(f"✅ 获取到 {len(articles)} 条中文 AI 新闻")
            return articles

        except Exception as e:
            print(f"❌ 抓取 AI 新闻失败: {e}")
            return []

    def format_output(self, ai_news: List[Dict]) -> str:
        """格式化输出"""
        today = datetime.now()
        weekday_map = {
            'Monday': '周一', 'Tuesday': '周二', 'Wednesday': '周三',
            'Thursday': '周四', 'Friday': '周五', 'Saturday': '周六', 'Sunday': '周日'
        }
        weekday = weekday_map.get(today.strftime('%A'), '')
        date_str = today.strftime(f'%Y.%m.%d {weekday}')
        
        output = f"### 🌅 AI 中文早报 · {date_str}\n\n"

        output += self._format_news_section("🤖 今日 AI 热点", ai_news)
        output += f"---\n🕐 {today.strftime('%Y.%m.%d')} AI 早报完毕"
        
        return output

    def _format_news_section(self, title: str, articles: List[Dict], show_sentiment: bool = False) -> str:
        output = f"#### {title}\n\n"
        if not articles:
            return output + "> 今日暂未抓到有效内容，可能是源站结构或网络临时异常。\n\n"

        for i, news in enumerate(articles, 1):
            title_text = news['title']
            url = news.get('url', '')
            headline = f"[{title_text}]({url})" if url else title_text
            meta = f"来源：{news['source']} | {self._format_article_time(news.get('time', 'N/A'))}"
            if show_sentiment:
                meta += f" | {news.get('sentiment', 'Neutral')}"
            output += f"{i}. **{headline}**\n\n   {meta}\n\n"

        return output

    def generate(self) -> str:
        """生成完整早报"""
        print("🚀 开始生成 AI 中文早报...\n")
        
        # 只抓取中文 AI 新闻
        ai_news = self.fetch_ai_news(10)
        
        # 格式化输出
        output = self.format_output(ai_news)
        
        print("\n✅ AI 中文早报生成完成！\n")
        return output


def main():
    """主函数"""
    briefing = DailyBriefing()
    output = briefing.generate()
    
    # 输出到控制台
    print(output)
    
    # 保存到文件
    today = datetime.now().strftime('%Y-%m-%d')
    output_file = f"briefing_{today}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"📄 早报已保存到: {output_file}")


if __name__ == "__main__":
    main()
