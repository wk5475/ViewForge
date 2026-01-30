#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/30 11:22
# @Author  : wang ke
# @File    : config.py
# @Software: PyCharm

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from dataclasses import dataclass

@dataclass
class Config:
    """Agents配置类"""

    # OpenAI 兼容 API
    openai_api_key: str = None
    openai_base_url: str = None  # 如: https://api.openai.com/v1
    openai_model: str = "gpt-4o-mini"  # OpenAI 兼容模型名称
    openai_temperature: float = 0.7  # OpenAI 温度参数（0.0-2.0，默认0.7）

    # === 搜索引擎配置（支持多 Key 负载均衡）===
    tavily_api_keys: str = None  # Tavily API Keys
    serpapi_keys: str = None  # SerpAPI Keys

    # 单例实例存储
    _instance: Optional["Config"] = None

    @classmethod
    def get_instance(cls) -> 'Config':
        """
        获取配置单例实例

        单例模式确保：
        1. 全局只有一个配置实例
        2. 配置只从环境变量加载一次
        3. 所有模块共享相同配置
        """
        if cls._instance is None:
            cls._instance = cls._load_from_env()
        return cls._instance

    @classmethod
    def _load_from_env(cls) -> "Config":
        """
         从 .env 文件加载配置
        """
        # 加载项目根目录下的 .env 文件
        # core/config.py -> core/ -> root
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)

        return cls(
            # OpenAI 兼容 API 配置
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_base_url=os.getenv("OPENAI_BASE_URL"),
            openai_model=os.getenv("OPENAI_MODEL"),
            # 搜索引擎 API Keys
            tavily_api_keys = os.getenv("TAVILY_API_KEYS"),
            serpapi_keys = os.getenv("SERPAPI_API_KEYS"),
        )


# === 便捷的配置访问函数 ===
def get_config() -> Config:
    """获取全局配置实例的快捷方式"""
    return Config.get_instance()

if __name__ == "__main__":
    # 测试配置加载
    config = get_config()
    print("=== 配置加载测试 ===")
    print(f"OpenAI API Key: {config.openai_api_key}")
