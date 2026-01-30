#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/30 11:49
# @Author  : wang ke
# @File    : viewforge_services.py
# @Software: PyCharm

from agents.viewforge_agent import get_agent
from utils.log import Log

logger = Log()

def call_viewforge_api(user_text: str, style = None, context_type = None, platform = None):
    """
    调用ViewForge API处理用户输入
    
    Args:
        user_text: 用户输入文本
        style: 输出风格（可选）
        context_type: 内容类型（可选）
        platform: 目标平台（可选）
    Returns:
        处理结果，包含响应文本和是否需要插图的信息
    """
    logger.info(f"📞 调用ViewForge API，用户输入：{user_text}")
    
    # 获取Agent实例
    agent = get_agent()
    
    # 运行Agent
    result = agent.run(user_text)

    return result
