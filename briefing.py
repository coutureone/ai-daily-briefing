#!/usr/bin/env python3
"""
AI Daily Briefing Generator
为 AI/Web3 自媒体创作者生成每日早报

数据源：
- TechCrunch AI 分类
- CoinDesk 加密货币新闻
- TechCrunch Venture 分类
- GitHub Trending

作者：Rion Wu
GitHub: https://github.com/Rion-Wu-tech/ai-daily-briefing
"""

import os
import sys
import json
import yaml
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin
from zoneinfo import ZoneInfo
import requests
from bs4 import BeautifulSoup


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
                'ai_news': 'https://techcrunch.com/category/artificial-intelligence/',
                'ai_news_rss': 'https://techcrunch.com/category/artificial-intelligence/feed/',
                'web3_news': 'https://www.coindesk.com/',
                'web3_news_rss': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
                'venture_news': 'https://techcrunch.com/category/venture/',
                'venture_news_rss': 'https://techcrunch.com/category/venture/feed/',
                'github_trending': 'https://github.com/trending'
            },
            'output': {
                'format': 'text',
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
    
    def fetch_ai_news(self, limit: int = 10) -> List[Dict]:
        """抓取 AI 热点新闻"""
        print("📡 正在抓取 AI 热点...")
        url = self.config['sources']['ai_news']
        
        try:
            rss_url = self.config['sources'].get('ai_news_rss')
            if rss_url:
                articles = self._fetch_rss(rss_url, 'TechCrunch', limit)
                print(f"✅ 获取到 {len(articles)} 条 AI 新闻")
                return articles

            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            items = soup.select('article')[:limit]
            
            for item in items:
                title_elem = item.select_one('h2 a, h3 a, h4 a')
                time_elem = item.select_one('time')
                
                if title_elem:
                    articles.append({
                        'title': title_elem.get_text(strip=True),
                        'url': urljoin(url, title_elem.get('href', '')),
                        'time': time_elem.get_text(strip=True) if time_elem else 'N/A',
                        'source': 'TechCrunch'
                    })
            
            print(f"✅ 获取到 {len(articles)} 条 AI 新闻")
            return articles
            
        except Exception as e:
            print(f"❌ 抓取 AI 新闻失败: {e}")
            return []
    
    def fetch_web3_news(self, limit: int = 3) -> List[Dict]:
        """抓取 Web3 热点新闻"""
        print("📡 正在抓取 Web3 热点...")
        url = self.config['sources']['web3_news']
        
        try:
            rss_url = self.config['sources'].get('web3_news_rss')
            if rss_url:
                articles = self._fetch_rss(rss_url, 'CoinDesk', limit)
                for article in articles:
                    article['sentiment'] = 'Neutral'
                print(f"✅ 获取到 {len(articles)} 条 Web3 新闻")
                return articles

            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            # CoinDesk 的结构可能需要根据实际页面调整
            items = soup.select('article')[:limit]
            
            for item in items:
                title_elem = item.select_one('h3, h2')
                
                if title_elem:
                    articles.append({
                        'title': title_elem.get_text(strip=True),
                        'source': 'CoinDesk',
                        'sentiment': 'Neutral'  # 默认中性
                    })
            
            print(f"✅ 获取到 {len(articles)} 条 Web3 新闻")
            return articles
            
        except Exception as e:
            print(f"❌ 抓取 Web3 新闻失败: {e}")
            return []
    
    def fetch_venture_news(self, limit: int = 5) -> List[Dict]:
        """抓取投资经济新闻"""
        print("📡 正在抓取投资经济新闻...")
        url = self.config['sources']['venture_news']
        
        try:
            rss_url = self.config['sources'].get('venture_news_rss')
            if rss_url:
                articles = self._fetch_rss(rss_url, 'TechCrunch', limit)
                print(f"✅ 获取到 {len(articles)} 条投资新闻")
                return articles

            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            items = soup.select('article')[:limit]
            
            for item in items:
                title_elem = item.select_one('h2 a, h3 a, h4 a')
                time_elem = item.select_one('time')
                
                if title_elem:
                    articles.append({
                        'title': title_elem.get_text(strip=True),
                        'url': urljoin(url, title_elem.get('href', '')),
                        'time': time_elem.get_text(strip=True) if time_elem else 'N/A',
                        'source': 'TechCrunch'
                    })
            
            print(f"✅ 获取到 {len(articles)} 条投资新闻")
            return articles
            
        except Exception as e:
            print(f"❌ 抓取投资新闻失败: {e}")
            return []
    
    def fetch_github_trending(self, limit: int = 10) -> List[Dict]:
        """抓取 GitHub Trending 项目"""
        print("📡 正在抓取 GitHub Trending...")
        url = self.config['sources']['github_trending']
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            projects = []
            items = soup.select('article.Box-row')[:limit]
            
            for item in items:
                repo_elem = item.select_one('h2 a')
                desc_elem = item.select_one('p')
                lang_elem = item.select_one('[itemprop="programmingLanguage"]')
                stars_elem = item.select_one('a[href*="/stargazers"]')
                today_stars_elem = item.select_one('.float-sm-right')
                
                if repo_elem:
                    repo_name = repo_elem.get('href', '').strip('/')
                    projects.append({
                        'name': repo_name,
                        'description': desc_elem.get_text(strip=True) if desc_elem else '',
                        'language': lang_elem.get_text(strip=True) if lang_elem else 'Unknown',
                        'stars': stars_elem.get_text(strip=True) if stars_elem else '0',
                        'today_stars': today_stars_elem.get_text(strip=True) if today_stars_elem else '',
                        'url': f"https://github.com/{repo_name}"
                    })
            
            print(f"✅ 获取到 {len(projects)} 个 GitHub 项目")
            return projects
            
        except Exception as e:
            print(f"❌ 抓取 GitHub Trending 失败: {e}")
            return []
    
    def generate_topics(self, ai_news: List[Dict], web3_news: List[Dict], 
                       venture_news: List[Dict], github_projects: List[Dict]) -> List[str]:
        """生成选题素材"""
        topics = []
        
        # 基于热点新闻生成选题
        if ai_news:
            topics.append(f"「{ai_news[0]['title'][:20]}...」深度解析")
        
        if web3_news:
            topics.append(f"「Web3 周报」{web3_news[0]['title'][:20]}等热点事件")
        
        if github_projects:
            topics.append(f"「GitHub 周刊」{github_projects[0]['name']} 等优质开源项目推荐")
        
        # 补充通用选题
        topics.append("「AI 工具测评」本周最值得关注的 5 个 AI 工具")
        topics.append("「行业观察」AI/Web3 领域的最新趋势和机会")
        
        return topics[:5]
    
    def format_output(self, ai_news: List[Dict], web3_news: List[Dict],
                     venture_news: List[Dict], github_projects: List[Dict],
                     topics: List[str]) -> str:
        """格式化输出"""
        today = datetime.now()
        weekday_map = {
            'Monday': '周一', 'Tuesday': '周二', 'Wednesday': '周三',
            'Thursday': '周四', 'Friday': '周五', 'Saturday': '周六', 'Sunday': '周日'
        }
        weekday = weekday_map.get(today.strftime('%A'), '')
        date_str = today.strftime(f'%Y.%m.%d {weekday}')
        
        output = f"### 🌅 Rion 每日早报 · {date_str}\n\n"

        output += self._format_news_section("🤖 AI 热点", ai_news)
        output += self._format_news_section("🔗 Web3 热点", web3_news, show_sentiment=True)
        output += self._format_news_section("💰 投资 & 经济", venture_news)
        output += self._format_github_section(github_projects)
        output += self._format_topics_section(topics)
        output += f"---\n🕐 {today.strftime('%Y.%m.%d')} 早报完毕"
        
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

    def _format_github_section(self, projects: List[Dict]) -> str:
        output = "#### ⭐ GitHub 优质项目\n\n"
        if not projects:
            return output + "> 今日暂未抓到 GitHub Trending 项目。\n\n"

        for i, proj in enumerate(projects, 1):
            description = proj['description'] or '暂无简介'
            today_stars = f" | {proj['today_stars']}" if proj.get('today_stars') else ''
            output += f"{i}. **[{proj['name']}]({proj['url']})**\n\n"
            output += f"   语言：{proj['language']} | ⭐ {proj['stars']}{today_stars}\n\n"
            output += f"   {description}\n\n"

        return output

    def _format_topics_section(self, topics: List[str]) -> str:
        output = "#### 💡 今日选题素材\n\n"
        for i, topic in enumerate(topics, 1):
            output += f"{i}. {topic}\n\n"
        return output
    
    def generate(self) -> str:
        """生成完整早报"""
        print("🚀 开始生成每日早报...\n")
        
        # 抓取各类数据
        ai_news = self.fetch_ai_news(10)
        web3_news = self.fetch_web3_news(3)
        venture_news = self.fetch_venture_news(5)
        github_projects = self.fetch_github_trending(10)
        
        # 生成选题
        topics = self.generate_topics(ai_news, web3_news, venture_news, github_projects)
        
        # 格式化输出
        output = self.format_output(ai_news, web3_news, venture_news, github_projects, topics)
        
        print("\n✅ 早报生成完成！\n")
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
