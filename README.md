# 观点熔炉 / ViewForge

将海量信息锻造成独特观点的智能工具

## 🌟 项目简介

ViewForge 是一款强大的信息处理与观点生成工具，它能够：
- 分析用户意图，匹配个性化表达风格
- 实时检索并提取网页核心信息
- 自动生成相关视觉内容
- 输出排版精美的结构化 Markdown 文档

## 🚀 核心功能

### 1. 意图识别
- 分析用户输入内容和需求
- 自动匹配或询问表达风格
- 支持多种风格：专业论文感、小红书种草风、赛博朋克风、冷幽默风格等

### 2. 深度搜索
- 通过 API 实时检索网页信息
- 智能提取核心事实和关键信息
- 过滤噪声，聚焦相关内容

### 3. 视觉增强
- 根据内容自动生成相关配图
- 优化图片与文本的匹配度
- 提升文档的视觉吸引力

### 4. 结构化输出
- 生成排版精美的 Markdown 文件
- 自动组织内容结构
- 支持自定义输出格式

## 📦 安装指南

### 环境要求
- Python 3.8+
- pip 包管理工具

### 安装步骤
1. 克隆项目
   ```bash
   git clone <repository-url>
   cd ViewForge
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 配置 API 密钥
   - 复制 `.env.example` 文件为 `.env`
   - 填写相关 API 密钥

## 🎯 使用方法

### 基本使用
1. 运行主程序
   ```bash
   python main.py
   ```

2. 按照提示输入你的需求
3. 选择或自定义表达风格
4. 等待系统处理并生成结果
5. 查看生成的 Markdown 文档

### 示例

**输入：**
```
请帮我分析最近人工智能领域的发展趋势，使用专业论文风格
```

**输出：**
- 一份包含最新AI发展趋势的专业分析报告
- 自动生成的相关图表和配图
- 结构化的 Markdown 文档

## 📁 项目结构

```
ViewForge/
├── main.py                 # 主程序入口
├── README.md               # 项目说明
├── requirements.txt        # 依赖配置
├── .env.example            # 环境变量示例
├── src/
│   ├── __init__.py
│   ├── intent_recognition/  # 意图识别模块
│   │   ├── __init__.py
│   │   ├── analyzer.py      # 意图分析器
│   │   └── style_matcher.py # 风格匹配器
│   ├── deep_search/         # 深度搜索模块
│   │   ├── __init__.py
│   │   ├── searcher.py      # 网页搜索器
│   │   └── extractor.py     # 信息提取器
│   ├── visual_enhancement/  # 视觉增强模块
│   │   ├── __init__.py
│   │   └── image_generator.py # 图片生成器
│   └── output/              # 输出处理模块
│       ├── __init__.py
│       └── markdown_generator.py # Markdown 生成器
└── tests/                   # 测试目录
    ├── __init__.py
    ├── test_intent.py
    ├── test_search.py
    ├── test_visual.py
    └── test_output.py
```

## 🔧 核心模块

### 意图识别模块
- **analyzer.py**：分析用户输入，识别核心需求
- **style_matcher.py**：匹配或推荐适合的表达风格

### 深度搜索模块
- **searcher.py**：调用搜索引擎 API 检索相关信息
- **extractor.py**：从搜索结果中提取核心事实和关键信息

### 视觉增强模块
- **image_generator.py**：根据内容生成相关配图

### 输出处理模块
- **markdown_generator.py**：将处理后的信息组织成结构化 Markdown 文档

## 🤝 贡献指南

欢迎对项目进行贡献！如果你有任何建议或改进， please:

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 联系方式

- 作者：wang ke
- 邮箱：your.email@example.com
- 项目链接：<repository-url>

---

**ViewForge** - 让信息处理更智能，让观点表达更独特！✨

核心功能：

意图识别： 分析用户输入，自动匹配或询问表达风格（如：专业论文感、小红书种草风、赛博朋克风、冷幽默风格等）。

深度搜索： 通过 API 实时检索网页，并提取核心事实。

视觉增强： 根据内容自动生成相关配图。

结构化输出： 最终产物为一份排版精美的 Markdown 文件。