# 小红书运营 Skill

全流程小红书运营工具，支持选题发现、筛选、内容创作、配图生成、发布。

## 功能

- 选题发现：搜索微信公众号/X/小红书/Reddit
- 选题筛选：综合热度/差异化/时效性评分
- 内容撰写：小红书风格种草文案
- 标题生成：CTR优化标题
- 配图设计：HTML截图/AI生图
- 自动发布：一键发布到小红书

## 项目结构

```
xhs-operations/
├── skill.yaml              # Skill配置文件
├── README.md              # 说明文档
├── .env.example           # 环境变量示例
├── prompts/               # Prompt文件
│   ├── __root__.md        # 入口路由
│   ├── topic-discovery.md # 选题发现
│   ├── topic-filter.md    # 选题筛选
│   ├── content-writer.md # 内容撰写
│   ├── title-generator.md# 标题生成
│   ├── image-designer.md # 配图设计
│   └── publisher.md       # 发布模块
├── scripts/               # Python脚本
│   ├── topic_discovery.py # 选题发现实现
│   ├── topic_filter.py   # 选题筛选实现
│   ├── image_designer.py # 配图设计实现
│   └── publisher.py      # 发布模块实现
└── test_integration.py   # 集成测试
```

## 使用方法

### 完整流程

```
帮我运营小红书，主题是AI工具推荐
```

### 分步功能

- 选题发现：`帮我找一些AI领域的选题`
- 选题筛选：对选题进行综合评分排序
- 内容撰写：生成小红书风格种草文案
- 标题生成：生成高CTR优化标题
- 配图设计：HTML截图或AI生图
- 自动发布：发布笔记到小红书

## 配置

1. 复制环境变量配置：

```bash
cp .env.example .env
```

2. 编辑 `.env` 填入你的配置：

- `XHS_COOKIE`: 小红书登录Cookie (推荐)
- `ALIYUN_API_KEY`: 阿里云通义万相API (AI生图)
- 其他API密钥根据需要配置

## 运行测试

```bash
python3 test_integration.py
```

## 技术栈

- OpenCLAW skill格式
- Python 3.x
- scikit-learn (选题筛选)
- Playwright/Selenium (可选，用于截图)
- AI生图API (阿里云/nano banana)

## License

MIT
