import os
import json
import time
import random
from typing import List, Dict, Optional


class XiaohongshuPublisher:
    """发布模块 - 自动发布小红书笔记"""

    def __init__(self, mock_mode: bool = False):
        self.username = os.getenv('XHS_USERNAME')
        self.password = os.getenv('XHS_PASSWORD')
        self.cookie = os.getenv('XHS_COOKIE')
        self.session = None
        # 允许测试时启用mock模式
        self._mock_mode = mock_mode

    def login(self) -> bool:
        """
        登录小红书账号

        Returns:
            bool: 登录是否成功

        Raises:
            ValueError: 未配置任何登录凭证
        """
        if self._mock_mode:
            print("[Publisher] Mock mode enabled - skipping credential check")
            return True

        if self.cookie:
            print("[Publisher] Using cookie for authentication")
            # TODO: 验证cookie有效性
            return True

        if self.username and self.password:
            print(f"[Publisher] Login with username: {self.username}")
            # TODO: 实现账号密码登录
            # 可以使用Selenium或API调用
            return True

        # 无凭证时返回False而非假成功
        print("[Publisher] ERROR: No credentials provided")
        return False

    def upload_image(self, image_data: str) -> str:
        """
        上传图片到小红书

        Args:
            image_data: 图片数据 (base64或URL)

        Returns:
            上传后的图片ID
        """
        # TODO: 实现真实的上传API
        # 小红书图片上传API:
        # POST https://www.xiaohongshu.com/api/sns/web/v1/upload/image

        # 模拟上传
        if image_data.startswith('http'):
            print(f"[Publisher] Uploading image from URL: {image_data[:50]}...")
        else:
            print(f"[Publisher] Uploading base64 image ({len(image_data)} chars)")

        # 返回模拟图片ID
        time.sleep(0.5)  # 模拟上传延迟
        return f"img_{random.randint(100000, 999999)}"

    def publish(self, title: str, content: str,
                images: Optional[List[str]] = None,
                topics: Optional[List[str]] = None) -> Dict:
        """
        发布笔记到小红书

        Args:
            title: 笔记标题
            content: 笔记正文
            images: 图片列表
            topics: 话题标签列表

        Returns:
            发布结果
        """
        if images is None:
            images = []
        if topics is None:
            topics = []

        # 1. 登录
        if not self.login():
            return {
                "success": False,
                "message": "登录失败"
            }

        # 2. 上传图片
        image_ids = []
        for i, img in enumerate(images):
            print(f"[Publisher] Uploading image {i+1}/{len(images)}")
            img_id = self.upload_image(img)
            image_ids.append(img_id)

        # 3. 构建发布数据
        payload = {
            "title": title,
            "desc": content,
            "images": image_ids,
            "topics": topics,
            "type": "normal",
            "privacy": "public"
        }

        # 4. 调用发布API
        # TODO: 实现真实的发布API
        # POST https://www.xiaohongshu.com/api/sns/web/v1/feed

        print(f"[Publisher] Publishing note: {title}")

        # 模拟发布成功
        note_id = f"note_{random.randint(100000000, 999999999)}"
        note_url = f"https://www.xiaohongshu.com/explore/{note_id}"

        return {
            "success": True,
            "note_id": note_id,
            "note_url": note_url,
            "message": "发布成功"
        }

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
        # TODO: 实现笔记更新API
        print(f"[Publisher] Updating note: {note_id}")
        return {
            "success": True,
            "message": "更新成功"
        }

    def delete_note(self, note_id: str) -> Dict:
        """
        删除笔记

        Args:
            note_id: 笔记ID

        Returns:
            删除结果
        """
        # TODO: 实现笔记删除API
        print(f"[Publisher] Deleting note: {note_id}")
        return {
            "success": True,
            "message": "删除成功"
        }


if __name__ == "__main__":
    # 测试代码
    publisher = XiaohongshuPublisher()

    result = publisher.publish(
        title="AI工具推荐 | 5个效率神器",
        content="姐妹们！今天分享5个我最近发现的AI神器...\n\n#AI工具 #效率神器 #好物分享",
        images=["base64_image_data_1", "base64_image_data_2"],
        topics=["#AI工具", "#效率神器"]
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
