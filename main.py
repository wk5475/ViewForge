#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/2/4 10:30
# @Author  : wang ke
# @File    : main.py
# @Software: PyCharm

from fastapi import FastAPI

from routers import generate_article
from utils.log import Log

logger = Log()

# 创建FastAPI应用
app = FastAPI(
    title="ViewForge API",
    description="用于生成爆文的API服务",
    version="1.0.0"
)

app.include_router(generate_article.router)

@app.get("/")
async def root():
    """
    根路径
    """
    return {"message": "Welcome to ViewForge API"}


if __name__ == "__main__":
    import uvicorn

    from core.config import get_config

    config = get_config()
    uvicorn.run(
        "main:app",
        host=config.api_host,
        port=config.api_port,
        reload=config.api_reload
    )
