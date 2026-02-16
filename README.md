# RAG Talk - Converse with History's Greatest Minds

[English](#english) | [中文](#中文)

---

<a id="english"></a>

## Overview

A full-stack RAG (Retrieval-Augmented Generation) application that lets you have real-time conversations with AI personas of historical figures. Each response is grounded in actual quotes, writings, and teachings scraped from primary sources, then retrieved via semantic search at query time.

**Live personas:** Charlie Munger, Benjamin Franklin, Marcus Aurelius, Warren Buffett, Confucius, Naval Ravikant

![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.6-orange)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)
![Tailwind](https://img.shields.io/badge/Tailwind-4-06B6D4?logo=tailwindcss)

## Architecture

```
┌─────────────┐     SSE Stream      ┌──────────────┐     Cosine Search    ┌───────────┐
│   Next.js   │ ◄──────────────────► │   FastAPI    │ ◄──────────────────► │ ChromaDB  │
│  Frontend   │     POST /api/chat   │   Backend    │     Top-K Retrieval  │  Vectors  │
└─────────────┘                      └──────┬───────┘                      └───────────┘
                                            │
                                            ▼
                                     ┌──────────────┐
                                     │  OpenRouter   │
                                     │  LLM API      │
                                     └──────────────┘
```

**How RAG works in this app:**
1. User sends a message to a persona
2. The message is embedded and searched against that persona's ChromaDB collection
3. Top-K most relevant quotes/writings are retrieved (cosine similarity)
4. Retrieved context is injected into the system prompt as "Reference Materials"
5. The LLM generates a response grounded in real source material
6. Response streams token-by-token via Server-Sent Events

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 16, React 19, TypeScript 5 | UI with real-time SSE streaming |
| Styling | Tailwind CSS 4 | Dark theme, glass morphism, per-persona theming |
| Backend | FastAPI, Uvicorn | Async API with SSE streaming |
| Vector DB | ChromaDB | Persistent semantic search with cosine similarity |
| LLM | OpenRouter API (Llama 3.1 8B default) | Response generation |
| Scraping | BeautifulSoup4, PyPDF, httpx | Data collection from primary sources |

## Features

- **6 unique AI personas** with distinct personalities, system prompts, and visual themes
- **RAG-grounded responses** - every answer backed by real quotes and writings
- **Real-time streaming** - token-by-token SSE for responsive conversation
- **Per-persona chat backgrounds** - unique high-tech animated backgrounds (circuit boards, constellations, network meshes, stock charts, etc.)
- **CSS art avatars** - SVG icon avatars with persona-colored gradients (no external images)
- **Dark mode UI** - Silicon Valley aesthetic with glass morphism and animated gradients
- **Full conversation memory** - history passed to maintain multi-turn context
- **Data pipeline** - automated scraping, cleaning, chunking, and vector ingestion

## Data Sources

| Persona | Sources | Content |
|---------|---------|---------|
| Charlie Munger | FS Blog, 25iq.com | Speeches, mental models, quotes |
| Benjamin Franklin | Project Gutenberg | Autobiography, Poor Richard's Almanack |
| Marcus Aurelius | Project Gutenberg | Meditations |
| Warren Buffett | Multiple financial blogs | Shareholder letters, interviews, quotes |
| Confucius | Project Gutenberg | Analerta, teachings |
| Naval Ravikant | Navalmanack | Wealth & happiness principles |

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- An [OpenRouter](https://openrouter.ai/) API key

### 1. Install dependencies
```bash
make setup
```

### 2. Configure environment
```bash
cp .env.example backend/.env
```

Edit `backend/.env`:
```
OPENROUTER_API_KEY=your-key-here
LLM_MODEL=meta-llama/llama-3.1-8b-instruct
CHROMA_DB_PATH=./chroma_db
```

### 3. Build the knowledge base
```bash
make data    # scrape sources + ingest into ChromaDB
```

### 4. Run development servers

Terminal 1:
```bash
make backend    # FastAPI on http://localhost:8000
```

Terminal 2:
```bash
make frontend   # Next.js on http://localhost:3000
```

### 5. Open the app
- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/personas` | List all available personas |
| `POST` | `/api/chat` | Send message, receive SSE stream |

**Chat request body:**
```json
{
  "persona_id": "charlie-munger",
  "message": "What are mental models?",
  "conversation_history": []
}
```

**SSE response format:**
```
data: {"token": "Mental"}
data: {"token": " models"}
data: {"token": " are"}
...
data: [DONE]
```

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI app, CORS, routes
│   │   ├── config.py              # Pydantic settings
│   │   ├── models/schemas.py      # Request/response models
│   │   ├── routers/
│   │   │   ├── chat.py            # POST /api/chat (SSE)
│   │   │   └── personas.py        # GET /api/personas
│   │   ├── services/
│   │   │   ├── rag.py             # RAG pipeline & context building
│   │   │   ├── llm.py             # OpenRouter streaming client
│   │   │   └── vectorstore.py     # ChromaDB wrapper
│   │   └── personas/*.json        # Persona definitions
│   ├── scrapers/                  # Web scrapers per source
│   ├── ingestion/                 # Clean, chunk, vectorize pipeline
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                   # Next.js pages & layout
│   │   ├── components/            # React components
│   │   │   ├── ChatInterface.tsx   # Main chat view
│   │   │   ├── ChatBackground.tsx  # Per-persona animated backgrounds
│   │   │   ├── PersonaAvatar.tsx   # CSS art SVG avatars
│   │   │   ├── PersonaCard.tsx     # Homepage persona cards
│   │   │   ├── MessageBubble.tsx   # Chat message bubbles
│   │   │   └── ChatInput.tsx       # Message input bar
│   │   ├── lib/
│   │   │   ├── api.ts             # API client & SSE handler
│   │   │   └── personas.ts        # Theme config & SVG paths
│   │   └── hooks/useChat.ts       # Chat state management
│   └── package.json
├── Makefile                       # Build & run commands
└── .env.example
```

## Make Commands

| Command | Description |
|---------|-------------|
| `make setup` | Install Python + Node dependencies |
| `make scrape` | Scrape all data sources |
| `make ingest` | Ingest scraped data into ChromaDB |
| `make data` | Scrape + ingest (full pipeline) |
| `make backend` | Start FastAPI dev server |
| `make frontend` | Start Next.js dev server |

---

<a id="中文"></a>

## 概述

一个全栈 RAG（检索增强生成）应用，让你与历史伟人的 AI 人格进行实时对话。每个回复都基于从原始资料中抓取的真实引言、著作和教导，通过语义搜索在查询时检索相关内容。

**内置人物：** 查理·芒格、本杰明·富兰克林、马可·奥勒留、沃伦·巴菲特、孔子、纳瓦尔·拉维坎特

## 架构

```
┌─────────────┐     SSE 流式传输     ┌──────────────┐     余弦相似度搜索    ┌───────────┐
│   Next.js   │ ◄──────────────────► │   FastAPI    │ ◄──────────────────► │ ChromaDB  │
│    前端      │   POST /api/chat    │    后端       │     Top-K 检索      │  向量数据库 │
└─────────────┘                      └──────┬───────┘                      └───────────┘
                                            │
                                            ▼
                                     ┌──────────────┐
                                     │  OpenRouter   │
                                     │  大语言模型    │
                                     └──────────────┘
```

**RAG 工作流程：**
1. 用户向某个人物发送消息
2. 消息被向量化并在该人物的 ChromaDB 集合中进行语义搜索
3. 检索出最相关的 Top-K 条引言/著作（余弦相似度）
4. 检索到的上下文作为"参考资料"注入系统提示词
5. 大语言模型基于真实原始资料生成回复
6. 回复通过 Server-Sent Events 逐 token 流式传输

## 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| 前端 | Next.js 16、React 19、TypeScript 5 | 界面与实时 SSE 流式传输 |
| 样式 | Tailwind CSS 4 | 暗色主题、毛玻璃效果、人物主题定制 |
| 后端 | FastAPI、Uvicorn | 异步 API 与 SSE 流式传输 |
| 向量库 | ChromaDB | 持久化语义搜索（余弦相似度） |
| 大模型 | OpenRouter API（默认 Llama 3.1 8B） | 回复生成 |
| 数据采集 | BeautifulSoup4、PyPDF、httpx | 从原始来源采集数据 |

## 功能特性

- **6 个独特 AI 人物** — 各有独立性格、系统提示词和视觉主题
- **RAG 增强回复** — 每个回答都有真实引言和著作支撑
- **实时流式传输** — 逐 token SSE 推送，对话响应即时
- **人物专属聊天背景** — 独特的高科技动画背景（电路板、星座、网络拓扑、股票图表等）
- **CSS 艺术头像** — SVG 图标头像配合人物专属渐变色（无外部图片）
- **暗色模式 UI** — 硅谷风格美学，毛玻璃效果与动画渐变
- **完整对话记忆** — 传递历史记录以维持多轮对话上下文
- **数据管线** — 自动化抓取、清洗、分块与向量化入库

## 数据来源

| 人物 | 来源 | 内容 |
|------|------|------|
| 查理·芒格 | FS Blog、25iq.com | 演讲、思维模型、语录 |
| 本杰明·富兰克林 | Project Gutenberg | 自传、穷理查年鉴 |
| 马可·奥勒留 | Project Gutenberg | 沉思录 |
| 沃伦·巴菲特 | 多个金融博客 | 致股东信、访谈、语录 |
| 孔子 | Project Gutenberg | 论语、学说 |
| 纳瓦尔·拉维坎特 | Navalmanack | 财富与幸福原则 |

## 快速开始

### 前置要求
- Python 3.10+
- Node.js 18+
- [OpenRouter](https://openrouter.ai/) API 密钥

### 1. 安装依赖
```bash
make setup
```

### 2. 配置环境变量
```bash
cp .env.example backend/.env
```

编辑 `backend/.env`：
```
OPENROUTER_API_KEY=你的密钥
LLM_MODEL=meta-llama/llama-3.1-8b-instruct
CHROMA_DB_PATH=./chroma_db
```

### 3. 构建知识库
```bash
make data    # 抓取数据源 + 入库 ChromaDB
```

### 4. 启动开发服务器

终端 1：
```bash
make backend    # FastAPI 运行在 http://localhost:8000
```

终端 2：
```bash
make frontend   # Next.js 运行在 http://localhost:3000
```

### 5. 打开应用
- 前端：http://localhost:3000
- API 文档：http://localhost:8000/docs

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/api/health` | 健康检查 |
| `GET` | `/api/personas` | 获取所有可用人物 |
| `POST` | `/api/chat` | 发送消息，接收 SSE 流 |

## Make 命令

| 命令 | 说明 |
|------|------|
| `make setup` | 安装 Python + Node 依赖 |
| `make scrape` | 抓取所有数据源 |
| `make ingest` | 将抓取数据导入 ChromaDB |
| `make data` | 抓取 + 导入（完整管线） |
| `make backend` | 启动 FastAPI 开发服务器 |
| `make frontend` | 启动 Next.js 开发服务器 |
