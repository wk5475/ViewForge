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
from tools.img_generate_tools import get_img_tools
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
        self.img_tools = get_img_tools()

        self.article_dir = os.path.join(root_path, output_dir)
        os.makedirs(self.article_dir, exist_ok=True)


    def run(self, input_text: str, context_type:str) -> str:
        """运行Agent处理用户输入"""
        logger.info(f"🚀 启动 {self.name}，处理用户输入...")

        try:
            # 1. 搜索相关内容
            search_results = self._search_content(input_text)
            logger.info(f"✅ 搜索完成，找到 {len(search_results)} 个相关结果")

            # 2. 生成爆文
            article_content = self._generate_article(input_text, context_type, search_results)
            logger.info("✅ 爆文生成完成")

            # # 3. 生成配图
            # image_url = self._generate_image(input_text, context_type)
            # logger.info(f"✅ 配图生成完成：{image_url}")
            image_url = "https://example.com/default_image.jpg"  # 使用默认图片URL

            # 4. 格式化为markdown
            markdown_output = self._format_to_markdown(article_content, image_url, search_results)
            logger.info("✅ Markdown格式转换完成")

            # 5. 保存文章
            save_path = self._save_article(markdown_output)
            logger.info(f"✅ 文章保存完成：{save_path}")

            logger.info("✅ Agent运行完成")
            return markdown_output
        except Exception as e:
            logger.error(f"❌ Agent运行失败: {e}")
            return f"生成失败: {str(e)}"


    def _search_content(self, content: str) -> str:
        """搜索相关内容"""
        return self.search_tool.search(content)

    def _generate_article(self, content: str, domain: str, search_results: str) -> str:
        """生成爆文"""
        
        # 构建prompt
        messages = [
            {
                "role": "system",
                "content": "你是一名专业的头条爆文撰写专家，擅长撰写吸引人的标题和内容。请根据提供的主题和相关信息，生成一篇符合头条风格的爆文。"
            },
            {
                "role": "user",
                "content": f"请根据以下主题和相关信息，生成一篇头条爆文："
                           f"主题：{content} 领域：{domain} 相关信息：{search_results}"
                           f"要求："
                           f"1. 标题要吸引人，使用感叹号或问号等标点增强语气"
                           f"2. 内容要生动有趣，符合头条风格"
                           f"3. 结构清晰，有开头、中间和结尾"
                           f"4. 结合最新信息，突出热点"
                           f"5. 语言简洁明了，避免使用复杂词汇"
                           f"6. 字数控制在800-1200字之间"
            }
        ]
        
        return self.llm.think(messages, temperature=0.7)

    def _generate_image(self, content: str, domain: str) -> str:
        """生成配图"""
        return self.img_tools.run(content, domain)

    def _format_to_markdown(self, article_content: str, image_path: str, search_results: str) -> str:
        """格式化为markdown"""
        lines = article_content.split('\n')
        markdown = "# " + lines[0] + "\n\n"
        
        # 处理图片路径
        if image_path.startswith('http'):
            # 如果是 URL，直接使用
            markdown += "![配图]('" + image_path + "')\n\n"
        else:
            # 如果是本地路径，调整为相对路径（相对于 articles 目录）
            image_rel_path = "../" + image_path
            markdown += "![配图]('" + image_rel_path + "')\n\n"
        
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
    test_input = "最近黄金走势怎么样，对未来有什么预测？"
    result = agent.run(test_input, context_type="财经")
    print("=== Agent运行测试结果 ===")
    print(result)