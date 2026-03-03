# 配图设计模块

## 功能
生成小红书笔记配图

## 支持模式

### 1. HTML截图模式 (html_screenshot)
将内容渲染为HTML后截图
- 适合文字卡片，信息图，海报
- 成本极低（仅调用文本API生成HTML）
- 可自定义风格模板

### 2. AI生图模式 (ai_gen)
调用AI生成图片
- 阿里云通义万相 (aliyun)
- nano banana pro (nano_banana)

## 参数
- content: HTML内容
- mode: 生图模式 (html_screenshot/ai_gen)
- style: 风格模板
- api: AI生图时使用的API (aliyun/nano_banana)
- width: 图片宽度 (默认800)
- height: 图片高度 (默认600)

## 输出
- html_screenshot: 返回截图的base64 (PNG格式)
- ai_gen: 返回生成的图片URL

## 风格系统 (12种)

参考 baoyu-skills 小红书图片生成最佳实践:

| 风格 | 描述 | 适用场景 |
|------|------|----------|
| **cute** | 甜美可爱，经典小红书风格 | 美妆、穿搭、生活分享 |
| **fresh** | 清新自然，干净清爽 | 健康、自然、生活方式 |
| **warm** | 温暖友好，情感共鸣 | 个人故事、生活分享 |
| **bold** | 高冲击力，吸睛 | 测评对比、避坑指南 |
| **minimal** | 极简精致，专业 | 商务、专业内容 |
| **retro** | 复古怀旧，潮流 | 经典、传统内容 |
| **pop** | 活力四射，炫酷 | 活动、创意内容 |
| **notion** | 手绘线稿，知性 | 干货知识、教程 |
| **modern** | 现代渐变，科技感 | 科技、效率工具 |
| **elegant** | 优雅精致，商务 | 专业知识、商业内容 |
| **dark** | 深色科技 | 开发者、内容创作者 |
| **glass** | 毛玻璃效果 | 时尚、设计类 |

## 布局系统 (8种)

| 布局 | 描述 | 适用场景 |
|------|------|----------|
| **sparse** | 稀疏布局 (1-2个要点) | 封面、吸睛内容 |
| **balanced** | 平衡布局 (3-4个要点) | 标准内容 |
| **dense** | 密集布局 (5-8个要点) | 知识卡片、干货 |
| **list** | 列表布局 (4-7项) | 清单、排名 |
| **comparison** | 对比前后对比、产品布局 | 对比 |
| **flow** | 流程布局 | 教程、步骤 |
| **mindmap** | 思维导图 | 知识整理 |
| **quadrant** | 四象限布局 | 分析、分类 |

## 风格 × 布局 组合矩阵

| | sparse | balanced | dense | list | comparison | flow |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| cute | ✓✓ | ✓✓ | ✓ | ✓✓ | ✓ | ✓ |
| fresh | ✓✓ | ✓✓ | ✓ | ✓ | ✓ | ✓✓ |
| warm | ✓✓ | ✓✓ | ✓ | ✓ | ✓✓ | ✓ |
| bold | ✓✓ | ✓ | ✓ | ✓✓ | ✓✓ | ✓ |
| minimal | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓ | ✓ |
| notion | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ |

## 内容分析

模块可以自动分析内容推荐合适的风格:

```
内容类型:
- 种草/安利 → cute + balanced
- 干货分享 → notion + dense
- 个人故事 → warm + balanced
- 测评对比 → bold + comparison
- 教程步骤 → fresh + flow
- 避坑指南 → bold + list
- 清单合集 → cute + list
```

## HTML模板规范

参考何三笔记 best practices:

### 1. 容器要求
- 必须包含 `id="capture-container"` 的容器
- 使用 `min-height` 而非固定高度
- 使用 `justify-content: flex-start` 防止内容被裁剪

### 2. 高度计算
```
标题: 50px
5个卡片: 5 × 80px = 400px
间距: 100px
内边距: 80px
总计: ~810px
建议: min-height: 1000px (预留20%缓冲)
```

### 3. 布局对齐
- 使用 flex 布局
- 推荐使用 `justify-content: flex-start`

## 使用示例

```python
from image_designer import ImageDesigner

designer = ImageDesigner()

# 查看所有可用风格
print(designer.get_available_styles())
# ['cute', 'fresh', 'warm', 'bold', 'minimal', 'retro', 'pop', 'notion', 'modern', 'elegant', 'dark', 'glass']

# HTML截图 - 推荐风格
content = """
<span class="tag">推荐</span>
<h1>AI工具推荐</h1>
<p>这5个神器让你的效率翻倍！</p>
"""
img = designer.design(content, mode='html_screenshot', style='cute')
```

## 内容分析示例

```python
from content_analyzer import ContentAnalyzer

analyzer = ContentAnalyzer()

result = analyzer.analyze(
    content="打工人必看！5个效率神器让你准时下班",
    title="打工人必看！5个效率神器让你准时下班"
)

print(f"推荐风格: {result.recommended_style}")
print(f"推荐布局: {result.recommended_layout}")
print(f"内容类型: {result.content_type.value}")
print(f"钩子分数: {result.hook_score}/5")
print(f"大纲策略: {result.outline_strategy}")
```

## 依赖安装

```bash
# 安装 Playwright
pip install playwright
playwright install chromium

# 或使用 AI 生图
# 配置 ALIYUN_API_KEY 环境变量
```
