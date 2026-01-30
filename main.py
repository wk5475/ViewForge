#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/30 10:46
# @Author  : wang ke
# @File    : main.py
# @Software: PyCharm

from services.viewforge_services import call_viewforge_api
from utils.log import Log

logger = Log()

def main():
    """主函数入口"""

    logger.info("📝 请输入您的问题或需求：")
    
    # 接收用户输入
    user_input = input()
    
    if not user_input:
        logger.error("❌ 输入为空，请重新运行程序并输入内容")
        return
    
    # 调用API处理输入
    call_viewforge_api(user_text=user_input)

if __name__ == "__main__":
    main()