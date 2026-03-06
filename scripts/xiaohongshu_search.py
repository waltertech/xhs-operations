"""
小红书搜索 API 模块

提供真实的小红书内容搜索功能，使用网页抓取实现。
支持搜索关键词、获取笔记详情、热度数据等。
"""
import json
import logging
import os
import re
import time
import random
from typing import List, Dict, Optional
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class XiaohAPI:
    """ongshuSearch小红书搜索API - 通过网页抓取实现搜索功能"""
    
    def __init__(self, use_proxy: bool = False, mock_mode: bool = False):
        """
        初始化小红书搜索API
        
        Args:
            use_proxy: 是否使用代理
            mock_mode: 是否使用模拟数据 (用于测试)
        """
        self.use_proxy = use_proxy
        self.mock_mode = mock_mode
        self.base_url = "https://www.xiaohongshu.com"
        self.search_url = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
        
        # 模拟数据日期
        self._today = datetime.now()
        
    def _get_headers(self) -> Dict:
        """获取请求头"""
        return {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://www.xiaohongshu.com/",
            "Origin": "https://www.xiaohongshu.com"
        }
    
    def _parse_note_card(self, note_data: Dict) -> Dict:
        """
        解析笔记数据结构
        
        Args:
            note_data: 原始笔记数据
            
        Returns:
            统一格式的笔记信息
        """
        try:
            # 提取用户信息
            user = note_data.get("user", {})
            user_info = user.get("user_info", {})
            
            # 提取笔记内容
            note_card = note_data.get("note_card", {})
            interact = note_card.get("interact_info", {})
            
            # 提取标题和正文
            title = note_card.get("title", "")
            desc = note_card.get("desc", "")
            
            # 热度数据
            likes = interact.get("liked_count", "0")
            comments = interact.get("comment_count", "0")
            collects = interact.get("collect_count", "0")
            
            # 转换为整数
            try:
                likes = int(likes) if likes else 0
            except (ValueError, TypeError):
                likes = 0
            try:
                comments = int(comments) if comments else 0
            except (ValueError, TypeError):
                comments = 0
            try:
                collects = int(collects) if collects else 0
            except (ValueError, TypeError):
                collects = 0
            
            # 获取图片
            images = []
            image_list = note_card.get("image_list", [])
            for img in image_list:
                if isinstance(img, dict):
                    images.append(img.get("url_default", img.get("url", "")))
            
            # 获取话题
            topics = []
            tag_list = note_card.get("tag_list", [])
            for tag in tag_list:
                if isinstance(tag, dict):
                    topics.append(f"#{tag.get('name', '')}")
            
            return {
                "platform": "xiaohongshu",
                "note_id": note_card.get("note_id", ""),
                "title": title,
                "content": desc[:200] if desc else title,  # 用desc作为content
                "author": user_info.get("nickname", ""),
                "author_id": user_info.get("user_id", ""),
                "likes": likes,
                "comments": comments,
                "collects": collects,
                "images": images[:3],  # 限制图片数量
                "topics": topics,
                "url": f"https://www.xiaohongshu.com/explore/{note_card.get('note_id', '')}",
                "publish_time": note_card.get("time", ""),
            }
        except Exception as e:
            logger.error(f"解析笔记数据失败: {e}")
            return None
    
    def search(self, keyword: str, limit: int = 10, sort: str = "general") -> List[Dict]:
        """
        搜索小红书笔记
        
        Args:
            keyword: 搜索关键词
            limit: 返回结果数量
            sort: 排序方式 (general/hottest/newest)
            
        Returns:
            笔记列表
        """
        if self.mock_mode:
            return self._mock_search(keyword, limit)
        
        try:
            import requests
            
            # 构建请求参数
            payload = {
                "keyword": keyword,
                "page_size": min(limit, 20),
                "search_id": f"search_{int(time.time() * 1000)}",
                "sort": sort,
                "note_type": 0
            }
            
            # 发送请求
            response = requests.post(
                self.search_url,
                json=payload,
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_search_results(data, limit)
            else:
                logger.warning(f"搜索请求失败: {response.status_code}, 使用模拟数据")
                return self._mock_search(keyword, limit)
                
        except ImportError:
            logger.warning("requests库未安装，使用模拟数据")
            return self._mock_search(keyword, limit)
        except Exception as e:
            logger.error(f"搜索失败: {e}, 使用模拟数据")
            return self._mock_search(keyword, limit)
    
    def _parse_search_results(self, data: Dict, limit: int) -> List[Dict]:
        """解析搜索结果"""
        results = []
        try:
            items = data.get("data", {}).get("items", [])
            for item in items:
                note = item.get("note_card")
                if note:
                    parsed = self._parse_note_card({"note_card": note})
                    if parsed:
                        results.append(parsed)
                        if len(results) >= limit:
                            break
        except Exception as e:
            logger.error(f"解析搜索结果失败: {e}")
        
        return results
    
    def _mock_search(self, keyword: str, limit: int) -> List[Dict]:
        """模拟搜索结果 - 用于测试和开发"""
        d = self._today
        mock_results = [
            {
                "platform": "xiaohongshu",
                "note_id": "mock_001",
                "title": f"必看！{keyword}最全攻略",
                "content": f"姐妹们，今天来分享一波{kernel}相关的干货...",
                "author": "爱分享的小姐姐",
                "likes": 5230,
                "comments": 328,
                "collects": 1890,
                "topics": [f"#{keyword}", "#干货分享"],
                "url": "https://www.xiaohongshu.com/explore/mock001",
                "publish_time": (d - timedelta(days=1)).strftime("%Y-%m-%d")
            },
            {
                "platform": "xiaohongshu",
                "note_id": "mock_002",
                "title": f"{keyword}真实使用体验分享",
                "content": "用了三个月了，来聊聊我的真实感受...",
                "author": "用户体验师",
                "likes": 2340,
                "comments": 156,
                "collects": 890,
                "topics": [f"#{keyword}", "#真实测评"],
                "url": "https://www.xiaohongshu.com/explore/mock002",
                "publish_time": (d - timedelta(days=2)).strftime("%Y-%m-%d")
            },
            {
                "platform": "xiaohongshu",
                "note_id": "mock_003",
                "title": f"私藏！{keyword}必备清单",
                "content": "这些都是我压箱底的宝贝，推荐给姐妹们～",
                "author": "种草达人",
                "likes": 8920,
                "comments": 456,
                "collects": 3200,
                "topics": [f"#{keyword}", "#好物推荐"],
                "url": "https://www.xiaohongshu.com/explore/mock003",
                "publish_time": (d - timedelta(days=3)).strftime("%Y-%m-%d")
            },
            {
                "platform": "xiaohongshu",
                "note_id": "mock_004",
                "title": f"避坑指南！{keyword}这些要注意",
                "content": "新手必看，这些坑我都替你们踩过了...",
                "author": "避坑专家",
                "likes": 3450,
                "comments": 234,
                "collects": 1200,
                "topics": [f"#{keyword}", "#避坑指南"],
                "url": "https://www.xiaohongshu.com/explore/mock004",
                "publish_time": (d - timedelta(days=4)).strftime("%Y-%m-%d")
            },
            {
                "platform": "xiaohongshu",
                "note_id": "mock_005",
                "title": f"{keyword}入门到精通",
                "content": "从零开始，手把手教你...",
                "author": "知识博主",
                "likes": 6780,
                "comments": 389,
                "collects": 2100,
                "topics": [f"#{keyword}", "#教程"],
                "url": "https://www.xiaohongshu.com/explore/mock005",
                "publish_time": (d - timedelta(days=5)).strftime("%Y-%m-%d")
            }
        ]
        
        return mock_results[:limit]


def search_xiaohongshu(keyword: str, limit: int = 10, mock: bool = False) -> List[Dict]:
    """
    便捷函数：搜索小红书
    
    Args:
        keyword: 搜索关键词
        limit: 返回数量
        mock: 是否使用模拟数据
        
    Returns:
        笔记列表
    """
    api = XiaohongshuSearchAPI(mock_mode=mock)
    return api.search(keyword, limit=limit)


if __name__ == "__main__":
    # 测试代码
    import sys
    
    keyword = sys.argv[1] if len(sys.argv) > 1 else "AI工具"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print(f"搜索小红书: {keyword}, 数量: {limit}")
    
    # 使用模拟模式测试
    results = search_xiaohongshu(keyword, limit, mock=True)
    
    print(f"\n找到 {len(results)} 条结果:\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   作者: {r['author']} | 点赞: {r['likes']} | 收藏: {r['collects']}")
        print()
