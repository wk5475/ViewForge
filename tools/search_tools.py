#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/30 14:00
# @Author  : wang ke
# @File    : search_tools.py
# @Software: PyCharm

from typing import List, Dict, Optional
import os
from core.config import get_config
from utils.log import Log

logger = Log()

class SearchTool:
    """搜索工具类"""
    
    def __init__(self):
        self.config = get_config()
        self.tavily_api_key = self.config.tavily_api_keys
        self.serpapi_key = self.config.serpapi_keys
        self.max_results = 3

    def search(self, query: str):
        """执行智能搜索"""

        try:
            if not query.strip():
                logger.error(f"搜索查询为空，无法执行搜索。")

            if not any([self.tavily_api_key, self.serpapi_key]):
                logger.error("⚠️ 未配置任何搜索引擎API Key，无法执行搜索。")

            if self.tavily_api_key:
                result = self._search_with_tavily(query)
                if result and "未找到" not in result:
                    return result

            elif self.serpapi_key:
                result = self._search_with_serpapi(query)
                if result and "未找到" not in result:
                    return result

        except Exception as e:
            logger.error(f"❌ 搜索时发生错误: {e}")
            return ""


    def _search_with_tavily(self, query: str) -> str:
        """使用Tavily搜索"""
        from tavily import TavilyClient

        tavily_client = TavilyClient(self.tavily_api_key)
        response = tavily_client.search(
            query=query,
            max_results=self.max_results
            )

        if response.get('answer'):
            result = f"AI直接答案:{response['answer']}\n\n"
        else:
            result = ""

        result += "相关结果:\n"
        for i, item in enumerate(response.get('results', [])[:3], 1):
            result += f"[{i}] {item.get('title', '')}\n"
            result += f"{item.get('content', '')[:150]}...\n\n"

        return result

    def _search_with_serpapi(self, query: str) -> str:
        """使用SerpApi搜索"""
        import serpapi

        search = serpapi.search(
            q=query,
            engine="google",
            api_key=self.serpapi_key,
            num=self.max_results
        )

        results = search.as_dict()

        result = "Google搜索结果:\n"
        if "organic_results" in results:
            for i, res in enumerate(results["organic_results"][:3], 1):
                result += f"[{i}] {res.get('title', '')}\n"
                result += f"    {res.get('snippet', '')}\n\n"

        return result

# 全局搜索工具实例
search_tool = SearchTool()

def get_search_tool() -> SearchTool:
    """获取搜索工具实例"""
    return search_tool