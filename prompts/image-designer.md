# 配图设计模块

## 功能
生成小红书笔记配图

## 支持模式

### 1. HTML截图模式 (html_screenshot)
将内容渲染为HTML后截图
- 适合文字卡片、信息图、海报
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

## HTML模板风格

### modern - 现代渐变风格 (推荐)
- 渐变背景 (紫蓝渐变)
- 白色玻璃卡片
- 现代字体 (Space Grotesk)
- 适合: 科技、效率工具推荐

```
<span class="tag">推荐</span>
<h1>AI工具推荐</h1>
<p>这5个神器让你的效率翻倍！</p>
```

### elegant - 优雅精致风格
- 浅灰背景
- 纯白卡片 + 左侧装饰线
- 衬线字体 (Archivo)
- 适合: 专业内容、知识分享

```
<div class="accent"></div>
<h1>深度解读</h1>
<p>关于ChatGPT的深度分析...</p>
```

### cute - 可爱活泼风格
- 暖色渐变背景 (橙黄)
- 粉色圆角卡片
- 表情装饰
- 适合: 生活分享、好物推荐

```
<span class="emoji">🌟</span>
<h1>必看推荐</h1>
<p>姐妹们！这个真的太好用了！</p>
```

### minimal - 极简风格
- 纯白背景
- 细边框卡片
- 无装饰
- 适合: 简约主义者

```
<h1>极简生活</h1>
<p>Less is more.</p>
```

### dark - 深色科技风格
- 深蓝渐变背景
- 半透明毛玻璃卡片
- 发光效果
- 适合: 开发者、内容创作者

```
<h1>Code Better</h1>
<p>Write clean code, ship faster.</p>
```

### glass - 毛玻璃风格
- 彩色渐变背景
- 高斯模糊玻璃效果
- 现代感强
- 适合: 时尚、设计类内容

```
<h1>设计灵感</h1>
<p>Beautiful design matters.</p>
```

## HTML生成规范

参考何三笔记的 best practices:

### 1. 容器要求
- 必须包含 `id="capture-container"` 的容器
- 使用 `min-height` 而非固定高度
- 使用 `justify-content: flex-start` 防止内容被裁剪

### 2. 高度计算
```
标题: 50px
5个卡片: 5 × 80px = 400px
4个箭头: 4 × 30px = 120px
底部说明: 60px
间距: 100px
内边距: 80px
总计: 810px
建议: min-height: 1000px (预留20%缓冲)
```

### 3. 布局对齐
- 使用 flex 布局
- 避免 `justify-content: center`（内容多时会被裁剪）
- 推荐使用 `justify-content: flex-start`

### 4. 样式建议
- 所有样式内联在 style 属性中
- 使用现代 CSS (flexbox, grid, 渐变)
- 考虑响应式设计

## 使用示例

```python
from image_designer import ImageDesigner

designer = ImageDesigner()

# HTML截图
content = """
<span class="tag">推荐</span>
<h1>AI工具推荐</h1>
<p>这5个神器让你的效率翻倍！</p>
"""
img = designer.design(content, mode='html_screenshot', style='modern')
```

## 依赖安装

```bash
# 安装 Playwright
pip install playwright
playwright install chromium

# 或使用 AI 生图
# 配置 ALIYUN_API_KEY 环境变量
```
