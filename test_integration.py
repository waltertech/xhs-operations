#!/usr/bin/env python3
"""
小红书运营 Skill 集成测试

测试完整流程: 选题发现 -> 筛选 -> 内容撰写 -> 配图生成 -> 发布
"""

import sys
import os
import json

# 添加scripts目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from topic_discovery import TopicDiscovery
from topic_filter import TopicFilter
from image_designer import ImageDesigner
from publisher import XiaohongshuPublisher


def test_topic_discovery():
    """测试选题发现模块"""
    print("\n" + "="*50)
    print("测试1: 选题发现")
    print("="*50)

    discovery = TopicDiscovery()
    topics = discovery.search("AI工具", platforms=['wechat', 'xiaohongshu'], limit=3)

    print(f"✓ 发现 {len(topics)} 个选题")
    for topic in topics:
        print(f"  - [{topic['platform']}] {topic['title']}")

    return topics


def test_topic_filter(topics):
    """测试选题筛选模块"""
    print("\n" + "="*50)
    print("测试2: 选题筛选")
    print("="*50)

    filter = TopicFilter()
    filtered = filter.filter(topics)

    print(f"✓ 筛选后 {len(filtered)} 个选题 (按综合分数排序)")
    for item in filtered:
        print(f"  - {item['original_data']['title']}")
        print(f"    热度:{item['scores']['hotness']} 差异化:{item['scores']['differentiation']} 时效性:{item['scores']['timeliness']}")
        print(f"    总分: {item['total_score']}")

    return filtered


def test_image_designer():
    """测试配图生成模块"""
    print("\n" + "="*50)
    print("测试3: 配图生成")
    print("="*50)

    designer = ImageDesigner()

    # 测试HTML截图
    content = "<h1>AI工具推荐</h1><p>这5个神器让你的效率翻倍！</p>"
    html_img = designer.design(content, mode='html_screenshot', style='modern')
    print(f"✓ HTML截图生成: {len(html_img)} chars")

    # 测试AI生图
    ai_img = designer.design("a modern tech gadget on desk", mode='ai_gen', api='aliyun')
    print(f"✓ AI生图生成: {ai_img}")

    return html_img, ai_img


def test_publisher():
    """测试发布模块"""
    import unittest.mock as mock

    print("\n" + "="*50)
    print("测试4: 发布模块")
    print("==="*50)

    # 测试1: 无凭证且非mock模式，应返回失败
    # 使用mock隔离环境变量，确保测试稳定性
    print("\n测试4a: 无凭证非mock模式")
    with mock.patch.dict('os.environ', {}, clear=True):
        publisher_no_creds = XiaohongshuPublisher(mock_mode=False)
        result = publisher_no_creds.publish(
            title="测试标题",
            content="测试内容",
            images=[],
            topics=[]
        )
        assert result['success'] == False, "无凭证时应返回失败"
    print("✓ 无凭证时正确返回失败")

    # 测试2: mock模式，应返回成功
    print("\n测试4b: mock模式")
    publisher = XiaohongshuPublisher(mock_mode=True)

    result = publisher.publish(
        title="AI工具推荐 | 5个效率神器",
        content="姐妹们！今天分享5个我最近发现的AI神器...\n\n#AI工具 #效率神器",
        images=["base64_image_1", "base64_image_2"],
        topics=["#AI工具", "#效率神器"]
    )

    print(f"✓ 发布结果: {result['success']}")
    print(f"  笔记ID: {result.get('note_id', 'N/A')}")
    print(f"  笔记URL: {result.get('note_url', 'N/A')}")

    return result


def test_full_flow():
    """完整流程测试"""
    print("\n" + "="*60)
    print(" 小红书运营 Skill 集成测试 - 完整流程")
    print("="*60)

    try:
        # 1. 选题发现
        topics = test_topic_discovery()

        # 2. 选题筛选
        filtered = test_topic_filter(topics)

        # 3. 配图生成
        html_img, ai_img = test_image_designer()

        # 4. 发布测试
        result = test_publisher()

        print("\n" + "="*60)
        print(" ✓ 所有测试通过!")
        print("="*60)

        return True

    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_full_flow()
    sys.exit(0 if success else 1)
