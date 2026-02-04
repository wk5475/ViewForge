#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/30 15:44
# @Author  : wang ke
# @File    : viewforge_agent.py
# @Software: PyCharm


import os
import time
from pathlib import Path

from core.llm import LLM
from core.config import get_config
from tools.search_tools import get_search_tool
from utils.log import Log


root_path = Path(__file__).resolve().parent.parent

logger = Log()


class ViewForgeAgent:
    """ViewForge Agent实现"""

    def __init__(self, name: str, output_dir: str = "output/article"):
        self.name = name
        config = get_config()
        self.llm = LLM(
            model=config.openai_model,
            apikey=config.openai_api_key,
            baseurl=config.openai_base_url
        )

        self.search_tool = get_search_tool()

        self.article_dir = os.path.join(root_path, output_dir)
        os.makedirs(self.article_dir, exist_ok=True)


    def run(self, input_text: str, context_type:str) -> str:
        """运行Agent处理用户输入"""
        logger.info(f"🚀 启动 {self.name}，处理用户输入...")

        try:
            # 1. 搜索相关内容
            search_results = self._search_content(input_text)

            # 2. 生成爆文
            article_content = self._generate_article(input_text, context_type, search_results)


            # 5. 格式化为markdown
            markdown_output = self._format_to_markdown(article_content, search_results)


            # 6. 保存文章
            self._save_article(markdown_output)

            logger.info("✅ Agent运行完成")
            return markdown_output
        except Exception as e:
            logger.error(f"❌ Agent运行失败: {e}")
            return f"生成失败: {str(e)}"


    def _search_content(self, content: str) -> str:
        """搜索相关内容，确保获取最新资讯"""
        logger.info(f"🔍 搜索最新资讯：{content}")
        
        # 优化搜索查询，添加时间限制
        optimized_query = f"{content} 最新 最近"
        
        # 执行搜索
        search_results = self.search_tool.search(optimized_query)

        logger.info(f"✅ 搜索完成，获取到最新资讯")
        return search_results


    def _generate_article(self, content: str, domain: str, search_results: str) -> str:
        """生成爆文，确保符合头条风格"""
        logger.info(f"📝 生成头条风格文章：{content}")
        
        # 构建prompt，增强头条风格
        messages = [
            {
                "role": "system",
                "content": "你是一名顶尖的头条爆文撰写专家，精通头条平台的内容创作规律。你的文章以标题吸引人、内容有深度、结构清晰、语言生动著称，能够快速获得高阅读量和互动率。"
            },
            {
                "role": "user",
                "content": f"请根据以下主题和相关信息，生成一篇符合头条风格的爆文：\n"
                           f"主题：{content}\n"
                           f"领域：{domain}\n"
                           f"相关最新信息：{search_results}\n"
                           f"\n"
                           f"严格按照以下要求创作：\n"
                           f"1. 标题：必须引人注目，使用感叹号或问号等标点增强语气，长度控制在15-25字之间\n"
                           f"2. 开头：第一段必须抓住读者眼球，用生动的场景或问题引入主题\n"
                           f"3. 内容：\n"
                           f"   - 结构清晰，分为多个段落，每段不宜过长\n"
                           f"   - 结合最新信息，突出热点话题\n"
                           f"   - 语言口语化，避免使用复杂词汇\n"
                           f"   - 加入适当的情感表达，增强文章感染力\n"
                           f"   - 提供有价值的信息和见解\n"
                           f"4. 结尾：总结全文，给出明确的观点或建议，鼓励读者评论互动\n"
                           f"5. 字数：控制在800-1200字之间\n"
                           f"6. 风格：符合头条平台的内容风格，接地气、有温度、有态度\n"
                           f"\n"
                           f"请直接输出完整文章，不要有任何引言或开场白。"
            }
        ]
        
        article = self.llm.think(messages, temperature=0.7)
        logger.info("✅ 文章生成完成，符合头条风格")
        return article

    def _format_to_markdown(self, article_content: str, search_results: str) -> str:
        """格式化为markdown"""
        lines = article_content.split('\n')
        markdown = "# " + lines[0] + "\n\n"
        markdown += "\n".join(lines[1:]) + "\n\n"
        markdown += "## 参考资料\n"
        markdown += search_results

        return markdown

    def _save_article(self, markdown_content: str) -> str:
        """保存文章到文件"""
        # 创建输出目录

        
        # 生成文件名
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"article_{timestamp}.md"
        file_path = os.path.join(self.article_dir, filename)
        
        # 保存文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            logger.info(f"✅ 文章已保存到：{file_path}")
            return file_path
        except Exception as e:
            logger.error(f"❌ 保存文章失败: {e}")
            return None


# 全局Agent实例
viewforge_agent = ViewForgeAgent("ViewForge Agent")


def get_agent() -> ViewForgeAgent:
    """获取ViewForge Agent实例"""
    return viewforge_agent

if __name__ == "__main__":
    # 测试Agent运行
    agent = get_agent()
    test_input = "国投白银LOF修改规则的问题"
    result = agent.run(test_input, context_type="财经")
    print("=== Agent运行测试结果 ===")
    print(result)