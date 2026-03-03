# 选题发现模块

## 功能
从多个平台搜索热门内容选题

## 支持平台
- 微信公众号 (wechat)
- X / Twitter (x)
- 小红书 (xiaohongshu)
- Reddit (reddit)

## 参数
- keyword: 搜索关键词
- platforms: 目标平台列表 (默认全部)
- limit: 返回数量 (默认10)

## 输出格式
```json
[
  {
    "platform": "wechat",
    "title": "文章标题",
    "summary": "文章摘要",
    "publish_time": "2024-01-01",
    "source": "公众号名称",
    "url": "文章链接",
    "engagement": { "likes": 100, "comments": 20 }
  }
]
```

## 执行逻辑
1. 根据关键词调用各平台搜索API
2. 格式化返回结果
3. 返回统一格式的JSON数组
