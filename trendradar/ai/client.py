# coding=utf-8

import os
import requests
from typing import Any, Dict, List


class AIClient:
    """Dify 原生 API 客户端（无 OpenAI，无 LiteLLM，绝对不 404）"""

    def __init__(self, config: Dict[str, Any]):
        # 全小写读取配置（和你项目一致）
        # self.model = config.get("model", "")
        # self.api_key = config.get("api_key", "")
        # self.api_base = config.get("api_base", "").rstrip("/")
        # self.user_id = config.get("user_id", "trendradar_user")
        # self.temperature = config.get("temperature", 0.3)
        # self.max_tokens = config.get("max_tokens", 2048)
        # self.timeout = config.get("timeout", 60)

        self.model = config.get("MODEL", "")
        self.api_key = config.get("API_KEY", "")
        self.api_base = config.get("API_KEY", "").rstrip("/")
        self.user_id = config.get("USER_ID", "trendradar_user")
        self.temperature = config.get("TEMPERATURE", 0.3)
        self.max_tokens = config.get("MAX_TOKENS", 2048)
        self.timeout = config.get("TIMEOUT", 60)

        # 【Dify 真实接口】这是你后台显示的正确地址！
        self.dify_api_url = "http://101.201.37.148/v1/chat-messages"

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """调用 Dify 原生 API（你自己平时用的方式）"""
        print(f"[Dify 原生API] 请求地址: {self.dify_api_url}")

        # 拼接最后一轮用户消息
        user_query = messages[-1]["content"] if messages else "你好"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "inputs": {},
            "query": user_query,
            "response_mode": "blocking",
            "user": self.user_id
        }

        try:
            response = requests.post(
                self.dify_api_url,
                headers=headers,
                json=data,
                timeout=self.timeout
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            result = response.json()
            return result.get("answer", "无返回内容")

        except Exception as e:
            raise Exception(f"Dify 调用失败: {str(e)}") from e

    def validate_config(self) -> tuple[bool, str]:
        if not self.api_key:
            return False, "Dify API Key 不能为空"
        return True, ""
