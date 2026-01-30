#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/30 15:44
# @Author  : wang ke
# @File    : viewforge_agent.py
# @Software: PyCharm

import json
from typing import Any, Dict, List

from core.llm import LLM
from core.config import get_config
from tools.search_tools import get_search_tool
from utils.log import Log

logger = Log()


class ViewForgeAgent:
    """ViewForge Agent实现"""

    def __init__(self, name: str):
        self.name = name
        config = get_config()
        self.llm = LLM(
            model=config.openai_model,
            apikey=config.openai_api_key,
            baseurl=config.openai_base_url
        )

        self.search_tool = get_search_tool()


    def run(self, input_text: str) -> str:
        """运行Agent处理用户输入"""
        logger.info(f"🚀 启动 {self.name}，处理用户输入...")

        # 步骤1：分析用户输入，判断是否需要搜索
        needs_search, search_query = self._analyze_input_needs_search(input_text)

        # 步骤2：执行搜索（如果需要）
        search_results = []
        if needs_search and search_query:
            search_results = self._execute_search(search_query)

        # 步骤3：生成响应，判断是否需要插图
        final_response, needs_illustration = self._generate_response(
            input_text, search_results
        )

        logger.info("✅ Agent运行完成")
        return final_response


    def _analyze_input_needs_search(self, input_text: str):
        """分析用户输入是否需要搜索"""
        logger.info("🧠 分析用户输入是否需要搜索...")

        messages = [
            {
                "role": "system",
                "content": "你是一个智能助手，需要分析用户的输入是否需要使用搜索工具获取信息。\n"
                           "请根据以下标准判断：\n"
                           "1. 如果用户的问题涉及事实性信息、当前事件、具体数据或需要最新信息，请返回需要搜索\n"
                           "2. 如果用户的问题是关于创意写作、个人建议、一般性知识或不需要实时信息的，请返回不需要搜索\n"
                           "\n"
                           "请以JSON格式返回你的判断结果：\n"
                           "{\"needs_search\": true/false, \"search_query\": \"搜索查询词\"}\n"
                           "其中search_query是根据用户输入生成的合适搜索词，如果不需要搜索则为空字符串"
            },
            {
                "role": "user",
                "content": input_text
            }
        ]

        response = self.llm.think(messages)

        try:
            analysis_result = json.loads(response)
            needs_search = analysis_result.get("needs_search", False)
            search_query = analysis_result.get("search_query", "")
        except:
            logger.error("❌ 解析LLM响应失败，默认不需要搜索")
            needs_search = False
            search_query = ""

        logger.info(f"✅ 分析结果：需要搜索={needs_search}")
        return needs_search, search_query


    def _execute_search(self, search_query: str, max_results: int = 5) -> List[Dict]:
        """执行搜索"""
        logger.info(f"🔍 执行搜索：{search_query}")
        return self.search_tool.search(search_query, max_results)


    def _generate_response(self, input_text: str, search_results: List[Dict]):
        """生成响应，判断是否需要插图"""
        logger.info("📝 生成响应...")

        # 构建上下文
        context = ""
        if search_results:
            context = "搜索结果：\n"
            for i, result in enumerate(search_results, 1):
                context += f"{i}. 标题：{result['title']}\n"
                context += f"链接：{result['url']}\n"
                context += f"内容：{result['content'][:200]}...\n\n"

        messages = [
            {
                "role": "system",
                "content": "你是一个智能助手，需要根据用户输入和可能的搜索结果生成最终响应。\n"
                           "请遵循以下要求：\n"
                           "1. 如果有搜索结果，请结合搜索结果提供准确的信息\n"
                           "2. 保持回答的风格与用户输入的风格一致\n"
                           "3. 判断回答是否需要插图（例如：需要展示数据、场景描述、人物形象等）\n"
                           "4. 请以JSON格式返回你的回答和判断结果：\n"
                           "{\"response\": \"你的回答\", \"needs_illustration\": true/false}\""
            },
            {
                "role": "user",
                "content": f"用户输入:{input_text}。检索的内容:{context}"
            }
        ]

        response = self.llm.think(messages)

        try:
            result = json.loads(response)
            final_response = result.get("response", "")
            needs_illustration = result.get("needs_illustration", False)
        except:
            logger.error("❌ 解析LLM响应失败")
            final_response = response or ""
            needs_illustration = False

        logger.info(f"✅ 响应生成完成，需要插图={needs_illustration}")
        return final_response, needs_illustration


# 全局Agent实例
viewforge_agent = ViewForgeAgent("ViewForge Agent")


def get_agent() -> ViewForgeAgent:
    """获取ViewForge Agent实例"""
    return viewforge_agent