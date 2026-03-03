import os
import base64
import json
import uuid
import tempfile
from typing import Optional, Dict, List


class ImageDesigner:
    """配图设计模块 - 生成小红书笔记配图

    支持多种精美风格 (参考 baoyu-skills):
    - cute: 甜美可爱 - 经典小红书风格
    - fresh: 清新自然 - 干净清爽
    - warm: 温暖友好 - 情感共鸣
    - bold: 高冲击力 - 吸睛
    - minimal: 极简精致 - 专业
    - retro: 复古怀旧 - 潮流
    - pop: 活力四射 - 炫酷
    - notion: 手绘线稿 - 知性
    - modern: 现代渐变 - 科技
    - elegant: 优雅精致 - 商务

    支持布局:
    - sparse: 稀疏布局 (1-2个要点)
    - balanced: 平衡布局 (3-4个要点)
    - dense: 密集布局 (5-8个要点)
    - list: 列表布局 (4-7项)
    - comparison: 对比布局
    - flow: 流程布局
    """

    # 风格配置 (颜色和CSS)
    STYLES: Dict = {}

    def __init__(self):
        self.aliyun_key = os.getenv('ALIYUN_API_KEY')
        self.nano_key = os.getenv('NANO_BANANA_API_KEY')
        self._init_styles()

    def _init_styles(self):
        """初始化所有风格配置"""
        font_import = '''
        @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&family=ZCOOL+KuaiLe&family=Ma+Shan+Zheng&display=swap');
        '''

        self.STYLES = {
            # 甜美可爱 - 经典小红书风格
            'cute': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'ZCOOL KuaiLe', 'Noto Sans SC', -apple-system, sans-serif;
                    background: linear-gradient(135deg, #FFE4EC 0%, #FFF0F5 50%, #E8F5E9 100%);
                    min-height: {{{{height}}}}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: rgba(255, 255, 255, 0.95);
                    border-radius: 32px;
                    padding: 44px;
                    max-width: {{{{width}}}}px;
                    box-shadow: 0 20px 40px rgba(255, 105, 180, 0.2);
                    border: 3px solid #FFB6C1;
                    position: relative;
                    overflow: hidden;
                }}
                .card::before {{
                    content: '✨';
                    position: absolute;
                    top: 20px;
                    right: 20px;
                    font-size: 24px;
                }}
                .card h1 {{
                    font-size: 34px;
                    font-weight: 700;
                    color: #FF69B4;
                    margin-bottom: 14px;
                    text-shadow: 2px 2px 0px #FFF0F5;
                }}
                .card p {{
                    font-size: 17px;
                    color: #8B7355;
                    line-height: 1.7;
                }}
                .tag {{
                    display: inline-block;
                    background: linear-gradient(135deg, #FF69B4 0%, #FFB6C1 100%);
                    color: white;
                    padding: 8px 20px;
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: 600;
                    margin-bottom: 16px;
                }}
                .decoration {{
                    position: absolute;
                    font-size: 20px;
                    opacity: 0.6;
                }}
            ''',

            # 清新自然
            'fresh': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Ma Shan Zheng', 'Noto Sans SC', -apple-system, sans-serif;
                    background: linear-gradient(135deg, #E8F5E9 0%, #E3F2FD 50%, #FFF8E1 100%);
                    min-height: {{{{height}}}}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: rgba(255, 255, 255, 0.9);
                    border-radius: 20px;
                    padding: 48px;
                    max-width: {{{{width}}}}px;
                    box-shadow: 0 15px 35px rgba(76, 175, 80, 0.15);
                    border-left: 5px solid #81C784;
                }}
                .card h1 {{
                    font-size: 32px;
                    font-weight: 600;
                    color: #2E7D32;
                    margin-bottom: 16px;
                }}
                .card p {{
                    font-size: 17px;
                    color: #558B2F;
                    line-height: 1.8;
                }}
                .tag {{
                    display: inline-block;
                    background: #81C784;
                    color: white;
                    padding: 6px 16px;
                    border-radius: 15px;
                    font-size: 12px;
                    font-weight: 500;
                }}
            ''',

            # 温暖友好
            'warm': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Poppins', 'Noto Sans SC', -apple-system, sans-serif;
                    background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 50%, #FFCC80 100%);
                    min-height: {{{{height}}}}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: #FFF8E1;
                    border-radius: 24px;
                    padding: 48px;
                    max-width: {{{{width}}}}px;
                    box-shadow: 0 20px 40px rgba(255, 152, 0, 0.2);
                    border: 2px solid #FFB74D;
                }}
                .card h1 {{
                    font-size: 34px;
                    font-weight: 600;
                    color: #E65100;
                    margin-bottom: 16px;
                }}
                .card p {{
                    font-size: 18px;
                    color: #795548;
                    line-height: 1.7;
                }}
                .tag {{
                    display: inline-block;
                    background: linear-gradient(135deg, #FF9800 0%, #FFB74D 100%);
                    color: white;
                    padding: 8px 18px;
                    border-radius: 18px;
                    font-size: 13px;
                    font-weight: 600;
                }}
            ''',

            # 高冲击力
            'bold': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Space Grotesk', 'Noto Sans SC', -apple-system, sans-serif;
                    background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%);
                    min-height: {{{{height}}}}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: linear-gradient(135deg, #E94560 0%, #FF6B6B 100%);
                    border-radius: 16px;
                    padding: 48px;
                    max-width: {{{{width}}}}px;
                    box-shadow: 0 30px 60px rgba(233, 69, 96, 0.4);
                }}
                .card h1 {{
                    font-size: 38px;
                    font-weight: 700;
                    color: #FFFFFF;
                    margin-bottom: 16px;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                }}
                .card p {{
                    font-size: 18px;
                    color: rgba(255, 255, 255, 0.9);
                    line-height: 1.6;
                }}
                .tag {{
                    display: inline-block;
                    background: #FFFFFF;
                    color: #E94560;
                    padding: 8px 20px;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: 700;
                    text-transform: uppercase;
                }}
            ''',

            # 极简精致
            'minimal': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Helvetica Neue', 'Noto Sans SC', Arial, sans-serif;
                    background: #FAFAFA;
                    min-height: {{{{height}}}}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: #FFFFFF;
                    border-radius: 8px;
                    padding: 48px;
                    max-width: {{{{width}}}}px;
                    border: 1px solid #E0E0E0;
                }}
                .card h1 {{
                    font-size: 28px;
                    font-weight: 500;
                    color: #212121;
                    margin-bottom: 16px;
                    letter-spacing: -0.5px;
                }}
                .card p {{
                    font-size: 15px;
                    color: #757575;
                    line-height: 1.7;
                }}
            ''',

            # 复古怀旧
            'retro': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Courier New', 'Noto Sans SC', monospace;
                    background: linear-gradient(135deg, #D4A574 0%, #C19A6B 50%, #8B7355 100%);
                    min-height: {{{{height}}}}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: #FFF8DC;
                    border-radius: 4px;
                    padding: 48px;
                    max-width: {{{{width}}}}px;
                    box-shadow: 0 15px 30px rgba(139, 115, 85, 0.3);
                    border: 3px double #8B7355;
                    transform: rotate(-1deg);
                }}
                .card h1 {{
                    font-size: 30px;
                    font-weight: 700;
                    color: #5D4037;
                    margin-bottom: 16px;
                    text-decoration: underline;
                    text-decoration-style: wavy;
                    text-decoration-color: #FFB74D;
                }}
                .card p {{
                    font-size: 16px;
                    color: #6D4C41;
                    line-height: 1.7;
                }}
                .tag {{
                    display: inline-block;
                    background: #8D6E63;
                    color: white;
                    padding: 6px 14px;
                    border-radius: 2px;
                    font-size: 12px;
                    font-weight: 600;
                }}
            ''',

            # 活力四射
            'pop': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Poppins', 'Noto Sans SC', -apple-system, sans-serif;
                    background: linear-gradient(135deg, #FF0080 0%, #FF8C00 50%, #FFE500 100%);
                    min-height: {{{{height}}}}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: #FFFFFF;
                    border-radius: 20px;
                    padding: 48px;
                    max-width: {{{{width}}}}px;
                    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
                    transform: rotate(1deg);
                }}
                .card h1 {{
                    font-size: 36px;
                    font-weight: 800;
                    color: #FF0080;
                    margin-bottom: 16px;
                    text-transform: uppercase;
                }}
                .card p {{
                    font-size: 18px;
                    color: #333333;
                    line-height: 1.6;
                }}
                .tag {{
                    display: inline-block;
                    background: #FF0080;
                    color: white;
                    padding: 8px 20px;
                    border-radius: 0;
                    font-size: 14px;
                    font-weight: 700;
                }}
            ''',

            # 手绘线稿 - 知性
            'notion': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Noto Sans SC', -apple-system, sans-serif;
                    background: #F5F5F5;
                    min-height: {{{{height}}}}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: #FFFFFF;
                    border-radius: 12px;
                    padding: 48px;
                    max-width: {{{{width}}}}px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                    border: 1px solid #E0E0E0;
                }}
                .card h1 {{
                    font-size: 28px;
                    font-weight: 600;
                    color: #37352F;
                    margin-bottom: 16px;
                    padding-bottom: 12px;
                    border-bottom: 2px solid #37352F;
                }}
                .card p {{
                    font-size: 15px;
                    color: #787774;
                    line-height: 1.8;
                }}
                .tag {{
                    display: inline-block;
                    background: #EBECED;
                    color: #787774;
                    padding: 4px 12px;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: 500;
                }}
            ''',

            # 现代渐变
            'modern': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Space Grotesk', 'Noto Sans SC', -apple-system, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: {{{{height}}}}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: rgba(255, 255, 255, 0.95);
                    border-radius: 24px;
                    padding: 48px;
                    max-width: {{{{width}}}}px;
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
                }}
                .card h1 {{
                    font-size: 36px;
                    font-weight: 700;
                    color: #1e293b;
                    margin-bottom: 16px;
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
                }}
            ''',

            # 优雅精致
            'elegant': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Archivo', 'Noto Sans SC', -apple-system, serif;
                    background: linear-gradient(145deg, #f5f5f5 0%, #e8e8e8 100%);
                    min-height: {{{{height}}}}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 40px;
                }}
                .card {{
                    background: #ffffff;
                    border-radius: 16px;
                    padding: 56px;
                    max-width: {{{{width}}}}px;
                    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
                    border-left: 4px solid #1a1a1a;
                }}
                .card h1 {{
                    font-size: 32px;
                    font-weight: 600;
                    color: #1a1a1a;
                    margin-bottom: 20px;
                    letter-spacing: -0.5px;
                }}
                .card p {{
                    font-size: 16px;
                    color: #6b7280;
                    line-height: 1.8;
                }}
                .accent {{
                    width: 60px;
                    height: 4px;
                    background: #1a1a1a;
                    margin-bottom: 24px;
                }}
            ''',

            # 深色科技
            'dark': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Space Grotesk', 'Noto Sans SC', -apple-system, sans-serif;
                    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
                    min-height: {{{{height}}}}px;
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
                    max-width: {{{{width}}}}px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }}
                .card h1 {{
                    font-size: 36px;
                    font-weight: 700;
                    color: #f8fafc;
                    margin-bottom: 16px;
                }}
                .card p {{
                    font-size: 18px;
                    color: #94a3b8;
                    line-height: 1.7;
                }}
            ''',

            # 毛玻璃
            'glass': f'''
                {font_import}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Poppins', 'Noto Sans SC', -apple-system, sans-serif;
                    background: linear-gradient(135deg, #a855f7 0%, #3b82f6 50%, #06b6d4 100%);
                    min-height: {{{{height}}}}px;
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
                    max-width: {{{{width}}}}px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }}
                .card h1 {{
                    font-size: 34px;
                    font-weight: 600;
                    color: #ffffff;
                    margin-bottom: 16px;
                }}
                .card p {{
                    font-size: 17px;
                    color: rgba(255, 255, 255, 0.85);
                    line-height: 1.7;
                }}
            ''',
        }

    def get_available_styles(self) -> List[str]:
        """获取所有可用的风格"""
        return list(self.STYLES.keys())

    def html_to_screenshot(self, content: str, style: str = 'modern',
                          width: int = 800, height: int = 600) -> str:
        """
        HTML布局截图模式

        Args:
            content: HTML内容
            style: 风格模板
            width: 图片宽度
            height: 图片高度

        Returns:
            截图的base64编码 (PNG格式)
        """
        html_template = self._generate_html(content, style, width, height)

        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.set_content(html_template, wait_until='networkidle')
                page.set_viewport_size({'width': width, 'height': height})
                screenshot = page.screenshot(type='png')
                browser.close()
                return base64.b64encode(screenshot).decode('utf-8')
        except ImportError:
            raise RuntimeError(
                "Playwright not installed. Run: pip install playwright && playwright install chromium "
                "Or use ai_gen mode with ALIYUN_API_KEY configured."
            )
        except Exception as e:
            raise RuntimeError(f"Screenshot failed: {e}")

    def save_html_file(self, content: str, style: str = 'modern',
                       width: int = 800, height: int = 600) -> str:
        """保存HTML到临时文件"""
        html_template = self._generate_html(content, style, width, height)

        fd, path = tempfile.mkstemp(suffix='.html', prefix='xhs_image_')
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(html_template)

        return path

    def ai_generate(self, prompt: str, api: str = 'aliyun') -> str:
        """AI生图模式"""
        if api == 'aliyun':
            return self._aliyun_generate(prompt)
        elif api == 'nano_banana':
            return self._nano_banana_generate(prompt)
        else:
            raise ValueError(f"不支持的API: {api}")

    def _generate_html(self, content: str, style: str, width: int, height: int) -> str:
        """生成HTML模板"""
        # 获取风格CSS，替换占位符
        base_css = self.STYLES.get(style, self.STYLES['modern'])
        css = base_css.replace('{{height}}', str(height)).replace('{{width}}', str(width))

        # 处理内容容器
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
        """阿里云通义万相API调用"""
        print(f"[ImageDesigner] Calling Aliyun API with prompt: {prompt[:50]}...")
        return f"https://example.com/generated_image_{hash(prompt)}.jpg"

    def _nano_banana_generate(self, prompt: str) -> str:
        """nano banana pro API调用"""
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
            style: 风格模板
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
    designer = ImageDesigner()

    print("Available styles:", designer.get_available_styles())

    # Test all styles
    test_styles = ['cute', 'fresh', 'warm', 'bold', 'minimal', 'retro', 'pop', 'notion', 'modern', 'elegant', 'dark', 'glass']

    content = """
        <span class="tag">推荐</span>
        <h1>AI工具推荐</h1>
        <p>这5个神器让你的效率翻倍！</p>
    """

    for style in test_styles:
        try:
            # Just generate HTML, don't screenshot in test
            html = designer._generate_html(content, style, 800, 600)
            print(f"{style}: {len(html)} chars HTML generated")
        except Exception as e:
            print(f"{style}: Error - {e}")
