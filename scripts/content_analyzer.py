"""
小红书内容分析模块

参考 baoyu-skills 的分析框架:
- 内容类型分类
- 钩子分析
- 目标受众识别
- 互动潜力评估
- 视觉机会映射
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ContentType(Enum):
    """内容类型"""
    PLANTING = "种草/安利"      # 产品推荐
    DRY_GOODS = "干货分享"      # 知识分享
    PERSONAL_STORY = "个人故事"  # 个人经历
    REVIEW = "测评对比"         # 评测对比
    TUTORIAL = "教程步骤"       # 教程步骤
    AVOIDANCE = "避坑指南"      # 避坑指南
    CHECKLIST = "清单合集"      # 清单合集


class Audience(Enum):
    """目标受众"""
    STUDENT = "学生党"        # 省钱、学习、校园
    WORKER = "打工人"         # 效率、职场
    MOM = "宝妈"              # 育儿、家居
    TRENDY_GIRL = "精致女孩"  # 美妆、穿搭
    TECH_GEEK = "技术宅"      # 工具、效率
    FOODIE = "美食爱好者"     # 探店、食谱
    TRAVELER = "旅行达人"     # 攻略、打卡


class HookType(Enum):
    """钩子类型"""
    NUMBER = "数字钩子"        # 5个方法、3分钟学会
    PAIN_POINT = "痛点钩子"    # 踩过的坑、后悔没早知道
    CURIOSITY = "好奇钩子"     # 原来、竟然
    BENEFIT = "利益钩子"       # 省钱、变美
    IDENTITY = "身份钩子"      # 打工人必看、学生党


@dataclass
class ContentAnalysis:
    """内容分析结果"""
    content_type: ContentType
    recommended_style: str
    recommended_layout: str
    target_audience: List[Audience]
    hook_score: int  # 1-5
    save_value: str  # high/medium/low
    share_triggers: List[str]
    outline_strategy: str  # a/b/c


class ContentAnalyzer:
    """小红书内容分析器"""

    # 内容类型 → 推荐风格/布局
    CONTENT_TYPE_MAP = {
        ContentType.PLANTING: ("cute", "balanced"),
        ContentType.DRY_GOODS: ("notion", "dense"),
        ContentType.PERSONAL_STORY: ("warm", "balanced"),
        ContentType.REVIEW: ("bold", "comparison"),
        ContentType.TUTORIAL: ("fresh", "flow"),
        ContentType.AVOIDANCE: ("bold", "list"),
        ContentType.CHECKLIST: ("cute", "list"),
    }

    # 关键词 → 内容类型
    KEYWORD_TYPE_MAP = {
        # 种草
        "推荐": ContentType.PLANTING,
        "好物": ContentType.PLANTING,
        "必备": ContentType.PLANTING,
        # 干货
        "技巧": ContentType.DRY_GOODS,
        "方法": ContentType.DRY_GOODS,
        "知识": ContentType.DRY_GOODS,
        # 个人故事
        "经历": ContentType.PERSONAL_STORY,
        "故事": ContentType.PERSONAL_STORY,
        "感受": ContentType.PERSONAL_STORY,
        # 测评
        "测评": ContentType.REVIEW,
        "对比": ContentType.REVIEW,
        "评测": ContentType.REVIEW,
        # 教程
        "教程": ContentType.TUTORIAL,
        "步骤": ContentType.TUTORIAL,
        "怎么": ContentType.TUTORIAL,
        # 避坑
        "避坑": ContentType.AVOIDANCE,
        "坑": ContentType.AVOIDANCE,
        "别": ContentType.AVOIDANCE,
        # 清单
        "清单": ContentType.CHECKLIST,
        "合集": ContentType.CHECKLIST,
        "列表": ContentType.CHECKLIST,
    }

    # 关键词 → 受众
    KEYWORD_AUDIENCE_MAP = {
        "学生": Audience.STUDENT,
        "上学": Audience.STUDENT,
        "打工": Audience.WORKER,
        "职场": Audience.WORKER,
        "上班": Audience.WORKER,
        "宝宝": Audience.MOM,
        "育儿": Audience.MOM,
        "孩子": Audience.MOM,
        "美妆": Audience.TRENDY_GIRL,
        "穿搭": Audience.TRENDY_GIRL,
        "漂亮": Audience.TRENDY_GIRL,
        "代码": Audience.TECH_GEEK,
        "开发": Audience.TECH_GEEK,
        "工具": Audience.TECH_GEEK,
        "美食": Audience.FOODIE,
        "好吃": Audience.FOODIE,
        "探店": Audience.FOODIE,
        "旅行": Audience.TRAVELER,
        "旅游": Audience.TRAVELER,
        "攻略": Audience.TRAVELER,
    }

    # 内容信号 → 推荐风格/布局 (来自 baoyu-skills)
    # 注意: 只使用 ImageDesigner 中实际存在的风格
    AUTO_SELECTION_MAP = {
        ("美", "时尚", "可爱", "女生", "粉色"): ("cute", "sparse"),
        ("健康", "自然", "清新", "有机"): ("fresh", "balanced"),
        ("生活", "故事", "情感", "温暖"): ("warm", "balanced"),
        ("警告", "重要", "必须", "关键"): ("bold", "list"),
        ("专业", "商业", "优雅", "简单"): ("minimal", "sparse"),
        ("经典", "复古", "传统", "怀旧"): ("retro", "balanced"),
        ("有趣", "惊喜", "哇", "厉害"): ("pop", "sparse"),
        ("知识", "概念", "效率", "软件"): ("notion", "dense"),
        ("教育", "教程", "学习", "课堂"): ("notion", "balanced"),  # chalkboard → notion
        ("笔记", "手写", "学习指南", "真实"): ("notion", "dense"),   # study-notes → notion
    }

    def analyze(self, content: str, title: str = "") -> ContentAnalysis:
        """
        分析内容

        Args:
            content: 内容文本
            title: 标题 (可选)

        Returns:
            ContentAnalysis: 分析结果
        """
        # 1. 内容类型分类
        content_type = self._classify_content_type(content)

        # 2. 目标受众识别
        audiences = self._identify_audience(content)

        # 3. 钩子分析
        hook_score = self._analyze_hook(title or content)

        # 4. 收藏价值
        save_value = self._evaluate_save_value(content)

        # 5. 分享触发点
        share_triggers = self._find_share_triggers(content)

        # 6. 推荐风格和布局 (先尝试 AUTO_SELECTION_MAP，后备 CONTENT_TYPE_MAP)
        style, layout = self._auto_select_style_layout(content)

        # 7. 大纲策略
        outline_strategy = self._determine_strategy(content_type, hook_score)

        return ContentAnalysis(
            content_type=content_type,
            recommended_style=style,
            recommended_layout=layout,
            target_audience=audiences,
            hook_score=hook_score,
            save_value=save_value,
            share_triggers=share_triggers,
            outline_strategy=outline_strategy,
        )

    def _auto_select_style_layout(self, content: str) -> tuple:
        """根据内容关键词自动选择风格和布局"""
        content_lower = content.lower()

        # 遍历 AUTO_SELECTION_MAP，匹配关键词
        for keywords, (style, layout) in self.AUTO_SELECTION_MAP.items():
            for keyword in keywords:
                if keyword in content_lower:
                    return (style, layout)

        # 如果没有匹配，返回默认值
        return ("cute", "balanced")

    def _classify_content_type(self, content: str) -> ContentType:
        """内容类型分类"""
        content_lower = content.lower()

        for keyword, ctype in self.KEYWORD_TYPE_MAP.items():
            if keyword in content_lower:
                return ctype

        return ContentType.DRY_GOODS  # 默认

    def _identify_audience(self, content: str) -> List[Audience]:
        """识别目标受众"""
        audiences = []
        content_lower = content.lower()

        for keyword, audience in self.KEYWORD_AUDIENCE_MAP.items():
            if keyword in content_lower and audience not in audiences:
                audiences.append(audience)

        return audiences if audiences else [Audience.WORKER]  # 默认

    def _analyze_hook(self, text: str) -> int:
        """分析钩子潜力 (1-5分)"""
        score = 0
        text_lower = text.lower()

        # 数字钩子
        if any(kw in text_lower for kw in ["个", "步", "分钟", "天", "第"]):
            score += 1

        # 痛点钩子
        if any(kw in text_lower for kw in ["坑", "后悔", "别再", "踩雷"]):
            score += 1

        # 好奇钩子
        if any(kw in text_lower for kw in ["原来", "竟然", "没想到"]):
            score += 1

        # 利益钩子
        if any(kw in text_lower for kw in ["省钱", "变美", "效率", "翻倍"]):
            score += 1

        # 身份钩子
        if any(kw in text_lower for kw in ["打工人", "学生党", "新手", "宝妈"]):
            score += 1

        return min(score + 1, 5)  # 至少1分

    def _evaluate_save_value(self, content: str) -> str:
        """评估收藏价值"""
        content_lower = content.lower()

        # 清单类、教程类收藏价值高
        if any(kw in content_lower for kw in ["清单", "教程", "步骤", "方法", "技巧"]):
            return "high"

        # 新闻类收藏价值低
        if any(kw in content_lower for kw in ["今天", "刚刚", "新闻"]):
            return "low"

        return "medium"

    def _find_share_triggers(self, content: str) -> List[str]:
        """查找分享触发点"""
        triggers = []
        content_lower = content.lower()

        if "朋友" in content_lower:
            triggers.append("我朋友也需要看这个")

        if any(kw in content_lower for kw in ["就是", "是我"]):
            triggers.append("这说的就是我")

        if any(kw in content_lower for kw in ["有用", "干货"]):
            triggers.append("太有用了必须分享")

        return triggers

    def _determine_strategy(self, content_type: ContentType, hook_score: int) -> str:
        """确定大纲策略"""
        # 个人故事类 → 策略A (故事驱动)
        if content_type == ContentType.PERSONAL_STORY:
            return "a"

        # 干货/教程类 → 策略B (信息密集)
        if content_type in [ContentType.DRY_GOODS, ContentType.TUTORIAL]:
            return "b"

        # 高钩子分数 + 种草/测评 → 策略C (视觉优先)
        if hook_score >= 4 and content_type in [ContentType.PLANTING, ContentType.REVIEW]:
            return "c"

        # 默认
        return "a"


if __name__ == "__main__":
    analyzer = ContentAnalyzer()

    # 测试
    test_contents = [
        ("打工人必看！5个效率神器让你准时下班", "打工人必看！5个效率神器让你准时下班"),
        ("考研英语背单词方法分享", "考研英语背单词方法分享"),
        ("我的护肤心得分享", "我的护肤心得分享"),
    ]

    for content, title in test_contents:
        result = analyzer.analyze(content, title)
        print(f"\n内容: {title}")
        print(f"  类型: {result.content_type.value}")
        print(f"  推荐风格: {result.recommended_style}")
        print(f"  推荐布局: {result.recommended_layout}")
        print(f"  钩子分数: {'⭐' * result.hook_score}")
        print(f"  收藏价值: {result.save_value}")
        print(f"  策略: {result.outline_strategy}")
