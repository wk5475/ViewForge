#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/2/4 15:37
# @Author  : wang ke
# @File    : generate_article.py
# @Software: PyCharm

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from services.viewforge_services import call_viewforge_api
from utils.log import Log

logger = Log()

router = APIRouter()

# 定义请求模型
class ArticleRequest(BaseModel):
    input_text: str
    context_type: Optional[str] = "通用"
    style: Optional[str] = None
    platform: Optional[str] = None

# 定义响应模型
class ArticleResponse(BaseModel):
    success: bool
    message: str
    saved_path: Optional[str] = None
    error: Optional[str] = None

@router.post("/generate_article", response_model=ArticleResponse)
async def generate_article(request: ArticleRequest):
    """
    生成爆文API

    Args:
        request: 包含用户输入文本和其他可选参数的请求

    Returns:
        包含生成结果的响应
    """
    try:
        logger.info(f"用户请求：{request.input_text}")
        # 调用服务生成文章
        result = call_viewforge_api(
            user_text=request.input_text,
            style=request.style,
            context_type=request.context_type,
            platform=request.platform
        )

        # 检查是否有错误
        if "error" in result:
            return ArticleResponse(
                success=False,
                message="生成失败",
                error=result["error"]
            )

        # 返回成功响应
        return ArticleResponse(
            success=True,
            message="文章生成成功",
            saved_path=result.get("saved_path")
        )
    except Exception as e:
        logger.error(f"API处理失败: {e}")
        return ArticleResponse(
            success=False,
            message="API处理失败",
            error=str(e)
        )