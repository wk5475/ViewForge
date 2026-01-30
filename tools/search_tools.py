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
        
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """执行搜索
        
        Args:
            query: 搜索查询字符串
            max_results: 返回的最大结果数
            
        Returns:
            搜索结果列表，每个结果包含标题、链接和摘要
        """
        if not self.tavily_api_key:
            logger.error("❌ 未配置Tavily API密钥")
            return []
        
        try:
            import tavily
            
            client = tavily.TavilyClient(api_key=self.tavily_api_key)
            results = client.search(
                query=query,
                max_results=max_results,
                include_answer=True,
                include_raw_content=False,
                include_images=False
            )
            
            logger.info(f"✅ 搜索完成，找到 {len(results.results)} 个结果")
            
            # 格式化结果
            formatted_results = []
            for result in results.results:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", "")
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"❌ 搜索时发生错误: {e}")
            return []

# 全局搜索工具实例
search_tool = SearchTool()

def get_search_tool() -> SearchTool:
    """获取搜索工具实例"""
    return search_tool