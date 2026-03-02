import json
import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class TopicDiscovery:
    """选题发现模块 - 从多个平台搜索热门内容"""

    def __init__(self):
        # 支持的平台名称映射 (别名 -> 实际方法名)
        self.platform_aliases = {
            'wechat': 'wechat',
            'x': 'x',
            'twitter': 'x',
            'xiaohongshu': 'xiaohongshu',
            'xhs': 'xiaohongshu',  # 支持 xhs 作为xiaohongshu的别名
            'reddit': 'reddit'
        }
        self.platforms = {
            'wechat': self.search_wechat,
            'x': self.search_x,
            'xiaohongshu': self.search_xiaohongshu,
            'reddit': self.search_reddit
        }
        # 动态日期（当前日期用于mock数据）
        self._today = datetime.now()

    def search_wechat(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        搜索微信公众号内容
        需要配置 WECHAT_SEARCH_API 环境变量或使用模拟数据
        """
        # TODO: 实现真实的微信搜索API调用
        # 可以使用微信搜索接口或第三方服务
        # 返回格式: [{title, summary, publish_time, source, url, engagement}]
        return self._mock_search('wechat', keyword, limit)

    def search_x(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        搜索X/T 需要配置 TWwitter内容
       ITTER_API_KEY 环境变量
        """
        # TODO: 实现真实的Twitter API调用
        # 使用Twitter API v2搜索推文
        # 返回格式: [{title, content, publish_time, author, url, engagement}]
        return self._mock_search('x', keyword, limit)

    def search_xiaohongshu(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        搜索小红书内容
        需要配置 XHS_API_KEY 环境变量
        """
        # TODO: 实现真实的小红书搜索API调用
        # 可以使用小红书开放API或网页爬取
        # 返回格式: [{title, content, likes, comments,收藏数}]
        return self._mock_search('xiaohongshu', keyword, limit)

    def search_reddit(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        搜索Reddit内容
        需要配置 REDDIT_API_KEY 环境变量
        """
        # TODO: 实现真实的Reddit API调用
        # 使用Reddit API搜索帖子
        # 返回格式: [{title, content, publish_time, subreddit, upvotes}]
        return self._mock_search('reddit', keyword, limit)

    def _mock_search(self, platform: str, keyword: str, limit: int) -> List[Dict]:
        """模拟搜索结果 - 用于测试和开发（动态日期）"""
        # 动态生成日期
        d = self._today
        mock_data = {
            'wechat': [
                {
                    'platform': 'wechat',
                    'title': f'{keyword}最新趋势分析',
                    'summary': '深度解析行业发展方向和未来趋势...',
                    'publish_time': (d - timedelta(days=3)).strftime('%Y-%m-%d'),
                    'source': '科技前沿',
                    'url': f'https://mp.weixin.qq.com/s/example1',
                    'engagement': {'likes': 520, 'comments': 45}
                },
                {
                    'platform': 'wechat',
                    'title': f'{keyword}使用指南',
                    'summary': '手把手教你快速上手...',
                    'publish_time': (d - timedelta(days=7)).strftime('%Y-%m-%d'),
                    'source': '技术社区',
                    'url': f'https://mp.weixin.qq.com/s/example2',
                    'engagement': {'likes': 380, 'comments': 28}
                }
            ],
            'x': [
                {
                    'platform': 'x',
                    'title': f'{keyword}热点讨论 #1',
                    'content': '关于这个话题的深度讨论...',
                    'publish_time': (d - timedelta(days=2)).strftime('%Y-%m-%d'),
                    'author': '@tech_expert',
                    'url': 'https://twitter.com/example1',
                    'engagement': {'likes': 890, 'comments': 120}
                }
            ],
            'xiaohongshu': [
                {
                    'platform': 'xiaohongshu',
                    'title': f'{keyword}真实使用体验',
                    'content': '姐妹们，真的太好用了！',
                    'publish_time': (d - timedelta(days=1)).strftime('%Y-%m-%d'),
                    'author': '用户昵称',
                    'likes': 2340,
                    'comments': 156,
                    '收藏数': 890,
                    'url': 'https://www.xiaohongshu.com/explore/example1'
                }
            ],
            'reddit': [
                {
                    'platform': 'reddit',
                    'title': f'[Discussion] {keyword} - 社区讨论',
                    'content': '欢迎大家分享自己的看法...',
                    'publish_time': (d - timedelta(days=5)).strftime('%Y-%m-%d'),
                    'subreddit': f'r/{keyword}',
                    'upvotes': 456,
                    'url': 'https://reddit.com/r/example'
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
        if platforms is None:
            platforms = list(self.platform_aliases.keys())

        results = []
        for platform in platforms:
            # 解析平台别名
            actual_platform = self.platform_aliases.get(platform)
            if not actual_platform:
                print(f"[TopicDiscovery] Unknown platform: {platform}, skipping")
                continue

            if actual_platform not in self.platforms:
                print(f"[TopicDiscovery] Platform not implemented: {actual_platform}, skipping")
                continue

            try:
                platform_results = self.platforms[actual_platform](keyword, limit)
                # 统一平台标识
                for r in platform_results:
                    r['platform'] = actual_platform
                results.extend(platform_results)
            except Exception as e:
                print(f"搜索{platform}失败: {e}")

        return results


if __name__ == "__main__":
    # 测试代码
    discovery = TopicDiscovery()
    results = discovery.search("AI工具", platforms=['wechat', 'xiaohongshu'], limit=5)
    print(json.dumps(results, ensure_ascii=False, indent=2))
