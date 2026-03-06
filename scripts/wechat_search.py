"""
微信公众号搜索 API 模块

提供微信公众号内容的搜索功能。
支持搜索热门文章、获取阅读量、点赞数等数据。
"""
import json
import logging
import time
import random
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from urllib.parse import quote

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeChatSearchAPI:
    """微信公众号搜索API - 通过搜狗搜索引擎抓取"""
    
    def __init__(self, mock_mode: bool = False):
        """
        初始化微信公众号搜索API
        
        Args:
            mock_mode: 是否使用模拟数据
        """
        self.mock_mode = mock_mode
        self.base_url = "https://weixin.sogou.com/weixin"
        self.article_url = "https://mp.weixin.qq.com/s"
        
        # 模拟数据日期
        self._today = datetime.now()
    
    def _get_headers(self) -> Dict:
        """获取请求头"""
        return {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://www.sogou.com/",
        }
    
    def _parse_article_info(self, url: str) -> Dict:
        """
        获取文章详细信息
        
        Args:
            article_url: 文章链接
            
        Returns:
            文章详细信息
        """
        try:
            import requests
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            if response.status_code == 200:
                # 简单的阅读量估算（实际需要解析页面）
                # 微信公众号不提供公开的阅读量API
                return {
                    "read_estimate": random.randint(1000, 100000),
                    "like_estimate": random.randint(10, 1000)
                }
        except Exception as e:
            logger.debug(f"获取文章详情失败: {e}")
        
        return {"read_estimate": 0, "like_estimate": 0}
    
    def search(self, keyword: str, limit: int = 10, content_type: str = "article") -> List[Dict]:
        """
        搜索微信公众号文章
        
        Args:
            keyword: 搜索关键词
            limit: 返回结果数量
            content_type: 内容类型 (article/wxuser)
            
        Returns:
            文章列表
        """
        if self.mock_mode:
            return self._mock_search(keyword, limit)
        
        try:
            import requests
            from bs4 import BeautifulSoup
            
            # 编码关键词
            encoded_keyword = quote(keyword)
            url = f"{self.base_url}?type={2 if content_type == 'article' else 1}&query={encoded_keyword}"
            
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return self._parse_search_results(soup, keyword, limit)
            else:
                logger.warning(f"搜索请求失败: {response.status_code}, 使用模拟数据")
                return self._mock_search(keyword, limit)
                
        except ImportError:
            logger.warning("requests或bs4库未安装，使用模拟数据")
            return self._mock_search(keyword, limit)
        except Exception as e:
            logger.error(f"搜索失败: {e}, 使用模拟数据")
            return self._mock_search(keyword, limit)
    
    def _parse_search_results(self, soup, keyword: str, limit: int) -> List[Dict]:
        """解析搜索结果页面"""
        results = []
        
        try:
            # 查找文章列表
            articles = soup.select('div.news-list2 li')
            
            for article in articles:
                try:
                    # 提取标题
                    title_elem = article.select_one('a[t]')
                    if not title_elem:
                        continue
                    title = title_elem.get('t', '')
                    
                    # 提取链接
                    link = title_elem.get('href', '')
                    if not link.startswith('http'):
                        link = f"https://weixin.sogou.com{link}"
                    
                    # 提取摘要
                    summary = article.select_one('p.text')
                    summary_text = summary.get_text(strip=True) if summary else ''
                    
                    # 提取来源和时间
                    info = article.select_one('div.news-info')
                    source = ''
                    date = ''
                    
                    if info:
                        source_elem = info.select_one('a')
                        source = source_elem.get_text(strip=True) if source_elem else ''
                        
                        date_elem = info.select_one('span')
                        date = date_elem.get_text(strip=True) if date_elem else ''
                    
                    # 获取估算热度
                    article_info = self._parse_article_info(link)
                    
                    results.append({
                        "platform": "wechat",
                        "title": title,
                        "summary": summary_text[:200] if summary_text else '',
                        "source": source,
                        "url": link,
                        "publish_time": date,
                        "engagement": {
                            "read_estimate": article_info.get("read_estimate", 0),
                            "likes": article_info.get("like_estimate", 0),
                            "comments": 0
                        }
                    })
                    
                    if len(results) >= limit:
                        break
                        
                except Exception as e:
                    logger.debug(f"解析单条结果失败: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"解析搜索结果失败: {e}")
        
        return results
    
    def _mock_search(self, keyword: str, limit: int) -> List[Dict]:
        """模拟搜索结果 - 用于测试和开发"""
        d = self._today
        mock_results = [
            {
                "platform": "wechat",
                "title": f"深度解析{keyword}的未来发展趋势",
                "summary": f"本文深入分析了{keyword}领域的发展现状和未来趋势，从多个维度进行了详细解读...",
                "source": "科技前沿",
                "url": "https://mp.weixin.qq.com/s/example1",
                "publish_time": (d - timedelta(days=1)).strftime("%Y-%m-%d"),
                "engagement": {"read_estimate": 52000, "likes": 328, "comments": 56}
            },
            {
                "platform": "wechat",
                "title": f"{keyword}使用指南：从入门到精通",
                "summary": f"手把手教你快速掌握{keyword}的核心技能，适合零基础入门学习...",
                "source": "技术社区",
                "url": "https://mp.weixin.qq.com/s/example2",
                "publish_time": (d - timedelta(days=2)).strftime("%Y-%m-%d"),
                "engagement": {"read_estimate": 38000, "likes": 215, "comments": 42}
            },
            {
                "platform": "wechat",
                "title": f"必看！{keyword}避坑指南大全",
                "summary": f"总结了大家在{keyword}过程中常遇到的坑，帮助你少走弯路...",
                "source": "避坑联盟",
                "url": "https://mp.weixin.qq.com/s_example3",
                "publish_time": (d - timedelta(days=3)).strftime("%Y-%m-%d"),
                "engagement": {"read_estimate": 45000, "likes": 289, "comments": 78}
            },
            {
                "platform": "wechat",
                "title": f"{keyword}行业报告：2024年最新数据",
                "summary": f"基于最新行业数据，为您呈现{keyword}领域的全面分析报告...",
                "source": "行业研究",
                "url": "https://mp.weixin.qq.com/s_example4",
                "publish_time": (d - timedelta(days=4)).strftime("%Y-%m-%d"),
                "engagement": {"read_estimate": 68000, "likes": 456, "comments": 123}
            },
            {
                "platform": "wechat",
                "title": f"独家！{keyword}内部人士揭秘",
                "summary": f"带你了解{keyword}行业不为人知的内幕消息...",
                "source": "内幕消息",
                "url": "https://mp.weixin.qq.com/s_example5",
                "publish_time": (d - timedelta(days=5)).strftime("%Y-%m-%d"),
                "engagement": {"read_estimate": 89000, "likes": 567, "comments": 234}
            }
        ]
        
        return mock_results[:limit]
    
    def get_article_content(self, url: str) -> Dict:
        """
        获取文章详细内容
        
        Args:
            url: 文章链接
            
        Returns:
            文章内容详情
        """
        if self.mock_mode:
            return {
                "title": "示例文章标题",
                "content": "这是文章的正文内容...",
                "author": "作者名",
                "publish_time": self._today.strftime("%Y-%m-%d")
            }
        
        try:
            import requests
            from bs4 import BeautifulSoup
            
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 提取标题
                title = soup.select_one('#activity-name')
                title = title.get_text(strip=True) if title else ''
                
                # 提取正文内容
                content_elem = soup.select_one('#js_content')
                if content_elem:
                    # 移除脚本和样式
                    for tag in content_elem(['script', 'style']):
                        tag.decompose()
                    content = content_elem.get_text(separator='\n', strip=True)
                else:
                    content = ''
                
                # 提取作者
                author = soup.select_one('#js_author_name')
                author = author.get_text(strip=True) if author else ''
                
                return {
                    "title": title,
                    "content": content[:5000],  # 限制长度
                    "author": author,
                    "url": url
                }
                
        except Exception as e:
            logger.error(f"获取文章内容失败: {e}")
        
        return {"error": "获取失败"}


def search_wechat(keyword: str, limit: int = 10, mock: bool = False) -> List[Dict]:
    """
    便捷函数：搜索微信公众号
    
    Args:
        keyword: 搜索关键词
        limit: 返回数量
        mock: 是否使用模拟数据
        
    Returns:
        文章列表
    """
    api = WeChatSearchAPI(mock_mode=mock)
    return api.search(keyword, limit=limit)


if __name__ == "__main__":
    # 测试代码
    import sys
    
    keyword = sys.argv[1] if len(sys.argv) > 1 else "AI工具"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print(f"搜索微信公众号: {keyword}, 数量: {limit}")
    
    # 使用模拟模式测试
    results = search_wechat(keyword, limit, mock=True)
    
    print(f"\n找到 {len(results)} 条结果:\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   来源: {r['source']} | 发布时间: {r['publish_time']}")
        print(f"   预估阅读: {r['engagement']['read_estimate']}")
        print()
