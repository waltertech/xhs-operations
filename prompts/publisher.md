# 发布模块

## 功能
自动发布小红书笔记

## 发布流程
1. 登录验证
2. 上传图片
3. 填写标题和内容
4. 添加话题标签
5. 提交发布

## 参数
- title: 笔记标题
- content: 笔记正文
- images: 图片列表 (base64或URL)
- topics: 话题标签列表

## 输出
```json
{
  "success": true,
  "note_id": "xxx",
  "note_url": "https://www.xiaohongshu.com/explore/xxx",
  "message": "发布成功"
}
```

## 注意事项
- 需要配置 XHS_COOKIE 环境变量 (登录态)
- 或使用 Selenium 模拟登录
- 图片格式支持 jpg/png，最大10MB
- 话题标签最多10个
