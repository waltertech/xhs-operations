"""
选题发现模块 - 从多个平台搜索热门内容

支持平台：
- 微信公众号 (wechat)
- X/Twitter (x/twitter)
- 小红书 (xiaohongshu/xhs)
- Reddit (reddit)

使用方法：
    from scripts.topic_discovery import TopicDiscovery
    
    discovery = TopicDiscovery()
    results = discovery.search("AI工具", platforms=["wechat", "xiaohongshu"])
"""
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 尝试导入新的API模块
try:
    from .xiaohongshu_search import XiaohongshuSearchAPI
    from .wechat_search import WeChatSearchAPI
    XHS_API_AVAILABLE = True
    WECHAT_API_AVAILABLE = True
except ImportError:
    XHS_API_AVAILABLE = False
    WECHAT_API_AVAILABLE = False
    logger.warning("新API模块不可用，使用旧版模拟实现")


class TopicDiscovery:
    """选题发现模块 - 从多个平台搜索热门内容"""

    def __init__(self, use_real_api: bool = False):
        """
        初始化选题发现模块
        
        Args:
            use_real_api: 是否尝试使用真实API (需要安装依赖)
        """
        # 平台别名映射
        self.platform_aliases = {
            'wechat': 'wechat',
            'x': 'x',
            'twitter': 'x',
            'xiaohongshu': 'xiaohongshu',
            'xhs': 'xiaohongshu',
            'reddit': 'reddit'
        }
        
        self.use_real_api = use_real_api
        self._today = datetime.now()
        
        # 初始化平台搜索方法
        self.platforms = {
            'wechat': self._search_wechat,
            'x': self._search_x,
            'xiaohongshu': self._search_xiaohongshu,
            'reddit': self._search_reddit
        }
        
        # 尝试初始化真实API
        if use_real_api:
            self._init_real_apis()
    
    def _init_real_apis(self):
        """初始化真实API客户端"""
        if XHS_API_AVAILABLE:
            try:
                self.xhs_api = XiaohongshuSearchAPI(mock_mode=not self.use_real_api)
                logger.info("小红书API已初始化")
            except Exception as e:
                logger.warning(f"小红书API初始化失败: {e}")
        
        if WECHAT_API_AVAILABLE:
            try:
                self.wechat_api = WeChatSearchAPI(mock_mode=not self.use_real_api)
                logger.info("微信公众号API已初始化")
            except Exception as e:
                logger.warning(f"微信公众号API初始化失败: {e}")

    def _search_wechat(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        搜索微信公众号内容
        
        Args:
            keyword: 搜索关键词
            limit: 返回数量
            
        Returns:
            文章列表
        """
        logger.info(f"搜索微信公众号: {keyword}")
        
        if self.use_real_api and WECHAT_API_AVAILABLE:
            try:
                results = self.wechat_api.search(keyword, limit)
                logger.info(f"微信公众号搜索完成，找到 {len(results)} 条结果")
                return results
            except Exception as e:
                logger.warning(f"微信公众号搜索失败: {e}，使用模拟数据")
        
        # 使用模拟数据
        return self._mock_search('wechat', keyword, limit)

    def _search_x(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        搜索X/Twitter内容
        
        Args:
            keyword: 搜索关键词
            limit: 返回数量
            
        Returns:
            推文列表
        """
        logger.info(f"搜索Twitter/X: {keyword}")
        
        # Twitter API需要OAuth，这里使用模拟数据
        # 如需真实API，可以使用tweepy库
        return self._mock_search('x', keyword, limit)

    def _search_xiaohongshu(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        搜索小红书内容
        
        Args:
            keyword: 搜索关键词
            limit: 返回数量
            
        Returns:
            笔记列表
        """
        logger.info(f"搜索小红书: {keyword}")
        
        if self.use_real_api and XHS_API_AVAILABLE:
            try:
                results = self.xhs_api.search(keyword, limit)
                logger.info(f"小红书搜索完成，找到 {len(results)} 条结果")
                return results
            except Exception as e:
                logger.warning(f"小红书搜索失败: {e}，使用模拟数据")
        
        # 使用模拟数据
        return self._mock_search('xiaohongshu', keyword, limit)

    def _search_reddit(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        搜索Reddit内容
        
        Args:
            keyword: 搜索关键词
            limit: 返回数量
            
        Returns:
            帖子列表
        """
        logger.info(f"搜索Reddit: {keyword}")
        
        # Reddit API可以使用 praw 库，这里使用模拟数据
        return self._mock_search('reddit', keyword, limit)

    def _mock_search(self, platform: str, keyword: str, limit: int) -> List[Dict]:
        """
        模拟搜索结果 - 用于测试和开发
        
        Args:
            platform: 平台名称
            keyword: 搜索关键词
            limit: 返回数量
            
        Returns:
            模拟的搜索结果
        """
        d = self._today
        
        mock_data = {
            'wechat': [
                {
                    'platform': 'wechat',
                    'title': f'{keyword}最新趋势分析',
                    'summary': f'深度解析{keyword}行业发展方向和未来趋势，独家数据报告...',
                    'publish_time': (d - timedelta(days=3)).strftime('%Y-%m-%d'),
                    'source': '科技前沿',
                    'url': f'https://mp.weixin.qq.com/s/example1',
                    'engagement': {'likes': 520, 'comments': 45, 'read_estimate': 52000}
                },
                {
                    'platform': 'wechat',
                    'title': f'{keyword}使用指南',
                    'summary': f'手把手教你快速上手{keyword}，零基础入门教程...',
                    'publish_time': (d - timedelta(days=7)).strftime('%Y-%m-%d'),
                    'source': '技术社区',
                    'url': f'https://mp.weixin.qq.com/s_example2',
                    'engagement': {'likes': 380, 'comments': 28, 'read_estimate': 38000}
                },
                {
                    'platform': 'wechat',
                    'title': f'必看的{keyword}避坑指南',
                    'summary': f'总结了{keyword}的常见误区和避坑方法...',
                    'publish_time': (d - timedelta(days=5)).strftime('%Y-%m-%d'),
                    'source': '避坑联盟',
                    'url': f'https://mp.weixin.qq.com/s_example3',
                    'engagement': {'likes': 650, 'comments': 56, 'read_estimate': 65000}
                }
            ],
            'x': [
                {
                    'platform': 'x',
                    'title': f'{keyword}热点讨论 #1',
                    'content': f'关于{keyword}的深度讨论，行业专家观点分享...',
                    'publish_time': (d - timedelta(days=2)).strftime('%Y-%m-%d'),
                    'author': '@tech_expert',
                    'url': 'https://twitter.com/example1',
                    'engagement': {'likes': 890, 'comments': 120}
                },
                {
                    'platform': 'x',
                    'title': f'{keyword}最新动态',
                    'content': f'{keyword}领域传来重大消息，圈内沸腾...',
                    'publish_time': (d - timedelta(days=1)).strftime('%Y-%m-%d'),
                    'author': '@industry_news',
                    'url': 'https://twitter.com/example2',
                    'engagement': {'likes': 1250, 'comments': 234}
                }
            ],
            'xiaohongshu': [
                {
                    'platform': 'xiaohongshu',
                    'note_id': 'mock_note_001',
                    'title': f'{keyword}真实使用体验分享',
                    'content': f'姐妹们，今天来聊聊我用了三个月的{keyword}...',
                    'publish_time': (d - timedelta(days=1)).strftime('%Y-%m-%d'),
                    'author': '爱分享的小姐姐',
                    'likes': 2340,
                    'comments': 156,
                    'collects': 890,
                    'topics': [f'#{keyword}', '#种草分享'],
                    'url': 'https://www.xiaohongshu.com/explore/mock001'
                },
                {
                    'platform': 'xiaohongshu',
                    'note_id': 'mock_note_002',
                    'title': f'私藏！{keyword}必备清单',
                    'content': f'这些都是我压箱底的宝贝，推荐给姐妹们～',
                    'publish_time': (d - timedelta(days=2)).strftime('%Y-%m-%d'),
                    'author': '种草达人',
                    'likes': 4560,
                    'comments': 289,
                    'collects': 1200,
                    'topics': [f'#{keyword}', '#好物推荐'],
                    'url': 'https://www.xiaohongshu.com/explore/mock002'
                }
            ],
            'reddit': [
                {
                    'platform': 'reddit',
                    'title': f'[Discussion] {keyword} - 社区深度讨论',
                    'content': f'欢迎大家分享自己对{keyword}的看法和使用经验...',
                    'publish_time': (d - timedelta(days=5)).strftime('%Y-%m-%d'),
                    'subreddit': f'r/{keyword.replace(" ", "")}',
                    'upvotes': 456,
                    'comments_count': 123,
                    'url': 'https://reddit.com/r/example'
                },
                {
                    'platform': 'reddit',
                    'title': f'[Guide] {keyword}新手入门完全指南',
                    'content': f'从零开始学习{keyword}的完整指南...',
                    'publish_time': (d - timedelta(days=10)).strftime('%Y-%m-%d'),
                    'subreddit': f'r/{keyword.replace(" ", "")}',
                    'upvotes': 890,
                    'comments_count': 234,
                    'url': 'https://reddit.com/r/example2'
                }
            ]
        }

        results = mock_data.get(platform, [])
        return results[:limit]

    def search(self, keyword: str, platforms: Optional[List[str]] = None, limit: int = 10) -> List[Dict]:
        """
        主搜索方法
        
        Args:
            keyword: 搜索关键词
            platforms: 目标平台列表 (默认全部)
                       支持: wechat, x, twitter, xiaohongshu, xhs, reddit
            limit: 每个平台返回数量
            
        Returns:
            统一格式的选题列表
        """
        logger.info(f"开始选题发现搜索: keyword={keyword}, platforms={platforms}, limit={limit}")
        
        if platforms is None:
            platforms = list(self.platforms.keys())

        results = []
        seen_platforms = set()  # 去重跟踪

        for platform in platforms:
            # 解析平台别名
            actual_platform = self.platform_aliases.get(platform, platform)
            
            # 去重：同一实际平台只搜索一次
            if actual_platform in seen_platforms:
                logger.debug(f"跳过重复平台: {platform} -> {actual_platform}")
                continue
            seen_platforms.add(actual_platform)

            if actual_platform not in self.platforms:
                logger.warning(f"未知平台: {platform}")
                continue

            try:
                platform_results = self.platforms[actual_platform](keyword, limit)
                # 统一平台标识
                for r in platform_results:
                    r['platform'] = actual_platform
                results.extend(platform_results)
                logger.info(f"平台 {actual_platform} 搜索完成: {len(platform_results)} 条结果")
            except Exception as e:
                logger.error(f"搜索平台 {platform} 失败: {e}")

        logger.info(f"选题发现完成: 总计 {len(results)} 条结果")
        return results

    def search_all(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        搜索所有可用平台
        
        Args:
            keyword: 搜索关键词
            limit: 每个平台返回数量
            
        Returns:
            所有平台的搜索结果
        """
        return self.search(keyword, platforms=None, limit=limit)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python topic_discovery.py <关键词> [平台1,平台2...] [数量]")
        print("示例: python topic_discovery.py AI工具 wechat,xiaohongshu 5")
        sys.exit(1)
    
    keyword = sys.argv[1]
    platforms = sys.argv[2].split(',') if len(sys.argv) > 2 else None
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    # 尝试使用真实API
    use_real = os.getenv('USE_REAL_API', 'false').lower() == 'true'
    discovery = TopicDiscovery(use_real_api=use_real)
    
    results = discovery.search(keyword, platforms, limit)
    
    print(f"\n找到 {len(results)} 条选题:\n")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
