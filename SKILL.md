---
name: xhs-operations
description: "小红书全流程运营Skill，覆盖选题发现、内容撰写、配图设计、自动发布。支持从多平台（微信公众号、X/Twitter、Reddit）发现热门选题，AI生成种草文案和高点击率标题，一键发布到小红书。Use when: (1) 需要运营小红书账号, (2) 寻找热门选题, (3) 生成种草文案, (4) 自动发布笔记"
metadata:
  {
    "openclaw":
      {
        "emoji": "📕",
        "requires": { "bins": ["python3"], "python": ["playwright", "requests", "scikit-learn", "numpy"] },
        "install":
          [
            {
              "id": "pip-install",
              "kind": "pip",
              "package": "-r requirements.txt",
              "label": "Install Python dependencies",
            },
            {
              "id": "playwright-install",
              "kind": "shell",
              "command": "playwright install chromium",
              "label": "Install Playwright Chromium",
            },
          ],
      },
  }
---

# 小红书运营 Skill (xhs-operations)

全流程小红书运营工具，覆盖选题发现 → 选题筛选 → 内容创作 → 配图生成 → 自动发布的完整工作流。

## 功能概览

| 功能 | 描述 | 脚本 |
|------|------|------|
| 选题发现 | 从微信公众号、X/Twitter、小红书、Reddit搜索热门内容 | `scripts/topic_discovery.py` |
| 选题筛选 | 综合热度/差异化/时效性评分排序 | `scripts/topic_filter.py` |
| 内容撰写 | 生成小红书风格种草文案 | prompts/`content-writer.md` |
| 标题生成 | CTR优化高点击率标题 | prompts/`title-generator.md` |
| 配图设计 | HTML截图/AI生图 | `scripts/image_designer.py` |
| 自动发布 | 一键发布笔记到小红书 | `scripts/publisher.py` |

## 快速开始

### 完整流程

```bash
# 帮我运营小红书，主题是AI工具推荐
# AI会执行: 选题发现 → 筛选 → 写文案 → 生成配图 → 发布
```

### 分步使用

```bash
# 1. 选题发现 - 搜索AI领域的热门选题
python3 scripts/topic_discovery.py --keyword "AI工具" --platforms wechat,xiaohongshu

# 2. 选题筛选 - 对选题进行综合评分
python3 scripts/topic_filter.py --input topics.json --sort-by score

# 3. 内容撰写 - 生成种草文案
# 通过 prompts/content-writer.md 使用

# 4. 标题生成 - 生成高CTR标题
# 通过 prompts/title-generator.md 使用

# 5. 配图设计 - 生成封面/配图
python3 scripts/image_designer.py --content "AI工具推荐" --style cute

# 6. 发布笔记 - 自动发布到小红书
python3 scripts/publisher.py --title "AI工具推荐" --content "正文..." --images img1.jpg,img2.jpg
```

## 配置

### 环境变量

在项目根目录创建 `.env` 文件：

```bash
# 复制示例配置
cp .env.example .env
```

支持的配置项：

| 变量 | 必填 | 描述 |
|------|-----|------|
| `XHS_COOKIE` | 推荐 | 小红书登录Cookie (用于发布) |
| `XHS_USERNAME` | 可选 | 小红书用户名 (Cookie失效时备用) |
| `XHS_PASSWORD` | 可选 | 小红书密码 |
| `ALIYUN_API_KEY` | 可选 | 阿里云通义万相API (AI生图) |
| `OPENAI_API_KEY` | 可选 | OpenAI API (内容生成) |
| `TWITTER_API_KEY` | 可选 | Twitter API (选题发现) |
| `REDDIT_API_KEY` | 可选 | Reddit API (选题发现) |

### 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Playwright浏览器 (可选，用于截图)
playwright install chromium
```

## 项目结构

```
xhs-operations/
├── SKILL.md                    # Skill配置文件
├── skill.yaml                  # Skill路由配置
├── README.md                   # 项目说明
├── .env.example               # 环境变量示例
├── requirements.txt           # Python依赖
├── prompts/                   # Prompt模板
│   ├── __root__.md            # 入口路由
│   ├── topic-discovery.md     # 选题发现Prompt
│   ├── topic-filter.md        # 选题筛选Prompt
│   ├── content-writer.md      # 内容撰写Prompt
│   ├── title-generator.md     # 标题生成Prompt
│   ├── image-designer.md      # 配图设计Prompt
│   └── publisher.md           # 发布Prompt
├── scripts/                   # Python实现
│   ├── topic_discovery.py     # 选题发现
│   ├── topic_filter.py        # 选题筛选
│   ├── content_analyzer.py     # 内容分析
│   ├── image_designer.py      # 配图设计
│   └── publisher.py           # 发布模块
└── test_integration.py         # 集成测试
```

## API 实现

### 选题发现 (topic_discovery.py)

支持的平台：

| 平台 | 方法 | 状态 |
|------|------|------|
| 微信公众号 | `search_wechat()` | Mock实现 |
| X/Twitter | `search_x()` | Mock实现 |
| 小红书 | `search_xiaohongshu()` | Mock实现 |
| Reddit | `search_reddit()` | Mock实现 |

```python
from scripts.topic_discovery import TopicDiscovery

discovery = TopicDiscovery()
results = discovery.search(
    keyword="AI工具",
    platforms=["wechat", "xiaohongshu"],
    limit=10
)
```

### 选题筛选 (topic_filter.py)

基于多维度评分：

- **热度分**: 点赞/评论/收藏数
- **差异化分**: 与已有内容的独特性
- **时效性分**: 内容新鲜度
- **平台权重**: 不同平台的影响力系数

```python
from scripts.topic_filter import TopicFilter

filter = TopicFilter()
scored = filter.score_and_sort(topics, weights={
    'engagement': 0.4,
    'differentiation': 0.3,
    'recency': 0.3
})
```

### 发布模块 (publisher.py)

支持两种模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| Mock模式 | 模拟发布，用于测试 | 开发调试 |
| 真实模式 | 真实调用小红书API | 生产环境 |

```python
from scripts.publisher import XiaohongshuPublisher

# Mock模式测试
publisher = XiaohongshuPublisher(mock_mode=True)
result = publisher.publish(
    title="AI工具推荐",
    content="姐妹们，今天分享...",
    images=["base64_or_url"],
    topics=["#AI工具"]
)
```

## 运行测试

```bash
# 运行集成测试
python3 test_integration.py

# 测试选题发现
python3 -c "
from scripts.topic_discovery import TopicDiscovery
d = TopicDiscovery()
print(d.search('AI', platforms=['wechat']))
"

# 测试发布模块
python3 -c "
from scripts.publisher import XiaohongshuPublisher
p = XiaohongshuPublisher(mock_mode=True)
print(p.publish('Test', 'Content'))
"
```

## 错误处理

所有核心模块都包含完善的错误处理：

- **网络错误**: 自动重试 + 降级处理
- **认证错误**: 清晰的错误提示
- **API限制**: 指数退避重试
- **参数验证**: 友好的输入提示

## 注意事项

1. **Cookie有效期**: 小红书Cookie通常有效期较短，建议定期更新
2. **API限制**: 各平台API有调用频率限制，请合理使用
3. **内容合规**: 发布内容需符合小红书社区规范
4. **Mock模式**: 生产环境发布前请先在Mock模式测试

## License

MIT
