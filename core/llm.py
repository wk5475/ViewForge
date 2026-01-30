#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/30 11:32
# @Author  : wang ke
# @File    : llm.py
# @Software: PyCharm

from openai import OpenAI
from typing import List, Dict

from utils.time_decorator import timer_decorator
from utils.log import Log

logger = Log()

class LLM:
    """
    大语言模型客户端封装类。
    """

    def __init__(self, model: str = None, apikey: str = None, baseurl: str = None, timeout: int = 80):
        """
        初始化客户端。
        """
        self.model = model

        if not all([self.model, apikey, baseurl]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        self.client = OpenAI(api_key=apikey, base_url=baseurl, timeout=timeout)

    @timer_decorator
    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        调用大语言模型进行思考，并返回其响应。
        """
        logger.info(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )

            # 处理流式响应
            logger.info("✅ 大语言模型响应成功:")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()  # 在流式输出结束后换行
            return "".join(collected_content)

        except Exception as e:
            logger.error(f"❌ 调用LLM API时发生错误: {e}")
            return None