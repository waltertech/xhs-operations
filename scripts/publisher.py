"""
小红书发布模块

提供小红书笔记的自动发布功能。
支持Cookie登录、图片上传、笔记发布等操作。

使用方式:
    from scripts.publisher import XiaohongshuPublisher
    
    publisher = XiaohongshuPublisher()
    result = publisher.publish(title="标题", content="正文", images=["base64或URL"])
"""
import json
import logging
import os
import time
import random
import base64
from typing import List, Dict, Optional
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class XiaohongshuPublisher:
    """小红书发布模块 - 自动发布笔记"""

    # API端点
    UPLOAD_URL = "https://www.xiaohongshu.com/api/sns/web/v1/upload/image"
    PUBLISH_URL = "https://www.xiaohongshu.com/api/sns/web/v1/feed"
    USER_INFO_URL = "https://www.xiaohongshu.com/api/sns/web/v1/user/otherinfo"

    def __init__(self, cookie: str = None, mock_mode: bool = False):
        """
        初始化发布器
        
        Args:
            cookie: 小红书Cookie (可选，默认从环境变量读取)
            mock_mode: 是否使用模拟模式 (用于测试)
        """
        self.cookie = cookie or os.getenv('XHS_COOKIE')
        self.username = os.getenv('XHS_USERNAME')
        self.password = os.getenv('XHS_PASSWORD')
        self.mock_mode = mock_mode
        self.session = None
        self.user_info = None
        
        logger.info(f"发布器初始化: mock_mode={mock_mode}, has_cookie={bool(self.cookie)}")

    def _get_headers(self, include_auth: bool = True) -> Dict:
        """获取请求头"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://www.xiaohongshu.com/",
            "Origin": "https://www.xiaohongshu.com",
            "Content-Type": "application/json"
        }
        
        if include_auth and self.cookie:
            headers["Cookie"] = self.cookie
            
        return headers

    def check_auth(self) -> Dict:
        """
        检查认证状态
        
        Returns:
            认证状态信息
        """
        if self.mock_mode:
            logger.info("Mock模式: 跳过认证检查")
            return {"authenticated": True, "mock": True}
        
        if not self.cookie:
            logger.warning("未配置Cookie")
            return {"authenticated": False, "reason": "no_cookie"}
        
        try:
            import requests
            response = requests.get(
                self.USER_INFO_URL,
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.user_info = data.get("data", {})
                    logger.info(f"认证成功: {self.user_info.get('nickname', 'unknown')}")
                    return {"authenticated": True, "user": self.user_info}
            
            logger.warning(f"认证失败: {response.status_code}")
            return {"authenticated": False, "reason": "invalid_cookie"}
            
        except ImportError:
            logger.warning("requests库未安装")
            return {"authenticated": False, "reason": "no_requests"}
        except Exception as e:
            logger.error(f"认证检查失败: {e}")
            return {"authenticated": False, "reason": str(e)}

    def upload_image(self, image_data: str) -> Dict:
        """
        上传图片到小红书
        
        Args:
            image_data: 图片数据 (base64字符串或URL)
            
        Returns:
            上传结果，包含图片ID和URL
        """
        logger.info(f"上传图片: {'URL' if image_data.startswith('http') else 'base64数据'}")
        
        if self.mock_mode:
            time.sleep(0.3)  # 模拟上传延迟
            mock_result = {
                "success": True,
                "image_id": f"img_{random.randint(100000, 999999)}",
                "file_id": f"file_{random.randint(1000000, 9999999)}",
                "width": 1080,
                "height": 1440,
                "url": f"https://ci.xiaohongshu.com/mock_image_{random.randint(1,100)}.jpg"
            }
            logger.info(f"Mock图片上传成功: {mock_result['image_id']}")
            return mock_result
        
        try:
            import requests
            
            # 处理不同类型的图片数据
            if image_data.startswith('http'):
                # 下载远程图片
                img_response = requests.get(image_data, timeout=30)
                image_bytes = img_response.content
                file_name = image_data.split('/')[-1].split('?')[0] or 'image.jpg'
            else:
                # base64解码
                image_bytes = base64.b64decode(image_data)
                file_name = f"image_{int(time.time())}.jpg"
            
            # 构建上传表单
            files = {
                'file': (file_name, image_bytes, 'image/jpeg')
            }
            
            # 发送上传请求
            response = requests.post(
                self.UPLOAD_URL,
                files=files,
                headers=self._get_headers(),
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("data", {})
                    logger.info(f"图片上传成功: {result.get('file_id')}")
                    return {"success": True, **result}
            
            logger.error(f"图片上传失败: {response.status_code}")
            return {"success": False, "error": f"HTTP {response.status_code}"}
            
        except ImportError:
            logger.error("requests库未安装")
            return {"success": False, "error": "requests_not_installed"}
        except Exception as e:
            logger.error(f"图片上传异常: {e}")
            return {"success": False, "error": str(e)}

    def publish(self, title: str, content: str,
                images: Optional[List[str]] = None,
                topics: Optional[List[str]] = None,
                location: str = None,
                visibility: str = "public") -> Dict:
        """
        发布笔记到小红书
        
        Args:
            title: 笔记标题 (max 20字)
            content: 笔记正文 (支持emoji)
            images: 图片列表 (base64或URL，最多9张)
            topics: 话题标签列表
            location: 位置信息 (可选)
            visibility: 可见性 (public/private/friends)
            
        Returns:
            发布结果
        """
        logger.info(f"开始发布笔记: {title[:20]}...")
        
        # 参数验证
        if not title or not title.strip():
            logger.error("标题不能为空")
            return {"success": False, "error": "title_empty"}
        
        if not content or not content.strip():
            logger.error("内容不能为空")
            return {"success": False, "error": "content_empty"}
        
        if not images:
            logger.warning("未提供图片，将使用文字笔记")
            images = []
        
        if len(images) > 9:
            logger.warning(f"图片数量超过9张，取前9张")
            images = images[:9]
        
        # 1. 检查认证
        auth_status = self.check_auth()
        if not auth_status.get("authenticated"):
            if not self.mock_mode:
                return {
                    "success": False,
                    "error": "auth_failed",
                    "reason": auth_status.get("reason", "unknown")
                }
        
        # 2. 上传图片
        uploaded_images = []
        for i, img in enumerate(images):
            logger.info(f"上传图片 {i+1}/{len(images)}")
            result = self.upload_image(img)
            
            if result.get("success"):
                uploaded_images.append({
                    "file_id": result.get("file_id"),
                    "width": result.get("width", 1080),
                    "height": result.get("height", 1440)
                })
            else:
                logger.warning(f"图片 {i+1} 上传失败: {result.get('error')}")
        
        # 3. 构建发布数据
        payload = {
            "title": title[:20],  # 标题限20字
            "desc": content,
            "type": "normal",
            "hash_tag": 0,  # 是否同步到微博
            "visibility": visibility,
            "images": uploaded_images
        }
        
        # 添加话题
        if topics:
            payload["topics"] = [{"name": t.strip('#')} for t in topics if t.strip()]
        
        # 添加位置
        if location:
            payload["location"] = location
        
        # 4. 发送发布请求
        if self.mock_mode:
            time.sleep(0.5)  # 模拟发布延迟
            note_id = f"note_{random.randint(100000000, 999999999)}"
            note_url = f"https://www.xiaohongshu.com/explore/{note_id}"
            
            result = {
                "success": True,
                "note_id": note_id,
                "note_url": note_url,
                "title": title,
                "images_count": len(uploaded_images),
                "topics": topics or [],
                "mock": True,
                "message": "Mock模式发布成功"
            }
            logger.info(f"Mock发布成功: {note_id}")
            return result
        
        try:
            import requests
            
            response = requests.post(
                self.PUBLISH_URL,
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result_data = data.get("data", {})
                    note_id = result_data.get("note_id", result_data.get("note", {}).get("note_id"))
                    note_url = f"https://www.xiaohongshu.com/explore/{note_id}"
                    
                    result = {
                        "success": True,
                        "note_id": note_id,
                        "note_url": note_url,
                        "title": title,
                        "images_count": len(uploaded_images),
                        "topics": topics or [],
                        "message": "发布成功"
                    }
                    logger.info(f"发布成功: {note_id}")
                    return result
                else:
                    logger.error(f"发布失败: {data.get('msg', 'unknown')}")
                    return {"success": False, "error": data.get("msg", "publish_failed")}
            
            logger.error(f"发布请求失败: {response.status_code}")
            return {"success": False, "error": f"HTTP {response.status_code}"}
            
        except ImportError:
            logger.error("requests库未安装")
            return {"success": False, "error": "requests_not_installed"}
        except Exception as e:
            logger.error(f"发布异常: {e}")
            return {"success": False, "error": str(e)}

    def update_note(self, note_id: str, title: str = None,
                   content: str = None) -> Dict:
        """
        更新已发布的笔记
        
        Args:
            note_id: 笔记ID
            title: 新标题
            content: 新内容
            
        Returns:
            更新结果
        """
        logger.info(f"更新笔记: {note_id}")
        
        if self.mock_mode:
            return {
                "success": True,
                "note_id": note_id,
                "message": "Mock更新成功"
            }
        
        # TODO: 实现真实的更新API
        return {
            "success": False,
            "error": "update_not_implemented",
            "message": "笔记更新功能尚未实现"
        }

    def delete_note(self, note_id: str) -> Dict:
        """
        删除笔记
        
        Args:
            note_id: 笔记ID
            
        Returns:
            删除结果
        """
        logger.info(f"删除笔记: {note_id}")
        
        if self.mock_mode:
            return {
                "success": True,
                "note_id": note_id,
                "message": "Mock删除成功"
            }
        
        # TODO: 实现真实的删除API
        return {
            "success": False,
            "error": "delete_not_implemented",
            "message": "笔记删除功能尚未实现"
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书发布工具")
    parser.add_argument("--title", "-t", required=True, help="笔记标题")
    parser.add_argument("--content", "-c", required=True, help="笔记正文")
    parser.add_argument("--images", "-i", nargs="*", help="图片列表 (URL或base64)")
    parser.add_argument("--topics", nargs="*", help="话题标签")
    parser.add_argument("--mock", action="store_true", help="使用模拟模式")
    
    args = parser.parse_args()
    
    publisher = XiaohongshuPublisher(mock_mode=args.mock)
    
    result = publisher.publish(
        title=args.title,
        content=args.content,
        images=args.images,
        topics=args.topics
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
