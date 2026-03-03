import os
import base64
import json
import uuid
import tempfile
from typing import Optional


class ImageDesigner:
    """配图设计模块 - 生成小红书笔记配图

    支持多种精美风格:
    - modern: 现代渐变风格 (Vibrant & Block-based)
    - elegant: 优雅精致风格 (Minimal & Sophisticated)
    - cute: 可爱活泼风格 (Playful & Friendly)
    - minimal: 极简风格 (Clean & Simple)
    - dark: 深色科技风格 (Tech & Modern)
    - glass: 毛玻璃风格 (Glassmorphism)
    """

    def __init__(self):
        self.aliyun_key = os.getenv('ALIYUN_API_KEY')
        self.nano_key = os.getenv('NANO_BANANA_API_KEY')

    def html_to_screenshot(self, content: str, style: str = 'modern',
                          width: int = 800, height: int = 600) -> str:
        """
        HTML布局截图模式

        Args:
            content: HTML内容
            style: 风格模板 (modern/elegant/cute/minimal/dark/glass)
            width: 图片宽度
            height: 图片高度

        Returns:
            截图的base64编码 (PNG格式)

        Note:
            需要安装 playwright 并运行 playwright install chromium
            或配置 ALIYUN_API_KEY 使用AI生图模式
        """
        html_template = self._generate_html(content, style, width, height)

        # 尝试使用Playwright进行截图
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.set_content(html_template, wait_until='networkidle')
                # 设置固定尺寸
                page.set_viewport_size({'width': width, 'height': height})
                screenshot = page.screenshot(type='png')
                browser.close()
                return base64.b64encode(screenshot).decode('utf-8')
        except ImportError:
            # Playwright未安装，返回错误提示
            raise RuntimeError(
                "Playwright not installed. Run: pip install playwright && playwright install chromium "
                "Or use ai_gen mode with ALIYUN_API_KEY configured."
            )
        except Exception as e:
            raise RuntimeError(f"Screenshot failed: {e}")

    def save_html_file(self, content: str, style: str = 'modern',
                       width: int = 800, height: int = 600) -> str:
        """
        保存HTML到临时文件（用于capture-html等外部工具）

        Args:
            content: HTML内容
            style: 风格模板
            width: 图片宽度
            height: 图片高度

        Returns:
            临时HTML文件路径
        """
        html_template = self._generate_html(content, style, width, height)

        # 创建临时文件
        fd, path = tempfile.mkstemp(suffix='.html', prefix='xhs_image_')
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(html_template)

        return path

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

    def _generate_html(self, content: str, style: str, width: int, height: int) -> str:
        """生成HTML模板 - 参考何三笔记和UI/UX设计规范"""

        # 字体导入
        font_import = '''
        @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
        '''

        styles = {
            # 现代渐变风格 - Vibrant & Block-based
            'modern': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Space Grotesk', 'Noto Sans SC', -apple-system, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: {height}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: rgba(255, 255, 255, 0.95);
                    border-radius: 24px;
                    padding: 48px;
                    max-width: {width - 80}px;
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }}
                .card h1 {{
                    font-size: 36px;
                    font-weight: 700;
                    color: #1e293b;
                    margin-bottom: 16px;
                    line-height: 1.2;
                }}
                .card p {{
                    font-size: 18px;
                    color: #64748b;
                    line-height: 1.7;
                }}
                .tag {{
                    display: inline-block;
                    background: linear-gradient(135deg, #E11D48 0%, #FB7185 100%);
                    color: white;
                    padding: 6px 16px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: 600;
                    margin-bottom: 16px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
            ''',

            # 优雅精致风格 - Minimal & Sophisticated
            'elegant': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Archivo', 'Noto Sans SC', -apple-system, sans-serif;
                    background: linear-gradient(145deg, #f5f5f5 0%, #e8e8e8 100%);
                    min-height: {height}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: #ffffff;
                    border-radius: 16px;
                    padding: 56px;
                    max-width: {width - 80}px;
                    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
                    border-left: 4px solid #1a1a1a;
                }}
                .card h1 {{
                    font-size: 32px;
                    font-weight: 600;
                    color: #1a1a1a;
                    margin-bottom: 20px;
                    letter-spacing: -0.5px;
                    line-height: 1.3;
                }}
                .card p {{
                    font-size: 16px;
                    color: #6b7280;
                    line-height: 1.8;
                    max-width: 90%;
                }}
                .accent {{
                    width: 60px;
                    height: 4px;
                    background: #1a1a1a;
                    margin-bottom: 24px;
                }}
            ''',

            # 可爱活泼风格 - Playful & Friendly
            'cute': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Poppins', 'Noto Sans SC', -apple-system, sans-serif;
                    background: linear-gradient(135deg, #ffe259 0%, #ffa751 100%);
                    min-height: {height}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: #fff5f5;
                    border-radius: 32px;
                    padding: 44px;
                    max-width: {width - 80}px;
                    box-shadow: 0 20px 40px rgba(255, 171, 145, 0.3);
                    border: 3px solid #ffb6b9;
                    position: relative;
                    overflow: hidden;
                }}
                .card::before {{
                    content: '';
                    position: absolute;
                    top: -50%;
                    right: -50%;
                    width: 100%;
                    height: 100%;
                    background: radial-gradient(circle, rgba(255,182,185,0.2) 0%, transparent 70%);
                }}
                .card h1 {{
                    font-size: 34px;
                    font-weight: 700;
                    color: #5d4a4a;
                    margin-bottom: 14px;
                    position: relative;
                }}
                .card p {{
                    font-size: 17px;
                    color: #7d6a6a;
                    line-height: 1.7;
                    position: relative;
                }}
                .emoji {{
                    font-size: 28px;
                    margin-right: 8px;
                }}
            ''',

            # 极简风格 - Clean & Simple
            'minimal': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Helvetica Neue', 'Noto Sans SC', Arial, sans-serif;
                    background: #ffffff;
                    min-height: {height}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: white;
                    border-radius: 8px;
                    padding: 48px;
                    max-width: {width - 80}px;
                    border: 1px solid #e5e5e5;
                }}
                .card h1 {{
                    font-size: 28px;
                    font-weight: 500;
                    color: #000000;
                    margin-bottom: 16px;
                    letter-spacing: -0.3px;
                    line-height: 1.4;
                }}
                .card p {{
                    font-size: 15px;
                    color: #666666;
                    line-height: 1.6;
                }}
            ''',

            # 深色科技风格 - Tech & Modern
            'dark': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Space Grotesk', 'Noto Sans SC', -apple-system, sans-serif;
                    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
                    min-height: {height}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: rgba(30, 41, 59, 0.8);
                    backdrop-filter: blur(20px);
                    border-radius: 20px;
                    padding: 48px;
                    max-width: {width - 80}px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                }}
                .card h1 {{
                    font-size: 36px;
                    font-weight: 700;
                    color: #f8fafc;
                    margin-bottom: 16px;
                    line-height: 1.2;
                }}
                .card p {{
                    font-size: 18px;
                    color: #94a3b8;
                    line-height: 1.7;
                }}
                .glow {{
                    position: absolute;
                    width: 200px;
                    height: 200px;
                    background: radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%);
                    top: -100px;
                    right: -100px;
                    border-radius: 50%;
                }}
            ''',

            # 毛玻璃风格 - Glassmorphism
            'glass': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Poppins', 'Noto Sans SC', -apple-system, sans-serif;
                    background: linear-gradient(135deg, #a855f7 0%, #3b82f6 50%, #06b6d4 100%);
                    min-height: {height}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(20px);
                    -webkit-backdrop-filter: blur(20px);
                    border-radius: 24px;
                    padding: 48px;
                    max-width: {width - 80}px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }}
                .card h1 {{
                    font-size: 34px;
                    font-weight: 600;
                    color: #ffffff;
                    margin-bottom: 16px;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    line-height: 1.3;
                }}
                .card p {{
                    font-size: 17px;
                    color: rgba(255, 255, 255, 0.85);
                    line-height: 1.7;
                }}
            ''',
        }

        css = styles.get(style, styles['modern'])

        # 处理内容 - 确保有capture-container
        if 'id="capture-container"' not in content:
            content = f'<div id="capture-container">{content}</div>'

        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Xiaohongshu Image</title>
    <style>
        {css}
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
               style: str = 'modern', api: str = 'aliyun',
               width: int = 800, height: int = 600) -> str:
        """
        主方法: 生成配图

        Args:
            content: HTML内容
            mode: 生图模式 (html_screenshot/ai_gen)
            style: 风格模板 (modern/elegant/cute/minimal/dark/glass)
            api: AI生图API
            width: 图片宽度
            height: 图片高度

        Returns:
            生成的图片数据 (base64或URL)
        """
        if mode == 'html_screenshot':
            return self.html_to_screenshot(content, style, width, height)
        elif mode == 'ai_gen':
            return self.ai_generate(content, api)
        else:
            raise ValueError(f"不支持的模式: {mode}")


if __name__ == "__main__":
    # 测试代码
    designer = ImageDesigner()

    # 测试各种风格
    test_styles = ['modern', 'elegant', 'cute', 'minimal', 'dark', 'glass']

    content = """
        <span class="tag">推荐</span>
        <h1>AI工具推荐</h1>
        <p>这5个神器让你的效率翻倍！</p>
    """

    for style in test_styles:
        try:
            img = designer.design(content, mode='html_screenshot', style=style)
            print(f"{style}: {len(img)} chars")
        except Exception as e:
            print(f"{style}: Error - {e}")

    # 测试AI生图
    img_url = designer.design("a cute cat sitting on a laptop", mode='ai_gen', api='aliyun')
    print(f"AI Image URL: {img_url}")
