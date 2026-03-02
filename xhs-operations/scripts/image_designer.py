import os
import base64
import json
from typing import Optional


class ImageDesigner:
    """配图设计模块 - 生成小红书笔记配图"""

    def __init__(self):
        self.aliyun_key = os.getenv('ALIYUN_API_KEY')
        self.nano_key = os.getenv('NANO_BANANA_API_KEY')

    def html_to_screenshot(self, content: str, style: str = 'default') -> str:
        """
        HTML布局截图模式

        Args:
            content: 笔记内容
            style: 风格模板 (default/modern/cute/minimal)

        Returns:
            截图的base64编码
        """
        html_template = self._generate_html(content, style)

        # TODO: 使用Playwright或Selenium进行截图
        # 示例代码:
        # from playwright.sync_api import sync_playwright
        # with sync_playwright() as p:
        #     browser = p.chromium.launch()
        #     page = browser.new_page()
        #     page.set_content(html_template)
        #     screenshot = page.screenshot()
        #     browser.close()
        # return base64.b64encode(screenshot).decode()

        # 暂时返回HTML内容作为占位符
        print(f"[ImageDesigner] Generated HTML ({len(html_template)} chars) for style: {style}")
        return base64.b64encode(html_template.encode('utf-8')).decode('utf-8')

    def ai_generate(self, prompt: str, api: str = 'aliyun') -> str:
        """
        AI生图模式

        Args:
            prompt: 图片生成提示词
            api: 使用的API (aliyun/nano_banana)

        Returns:
            生成的图片URL
        """
        if api == 'aliyun':
            return self._aliyun_generate(prompt)
        elif api == 'nano_banana':
            return self._nano_banana_generate(prompt)
        else:
            raise ValueError(f"不支持的API: {api}")

    def _generate_html(self, content: str, style: str) -> str:
        """生成HTML模板"""

        styles = {
            'default': '''
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    background: #ffffff;
                    color: #333;
                    padding: 40px;
                    max-width: 800px;
                    margin: 0 auto;
                    line-height: 1.8;
                }
                .card {
                    padding: 30px;
                    border-radius: 12px;
                }
            ''',
            'modern': '''
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #333;
                    padding: 40px;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .card {
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                    max-width: 600px;
                }
            ''',
            'cute': '''
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    background: linear-gradient(135deg, #ffe259 0%, #ffa751 100%);
                    color: #5a4a4a;
                    padding: 40px;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .card {
                    background: #fff5f5;
                    padding: 35px;
                    border-radius: 25px;
                    border: 3px solid #ffb6b9;
                    max-width: 580px;
                }
            ''',
            'minimal': '''
                body {
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                    background: #fafafa;
                    color: #111;
                    padding: 60px;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .card {
                    background: white;
                    padding: 50px 40px;
                    max-width: 500px;
                    border-left: 2px solid #111;
                }
            '''
        }

        css = styles.get(style, styles['default'])

        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Xiaohongshu Card</title>
    <style>
        {css}
        h1 {{ font-size: 28px; margin-bottom: 20px; }}
        p {{ font-size: 16px; margin: 0; }}
    </style>
</head>
<body>
    <div class="card">
        {content}
    </div>
</body>
</html>'''

        return html

    def _aliyun_generate(self, prompt: str) -> str:
        """
        阿里云通义万相API调用

        TODO: 实现真实的API调用
        需要配置 ALIYUN_API_KEY 环境变量
        """
        # 示例API调用代码:
        # import requests
        # url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/generation"
        # headers = {
        #     "Authorization": f"Bearer {self.aliyun_key}",
        #     "Content-Type": "application/json"
        # }
        # payload = {
        #     "model": "wanx-v1",
        #     "input": {"prompt": prompt},
        #     "parameters": {"size": "1024x1024"}
        # }
        # response = requests.post(url, headers=headers, json=payload)
        # return response.json()['output']['results'][0]['url']

        # 返回模拟URL
        print(f"[ImageDesigner] Calling Aliyun API with prompt: {prompt[:50]}...")
        return f"https://example.com/generated_image_{hash(prompt)}.jpg"

    def _nano_banana_generate(self, prompt: str) -> str:
        """
        nano banana pro API调用

        TODO: 实现真实的API调用
        需要配置 NANO_BANANA_API_KEY 环境变量
        """
        # 示例API调用代码:
        # import requests
        # url = "https://api.nanobanana.pro/v1/generate"
        # headers = {"Authorization": f"Bearer {self.nano_key}"}
        # payload = {"prompt": prompt, "model": "pro"}
        # response = requests.post(url, headers=headers, json=payload)
        # return response.json()['image_url']

        # 返回模拟URL
        print(f"[ImageDesigner] Calling Nano Banana API with prompt: {prompt[:50]}...")
        return f"https://example.com/nano_image_{hash(prompt)}.jpg"

    def design(self, content: str, mode: str = 'html_screenshot',
               style: str = 'default', api: str = 'aliyun') -> str:
        """
        主方法: 生成配图

        Args:
            content: 笔记内容
            mode: 生图模式 (html_screenshot/ai_gen)
            style: 风格模板
            api: AI生图API

        Returns:
            生成的图片数据 (base64或URL)
        """
        if mode == 'html_screenshot':
            return self.html_to_screenshot(content, style)
        elif mode == 'ai_gen':
            return self.ai_generate(content, api)
        else:
            raise ValueError(f"不支持的模式: {mode}")


if __name__ == "__main__":
    # 测试代码
    designer = ImageDesigner()

    # 测试HTML截图
    content = "<h1>AI工具推荐</h1><p>这5个神器让你的效率翻倍！</p>"
    img = designer.design(content, mode='html_screenshot', style='modern')
    print(f"HTML Screenshot: {len(img)} chars")

    # 测试AI生图
    img_url = designer.design("a cute cat sitting on a laptop", mode='ai_gen', api='aliyun')
    print(f"AI Image URL: {img_url}")
