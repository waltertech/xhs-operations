# 配图设计模块

## 功能
生成小红书笔记配图

## 支持模式

### 1. HTML截图模式 (html_screenshot)
将内容渲染为HTML后截图
- 适合文字卡片、信息图
- 可自定义风格模板

### 2. AI生图模式 (ai_gen)
调用AI生成图片
- 阿里云通义万相 (aliyun)
- nano banana pro (nano_banana)

## 参数
- content: 笔记内容
- mode: 生图模式 (html_screenshot/ai_gen)
- style: 风格(可选: default/modern/cute/minimal)
- api: AI生图时使用的API (aliyun/nano_banana)

## 输出
- html_screenshot: 返回截图的base64
- ai_gen: 返回生成的图片URL

## HTML模板风格

### default - 简洁风格
- 白色背景
- 黑色文字
- 居中对齐

### modern - 现代风格
- 渐变背景
- 白色卡片
- 阴影效果

### cute - 可爱风格
- 粉色/暖色系
- 圆角卡片
- 表情符号

### minimal - 极简风格
- 大面积留白
- 细字体
- 黑白配色
