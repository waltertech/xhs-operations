import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class TopicFilter:
    """选题筛选模块 - 对选题进行综合评分排序"""

    def __init__(self):
        self.weights = {
            'hotness': 0.4,
            'differentiation': 0.3,
            'timeliness': 0.3
        }

    def calculate_hotness(self, topic: Dict) -> float:
        """
        计算热度分数
        热度 = (点赞 + 收藏 + 评论) / 归一化基准
        """
        # 尝试多种格式的互动数据
        engagement = topic.get('engagement', {})
        total = 0

        # 格式1: {likes: x, comments: y}
        if engagement:
            total += engagement.get('likes', 0)
            total += engagement.get('comments', 0)

        # 格式2: {likes: x, 收藏数: y}
        total += topic.get('likes', 0)
        total += topic.get('收藏数', 0)
        total += topic.get('comments', 0)

        # 格式3: upvotes (Reddit)
        total += topic.get('upvotes', 0)

        # 归一化到0-1 (假设10000为满分)
        return min(total / 10000, 1.0)

    def calculate_timeliness(self, topic: Dict) -> float:
        """
        计算时效性分数
        7天内为1.0，30天外为0
        """
        publish_time = topic.get('publish_time')
        if not publish_time:
            return 0.5

        try:
            # 尝试多种日期格式
            for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y/%m/%d']:
                try:
                    dt = datetime.strptime(str(publish_time), fmt)
                    days_ago = (datetime.now() - dt).days

                    if days_ago <= 7:
                        return 1.0
                    elif days_ago >= 30:
                        return 0.0
                    else:
                        return 1.0 - (days_ago - 7) / 23
                except ValueError:
                    continue

            # 无法解析日期
            return 0.5
        except Exception:
            return 0.5

    def calculate_differentiation(self, topic: Dict, existing_topics: List[Dict],
                                   all_topics: List[Dict] = None) -> float:
        """
        计算差异化分数
        与已有选题相似度越低，分数越高

        Args:
            topic: 当前选题
            existing_topics: 历史已有选题列表
            all_topics: 当前批次的所有选题（用于批次内差异化）
        """
        # 提取当前选题文本
        current_text = self._extract_text(topic)
        if not current_text.strip():
            return 0.5

        # 如果有历史选题，计算与历史的差异化
        if existing_topics:
            existing_texts = [self._extract_text(t) for t in existing_topics]
            try:
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform([current_text] + existing_texts)

                similarities = []
                for i in range(1, len(existing_texts) + 1):
                    sim = np.dot(tfidf_matrix[0], tfidf_matrix[i].T).toarray()[0][0]
                    similarities.append(sim)

                max_similarity = max(similarities) if similarities else 0
                return 1.0 - max_similarity
            except Exception:
                pass

        # 如果没有历史选题，但有当前批次选题，计算批次内差异化
        if all_topics and len(all_topics) > 1:
            other_topics = [t for t in all_topics if t is not topic]
            other_texts = [self._extract_text(t) for t in other_topics]

            try:
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform([current_text] + other_texts)

                similarities = []
                for i in range(1, len(other_texts) + 1):
                    sim = np.dot(tfidf_matrix[0], tfidf_matrix[i].T).toarray()[0][0]
                    similarities.append(sim)

                max_similarity = max(similarities) if similarities else 0
                return 1.0 - max_similarity
            except Exception:
                pass

        # 默认返回中等分数
        return 0.5

    def _extract_text(self, topic: Dict) -> str:
        """从选题中提取文本用于相似度计算"""
        texts = []

        # 标题
        if topic.get('title'):
            texts.append(topic['title'])

        # 内容/摘要
        if topic.get('content'):
            texts.append(topic['content'])
        if topic.get('summary'):
            texts.append(topic['summary'])

        return ' '.join(texts)

    def filter(self, topics: List[Dict], existing_topics: Optional[List[Dict]] = None) -> List[Dict]:
        """
        对选题列表进行综合评分排序

        Args:
            topics: 待筛选的选题列表
            existing_topics: 已有选题列表(用于差异化计算)

        Returns:
            按综合分数排序的选题列表
        """
        if existing_topics is None:
            existing_topics = []

        scored_topics = []
        for topic in topics:
            hotness = self.calculate_hotness(topic)
            timeliness = self.calculate_timeliness(topic)
            # 传入所有topics用于批次内差异化计算
            differentiation = self.calculate_differentiation(topic, existing_topics, topics)

            total = (
                hotness * self.weights['hotness'] +
                differentiation * self.weights['differentiation'] +
                timeliness * self.weights['timeliness']
            )

            scored_topics.append({
                'original_data': topic,
                'scores': {
                    'hotness': round(hotness, 2),
                    'differentiation': round(differentiation, 2),
                    'timeliness': round(timeliness, 2)
                },
                'total_score': round(total, 2)
            })

        # 按总分降序排列
        return sorted(scored_topics, key=lambda x: x['total_score'], reverse=True)


if __name__ == "__main__":
    # 测试代码
    filter = TopicFilter()

    test_topics = [
        {
            'platform': 'wechat',
            'title': 'AI工具最新趋势分析',
            'summary': '深度解析行业发展方向...',
            'publish_time': '2024-01-15',
            'engagement': {'likes': 520, 'comments': 45}
        },
        {
            'platform': 'xiaohongshu',
            'title': 'AI工具真实使用体验',
            'content': '姐妹们，真的太好用了！',
            'publish_time': '2024-01-20',
            'likes': 2340,
            'comments': 156,
            '收藏数': 890
        }
    ]

    results = filter.filter(test_topics)
    print(json.dumps(results, ensure_ascii=False, indent=2))
