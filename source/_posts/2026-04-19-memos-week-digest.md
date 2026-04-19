---
title: 周记 · Memos 摘录（2026-04-13 ~ 2026-04-19）
date: 2026-04-19 20:00:00
updated: 2026-04-19 20:00:00
tags:
  - 周记
  - Memos
categories:
  - 周记
excerpt: 汇总本周 Memos 中按主题整理的技术笔记、阅读摘录与随笔，便于检索与复盘。
---

> 本文由 [Memos](https://usememos.com/) 中 **2026-04-13 ~ 2026-04-19**（北京时间）发布的笔记自动汇总生成，按主题归类；每条保留原文要点，并附回链。

## 项目 · NoteSeed

### NoteSeed 项目特色与亮点解析

- **时间**：2026-04-19T01:49:35Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/UjVQRXdWfqumXromkqKyXg)

# NoteSeed 项目特色与亮点解析

## 一句话定位

**"浏览即学习"** — 把网页碎片阅读转化为结构化知识卡片的 Chrome 扩展 + 后端系统。

## 1. 核心亮点：5 阶段 AI Skills 管线

这是整个项目最有设计感的部分。不是简单地"把网页丢给 LLM 总结"，而是拆成了精心设计的 5 步管线：

PageSense → Contextualizer → Distiller → Tagger → Cardwright

| 阶段 | 作用 | 亮点 |
|------|------|------|
| PageSense | 分类（8种页面类型） | 用 fast model，决定后续 prompt 策略 |
| Contextualizer | 补全元数据 | 自动推断作者、日期、阅读时间 |
| Distiller | 内容蒸馏 | 按页面类型用不同 prompt，支持自定义 prompt |
| Tagger | 标签生成 | 参考用户历史标签，保持一致性 |
| Cardwright | 模板渲染 | 6 种模板，纯字符串拼接无 LLM 调用 |

**每一步都有优雅的降级路径** — LLM 挂了不会整条链路崩溃。PageSense 失败就默认 resource 类型，Distiller 失败就截取前 200 字，Tagger 失败就空标签，Cardwright 失败就拼个最简 markdown。这种渐进式降级设计比 all or nothing 健壮得多。

## 2. 架构亮点：pnpm Monorepo + 关注点分离

- apps/extension → Chrome MV3 扩展（React + Zustand + Dexie）
- apps/backend → Fastify API（Prisma + Postgres）
- packages/skills → AI 管线引擎（纯逻辑，不依赖框架）
- packages/adapters → 第三方平台适配器
- packages/shared-types → Zod schema + TS 类型

skills 包是纯业务逻辑，不依赖 Fastify 也不依赖 Chrome API，可以独立测试和复用。这是很好的依赖反转实践。

## 3. LLM 多厂商抽象

- 统一的 LLMProvider 抽象层，Anthropic 走 tool_use，OpenAI 走 function calling
- 请求级 provider 覆盖：每次调用可以用不同模型，用 try/finally 保证清理
- 兼容 DeepSeek / Moonshot / GLM / Ollama 等 OpenAI 协议兼容的模型

## 4. 适配器 + 分发器模式

- 注册表模式：registry 映射目标名到适配器实例，新增平台只需加一个 adapter
- 并行分发：Promise.all 同时保存到多个目标
- 凭证解耦：credentialResolver 回调注入，适配器本身不知道凭证怎么存

## 5. 安全设计

- AES-256-GCM 凭证加密：API Key 和第三方 Token 在 Postgres 中加密存储
- Zod 边界校验：HTTP body、环境变量、共享类型全部用 Zod schema 做运行时验证
- 环境变量里的 CREDENTIAL_ENCRYPTION_KEY 要求 ≥32 字节

## 6. 扩展端工程亮点

- MV3 Service Worker 消息路由：content script / side panel / service worker 三角通信，AbortController 支持取消进行中的请求
- Dexie 离线暂存：IndexedDB 本地缓存 + LRU 策略，网络挂了卡片不丢
- Readability + DOMPurify + Turndown 三件套：页面抓取 → 净化 → HTML 转 Markdown

## 7. 运维友好

- Docker Compose 一键起 Postgres + Backend
- 提供 docker-compose.prod.yml 和 1Panel 部署教程
- GitHub Actions CI：lint → build → test
- 78+ 单元/集成测试覆盖

## 值得注意的技术债

1. auth/login.ts 已写但未注册到路由 — JWT magic link 登录是预留的，当前是固定单用户模式
2. configFromEnv() 在 skills 包里有但路由没调用 — 环境变量级 AI 配置实际未生效
3. 飞书适配器已注册但还在开发中

## 总结

NoteSeed 的核心竞争力：
1. 管线式架构 — 每步可独立调优、降级、替换
2. 模板多样性 — 6 种卡片模板 + 自定义 prompt
3. 工程质量 — Monorepo 分层清晰、Zod 全链路校验、优雅降级、测试覆盖
4. 开放性 — 多 LLM 厂商、多保存目标、自定义提示词

整体来看这是一个设计过度（褒义）的 side project — 架构和工程化做得比功能体量所需的更完善，留足了扩展空间。

#AI-Agent

---

### NoteSeed 🌱

- **时间**：2026-04-19T01:54:42Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/T9gNjgpJk6MBYxNUe4QN73)

# NoteSeed 🌱

**Seed the web into your second brain.**

NoteSeed 是一款 Chrome 浏览器扩展（MV3），通过 5 阶段 AI Skills 管线将网页内容转化为结构化知识卡片，一键保存到 [Memos](https://usememos.com/) 等知识系统。

> 🧠 核心理念：浏览即学习 — 把碎片化阅读转化为可检索、可复用的知识资产。

---

## ✨ 功能亮点

| 功能 | 描述 |
|------|------|
| **智能分类** | 自动识别 8 种页面类型（教程 / 观点 / 新闻 / 文档 / 工具 / 资源 / 长文 / 讨论） |
| **AI 管线提取** | 5 阶段管线：分类 → 元数据补全 → 内容蒸馏 → 标签生成 → 卡片渲染 |
| **6 种卡片模板** | 平衡 / 精简 / 详细 / 教程提炼 / 观点摘要 / 自定义提示词 |
| **自定义 AI** | 支持 Anthropic 和 OpenAI 协议兼容的任意大模型（Claude / GPT / DeepSeek / Moonshot / GLM / Ollama 等） |
| **自定义提示词** | 输入任意提示词即可按你的方式制卡 |
| **一键制卡** | 从任意网页生成结构化 Markdown 知识卡片，支持编辑后保存 |
| **多目标分发** | 保存到 Memos（更多平台开发中） |
| **离线暂存** | Dexie (IndexedDB) 离线缓存 + LRU 清理，网络故障不丢数据 |
| **凭证加密** | AES-256-GCM 后端加密存储，前端不存明文 |
| **云部署** | 支持 Docker Compose 一键部署到云服务器 |

---

## 🏗️ 架构概览

```
┌────────────────────────────┐
│   Chrome Extension (MV3)   │
│ ┌────────┐ ┌────────────┐  │
│ │Content │ │ Side Panel  │  │
│ │ Script │ │  (React)    │  │
│ └───┬────┘ └──────┬─────┘  │
│     │  messages    │        │
│  ┌──▼─────────────▼──┐     │
│  │  Service Worker    │     │
│  └────────┬───────────┘     │
└───────────┼─────────────────┘
            │ HTTPS
┌───────────▼─────────────────┐
│   Backend (Fastify)          │
│ ┌─────────┐ ┌─────────────┐ │
│ │  Skills  │ │  Adapters   │ │
│ │ Pipeline │ │  (Memos)    │ │
│ └─────────┘ └─────────────┘ │
│ ┌──────────┐                │
│ │ Prisma   │                │
│ │ (PG 16)  │                │
│ └──────────┘                │
└──────────────────────────────┘
```

**数据流:** Content Script 抓取 → Readability 清洗 → Skills Pipeline 生成 KnowledgeCard → react-markdown 预览 → Adapter Dispatcher 分发保存

### AI Skills 管线

| 阶段 | Skill | 模型角色 | 职责 |
|------|-------|---------|------|
| 1 | **PageSense** | fast | 页面类型分类（8 种类型） |
| 2 | **Contextualizer** | fast | 元数据补全（作者 / 日期 / 语言 / 阅读时间） |
| 3 | **Distiller** | powerful | 内容结构化提取（按类型定制 prompt） |
| 4 | **Tagger** | fast | 标签 / 分类 / 主题生成 |
| 5 | **Cardwright** | 无 LLM | Markdown 模板渲染（6 种模板） |

每步都有降级路径：LLM 失败时回退到启发式规则或默认值。

### 卡片模板

| 模板 | 说明 |
|------|------|
| **平衡** (balanced) | 默认模板，摘要 + 要点 + 引述，适合大多数网页 |
| **精简** (concise) | 极简输出，一句话摘要 + 3 个核心要点 |
| **详细** (detailed) | 完整卡片，含引述、不同意见与反论点 |
| **教程提炼** (tutorial) | 提取步骤、前置条件、代码片段 |
| **观点摘要** (opinion) | 聚焦论点、论据、立场分析 |
| **自定义提示词** (custom) | 输入任意提示词，AI 按你的要求生成内容 |

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 扩展 | React 18, TypeScript 5, Vite 5, CRXJS (beta), Tailwind CSS 3, Zustand 5, Dexie 4 |
| 后端 | Node.js 20, Fastify 5, Prisma 5, PostgreSQL 16 |
| AI | 多提供者支持：Anthropic (tool_use) + OpenAI 兼容 (function calling)，用户可自定义 |
| 内容处理 | Readability, DOMPurify, Turndown (HTML→Markdown), react-markdown |
| 测试 | Vitest, 78+ 单元 / 集成测试（覆盖 skills / adapters / schemas / backend） |
| 工程化 | pnpm workspace monorepo, ESLint, Prettier, Docker |

---

## 🚀 快速开始

### 前置要求

- **Node.js** 20+
- **pnpm** 9+
- **Docker** & Docker Compose（用于 PostgreSQL + 后端）
- **AI API Key**（[Anthropic](https://console.anthropic.com/) 或 [OpenAI](https://platform.openai.com/) 或其他兼容服务）

### 1. 克隆 & 安装依赖

```bash
git clone https://github.com/jxzzlfh/NoteSeed.git noteseed
cd noteseed
pnpm install
```

### 2. 启动服务

```bash
docker compose up -d    # PostgreSQL 16 + Backend
```

### 3. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 填入必要值：

| 变量 | 必填 | 说明 |
|------|:----:|------|
| `DATABASE_URL` | ✅ | PostgreSQL 连接串（默认值可直接用） |
| `CREDENTIAL_ENCRYPTION_KEY` | ✅ | AES-256 加密密钥（32 字节 base64） |
| `NODE_ENV` | | `development` / `production`（默认 `development`） |
| `PORT` | | 服务端口（默认 `3000`） |
| `LOG_LEVEL` | | 日志级别（默认 `info`） |

> 💡 **快速生成密钥:** `node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"`
>
> AI API Key 不在 `.env` 中配置 — 用户在扩展设置页的「AI 模型」Tab 中填写，每次请求随报文传入后端。

### 4. 初始化数据库

```bash
pnpm --filter @noteseed/backend exec prisma migrate dev
```

### 5. 启动开发服务

```bash
# 扩展热重载
pnpm --filter @noteseed/extension dev
```

> 后端已通过 `docker compose up -d` 随容器启动（端口 3000）。如需本地源码调试后端，可单独 `pnpm --filter @noteseed/backend dev`。

### 6. 加载扩展

1. 打开 Chrome，访问 `chrome://extensions`
2. 开启右上角「开发者模式」
3. 点击「加载已解压的扩展程序」→ 选择 `apps/extension/dist` 目录
4. 点击浏览器工具栏的 NoteSeed 图标，打开侧边栏

### 7. 初始配置

打开扩展设置页（侧边栏右上角 ⚙ 图标）：

1. **通用** Tab → 确认后端地址为 `http://localhost:3000`
2. **AI 模型** Tab → 选择 AI 提供者，填入 API Key 和模型名
3. **凭证** Tab → 填写 Memos Base URL 和 Token → 测试连接 → 保存

完成后即可在任意网页点击侧边栏一键制卡。

---

## 📦 构建 & 测试

```bash
# 构建所有包
pnpm build

# 仅构建扩展 zip（用于发布）
pnpm --filter @noteseed/extension build:zip

# 运行全部测试
pnpm test

# 代码检查 & 格式化
pn

…

（篇幅过长，完整正文请在上方 Memos 原文链接中查看。）

---

## AI 与工程实践

### Hermes 常用 CLI 命令

- **时间**：2026-04-15T06:40:44Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/khmDZRQkYpZnXiubR4Fq9M)

## Hermes 常用 CLI 命令

### 核心命令
- hermes chat - 交互式或一次性聊天
- hermes model - 选择默认的模型提供商
- hermes setup - 交互式设置向导
- hermes status - 显示代理、认证和平台状态

### 配置管理
- hermes config - 查看和编辑配置文件
- hermes tools - 配置启用的工具
- hermes skills - 浏览、安装和管理技能
- hermes profile - 管理多个配置文件

### 会话管理
- hermes sessions - 列出最近会话
- hermes backup - 备份 Hermes 目录
- hermes logs - 查看日志文件
- hermes doctor - 诊断配置和依赖问题

### 实用工具
- hermes version - 显示版本信息
- hermes update - 更新到最新版本
- hermes uninstall - 卸载 Hermes
- hermes cron - 管理定时任务

## Hermes 常用斜杠命令（聊天中）

### 会话控制
- /new 或 /reset - 开始新会话
- /clear - 清屏并开始新会话
- /history - 显示对话历史
- /title [名称] - 设置会话标题
- /save - 保存当前对话

### 模型控制
- /model [模型名] - 切换模型
- /provider - 查看可用提供商
- /fast [normal|fast|status] - 切换快速模式
- /reasoning [level|show|hide] - 管理推理努力

### 工具管理
- /tools [list|disable|enable] - 管理工具
- /skills - 搜索和管理技能
- /browser [connect|disconnect|status] - 管理浏览器连接
- /cron - 管理定时任务

### 调试和帮助
- /help - 显示帮助信息
- /usage - 显示令牌使用情况和成本分析
- /debug - 上传调试报告
- /config - 显示当前配置

### 高级功能
- /background <提示> - 在后台运行任务
- /plan [请求] - 加载计划技能编写计划
- /snapshot [create|restore|prune] - 创建或恢复快照
- /yolo - 切换 YOLO 模式（跳过危险命令确认）

#AI-Agent

---

### Claude Code Routines 功能亮点

- **时间**：2026-04-16T00:44:30Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/LMoReZGEZ2JVDMopL9PdyX)

## Claude Code Routines 功能亮点
**Claude Code 全新推出的 routines 功能**，实现了**云端与本地环境打通**，可在无需开机的状态下运行云端定时任务，任务执行完成后还能衔接本地环境，待工作时继续处理。

- 支持将**提示词、仓库、环境、连接器**打包为云端自动任务，电脑关机时 Claude 仍可按计划或事件自动执行
- 触发方式多样：按小时/每日定时、HTTP API 调用、响应 GitHub 的 PR/push/issue/workflow 事件
- 适用于**无人值守、可重复、目标明确**的自动化工作流
- 每次触发会开启完整的云端 Claude Code 会话，可运行 shell、调用仓库内技能、访问外部服务

该功能体现了 Agent 产品的构建思路：以**本地优先**为基础，通过云端自动化承接基础重复性任务，且随着模型能力提升，可覆盖的任务范围将持续扩大。

详情：https://code.claude.com/docs/en/routines

---

### 人格化专属Agent：AI行业的终极破局方向

- **时间**：2026-04-16T01:03:47Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/i92QfXRGXzXZ8YvpVo4Xqa)

## 人格化专属Agent：AI行业的终极破局方向

### 一、通用大模型的核心局限
- 算法可**拟合知识、复刻逻辑**，但无法触及人性核心
- 关键短板：缺乏独属于人的经历、思维内核、价值判断与深层共情，这是通用AI难以突破的边界

### 二、AI的终极形态定义
- 核心方向：并非打造全能通用机器，而是**封装个人专属特质**，锻造人格化Agent
- 封装核心要素：人生阅历、底层思维、专属方法论、核心价值观

### 三、人格化专属Agent的核心价值
1. 精准解决问题：如同“数字药方”或资深医者的独家诊疗方案，直击痛点、落地性强
2. 不可复制性：作为个人独一无二的数字投影，具备专属人格底色与思考逻辑
3. 核心竞争力：拥有无法抄袭、不可替代的价值，无限逼近真人存在形态

---

### 知识管理无效的根源在于生产方式

- **时间**：2026-04-16T01:05:07Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/XpyRkNwMjmQsE4zvuGw4rk)

## 知识管理无效的根源在于生产方式
很多人都会陷入这样的误区：
- 知乎App里收藏大量内容，却从不翻看
- 云笔记中收集各类复杂模板，却从不使用
- AI时代让大模型生成卡片笔记，依旧束之高阁

这一现象的核心问题，**并非知识管理工具不行**，**也不是个人缺乏思考与内化能力**，更无关所谓注意力、灵魂内化等抽象概念。

根本原因在于：**你不靠文字内容谋生**，问题本质出在**生产方式**上。

当**内容并非你的核心生产要素**时，所做的一切知识管理行为，都只是形式上的积累，没有实际产出需求驱动。这样的知识管理，不过是个无用的**玩具**，完全没有必要去做。

---

### AI技术快速迭代，人机交互迈向全新范式

- **时间**：2026-04-16T01:16:01Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/bg7hgegtkaQH8sSCvS6ead)

## AI技术快速迭代，人机交互迈向全新范式
不到半年，行业从**Chat first**转向**Code first**，人们的工作界面、习惯与模式彻底改变；**AI Agents**推动世界进入**通用智能时代**，逐步接管计算机与互联网。

- Skill Graph、Harness as product等**AI原生团队**专属概念，大众仍感陌生，但数代人才能完成的技术范式转变，如今数月内便已发生。
- PC时代人类需适应机器界面，当下**大语言模型（LLMs）**主动学习人类语言，如同智能伙伴与人协作，技术进化核心是**机器趋人化**，而非人趋机器化。

人类凭借**强大的适应性**不会被技术淘汰。技术越发展，越贴近生命本真，现有软件在不久后便会显得陈旧过时。

计算正成为普惠魔法，只需指令即可实现创造；其核心价值在于**民主化**，艺术、软件与科学创造不再专属少数人，而是向每一位勇于探索者开放。

---

### 发现一个有意思的AI技能平台——虾评Skill

- **时间**：2026-04-16T01:37:21Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/UQZ3j8YhrioMnxLqhog5MB)

## 发现一个有意思的AI技能平台——虾评Skill
作为**技术小白**，想借助AI开展副业，经朋友推荐了解到**虾评Skill**，平台汇聚各类AI技能，还可赚取**虾米**。

经过两天体验，该平台十分适合普通人入门，优势如下：
- 每日打卡即可赚取虾米
- 部分技能支持免费试用
- 社区内有其他Agent分享实操经验

https://xiaping.coze.site

---

### AI引发的失业潮与行业反噬困境

- **时间**：2026-04-16T01:48:25Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/VGnC6JT4y6CCgWQ4MzuPmK)

## AI引发的失业潮与行业反噬困境
AI普及将造成**大规模失业**，失业导致居民收入下降、消费缩减，进而让企业产品滞销、营收利润下滑并削减预算。

- 企业经营困难甚至倒闭，将停止采购AI服务，直接冲击**大模型公司收入**，使其无力投入数据中心建设、算力采购，也难以支撑高估值。
- 企业营销投放减少，自媒体失去商单收入，即便AI能高效生产内容也无盈利意义，相关内容模型研发动力消失。
- 财富向头部科技企业与顶尖人才集中，货币无法向下流动，底层群体受冲击后会反向影响上层经济生态。

破解路径仅有两条：
1. 国家为受冲击群体发放**基本收入保障**
2. 创造大量新就业岗位

但新行业岗位门槛高、吸纳就业能力远不及餐饮、房产等传统行业，还会进一步替代人力，同时拖累传统行业发展。

发放保障资金需依靠税收，而个税与普通企业税均不可行，最可行方式是向**Token生产与使用企业征税**。可若仅我国征税、美国不征税，会导致AI企业与资本外流，削弱我国AI竞争力，因此反而需减税补贴。

整体而言，该问题**解决难度极大**，十分考验未来治理能力。

---

### 7 个真正能变现的 Claude Skill 方向

- **时间**：2026-04-16T01:49:48Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/57yu73VRbpcCUKGZWgBaSK)

## 7 个真正能变现的 Claude Skill 方向
1. **克隆客户文风**：生成内容贴近真人表达，无明显AI痕迹
2. **自动生成周报**：自动整理数据产出周报，每周节省2小时，提升工作效率
3. **长内容拆分短切片**：将长内容拆解为15个短内容，实现一稿多发，解决分发难题
4. **自动生成商业提案+报价**：填写表单即可快速生成，提升成单效率
5. **CRM数据智能分析**：筛查续约机会与流失风险，挖掘潜在收益
6. **知识库驱动客服回复**：依托知识库自动起草回复，减少人力投入
7. **定制化开发信撰写**：抓取目标公司数据生成专属开发信，提高转化效果

---

### Claude Code品牌视觉一致性技能Hue

- **时间**：2026-04-16T04:36:11Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/NBxzbv2eyJTkNU6mNEVgZJ)

## Claude Code品牌视觉一致性技能Hue
**Hue**是Claude Code的一项实用技能，只需向其提供**URL或截图**，即可实现品牌视觉一致性输出。

- 可自动提取URL或截图内的**品牌风格**，涵盖颜色、字体、阴影等元素，生成完整**设计系统**
- Claude后续生成的所有UI内容，会自动引用该设计系统，确保品牌视觉统一
- 设计系统包含：颜色、字体、圆角、阴影等基础规范
- 内置**30+常用UI组件**，如按钮、输入框、卡片等
- 支持**深浅双模式**适配
- 最终生成**8个文件**，其中包含可直接浏览的完整组件库HTML文件

https://github.com/dominikmartn/hue

---

### newtype-os - AI Agent 内容创作协作系统

- **时间**：2026-04-16T12:41:30Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/mcGKAbXAivWqW7C329JVSV)

## newtype-os - AI Agent 内容创作协作系统

**简介**：8人代理分层编排系统，模仿真实内容生产团队
- Chief（主编）：用户唯一交互入口
- Deputy（副主编）：调度协调  
- 6位专家：Researcher（研究）、Fact-Checker（事实核查）、Archivist（知识库）、Extractor（提取）、Writer（写作）、Editor（编辑）

**核心功能**：
- 专业技能框架：/super-workflow、/super-analyst 等
- MCP 工具：Exa、Tavily、Firecrawl 搜索
- 记忆系统：每日摘要、7天归档
- 知识库：AGENTS.md、KNOWLEDGE.md
- 微信集成：WeClaw

**用法**：
1. CLI: npm install -g @newtype-os/cli && nt
2. OpenCode插件: bun add @newtype-os/plugin
3. nt init 初始化配置
4. 命令：nt research、nt write、nt pipeline

#AI-Agent

---

### Lime：本地优先的 AI Agent 创作工作台

- **时间**：2026-04-17T01:01:12Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/inSVJgTUqGU8QEbkEcUCec)

## Lime：本地优先的 AI Agent 创作工作台

1. Lime 是一个基于 Tauri 的本地优先桌面应用，为创作者、内容团队与知识工作者提供全流程创作支持，从想法生成到交付结果。
2. 主要功能包括 Workspace（汇总项目文件和任务会话）、Skills（流程和经验复用工具）、MCP（标准能力扩展）、Claw 渠道（异步协作接口）以及 Artifact（成果交付和沉淀）。
3. 用户可以通过 Lime 实现内容创作闭环、信息收集与整理、跨平台交互、标准能力工具调用，以及批量或长期任务的自动化执行。
4. 适合需要高效创作、数据沉淀和结果可追溯的小团队和专业创作者。
5. 提供跨平台支持（macOS 和 Windows），Linux 的开发暂时停止。支持开发者通过文档和命令自主定制。

https://github.com/limecloud/lime

---

### Claude-Cowork 桌面AI助手

- **时间**：2026-04-17T01:05:52Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/gTMqLfRzbzWM2Fka7ribGC)

## Claude-Cowork 桌面AI助手
**项目地址**：https://github.com/DevAgentForge/Claude-Cowork/blob/main/README_ZH.md

**项目简介**：
开源版 Claude CoWork，一款**桌面 AI 助手**，可高效辅助完成各类任务。

- 支持**编程辅助**、**文件管理**及自定义描述类任务处理
- 无需 Claude 订阅即可使用
- 兼容多款**国产大模型**：智谱 GLM、MiniMax、Kimi、DeepSeek 等

---

### HAPI：本地运行AI编程会话并支持远程控制

- **时间**：2026-04-17T01:21:51Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/C6NWCRFAmDPSnw9awKBKw8)

## HAPI：本地运行AI编程会话并支持远程控制
**项目地址**：https://github.com/tiann/hapi

**项目简介**：
一款**开源的AI编程Agent客户端**，核心功能如下：
- 支持在**本地运行**官方 Claude Code、Codex、Gemini、OpenCode 会话
- 可通过**网页、PWA、Telegram迷你应用**实现远程控制
- 支持远程**监控与审批工具权限**，保障使用安全

---

### AgentVerse多AI智能体协作开源平台

- **时间**：2026-04-17T01:25:19Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/PbzLUK8bcLFmqTqjyXXFeZ)

## AgentVerse多AI智能体协作开源平台
- **项目地址**：https://github.com/Peiiii/AgentVerse
- **项目定位**：**开源平台**，支持**多AI智能体协作对话**
- **核心能力**
  1. 汇聚**不同专业领域、不同个性**的AI专家
  2. AI专家可实现**自主交流、协作讨论**
  3. 为用户提供**多角度专业见解**与**解决方案**

---

### lovcode人工智能编码工具桌面配套应用

- **时间**：2026-04-17T01:30:29Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/e4nuJdvS3jex83JnwP8Bpr)

## lovcode人工智能编码工具桌面配套应用
- **项目地址**：https://github.com/lovstudio/lovcode
- **项目定位**：面向人工智能编码工具的**桌面配套应用**
- **核心功能**：
  1. 浏览 Claude Code 聊天记录
  2. 管理相关配置信息
  3. 管理使用命令
  4. 管理各类技能

---

### LobsterAI全场景个人助理Agent

- **时间**：2026-04-17T01:40:03Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/hwD7PoGvKg8Jx6QT5mMfTd)

## LobsterAI全场景个人助理Agent
**项目地址**：https://github.com/netease-youdao/LobsterAI/blob/main/README_zh.md
**开发主体**：**网易有道**(opens new window)

**核心功能**：
- 提供**7×24小时**全天候服务
- 支持**数据分析**
- 支持**制作PPT**
- 支持**生成视频**
- 支持**撰写文档**
- 支持**信息搜索**
- 支持**收发邮件**
- 支持**定时任务**
- 可满足更多日常办公场景需求

---

### lumma AI原生开源日记应用

- **时间**：2026-04-17T01:48:35Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/TeQU9pfi83g4csqXMNpKDC)

## lumma AI原生开源日记应用
- **项目地址**：https://github.com/geosmart/lumma
- **技术基础**：基于**Flutter**开发的开源AI日记应用
- **核心功能**
  1. 提供**Q&A引导式记录**与**AI聊天**两种记录模式
  2. 支持接入**多种大模型**，实现内容自动摘要与分类
- **数据存储**：可通过**WebDAV**或**Obsidian插件**，完成数据本地化持久存储与多端同步

---

## 产品与商业思考

### 木桶效应在 AI 时代被放大。 设计，产品，研发，测试，营销，任何一个环节还在用人类速度运行，都会拖垮整个团队的 AI

- **时间**：2026-04-16T00:42:57Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/eAJMissvnS5Z2eCY5h6TzL)

木桶效应在 AI 时代被放大。

设计，产品，研发，测试，营销，任何一个环节还在用人类速度运行，都会拖垮整个团队的 AI 速度。

---

### 表演赚钱与真实做生意的区别

- **时间**：2026-04-16T01:24:05Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/7MXCpvoGvPoLBX5vUxxcL3)

## 表演赚钱与真实做生意的区别
- 表演赚钱阶段：可以且需要展示给**观众**，对应**Build in Public**模式。因自身尚未确定能否盈利，通过公开造势、积累关注度是合理的。
- 真正盈利阶段：不再需要观众，**观众不提供收益，只有顾客才会付费**。
- 本质差异：前者是试探性造势，后者才是务实的商业逻辑，**真正的生意只聚焦顾客，而非观众**。

---

### MrRSS 开源RSS阅读器

- **时间**：2026-04-17T01:52:34Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/46tevtPzn3LNUNPq8UtRyP)

## MrRSS 开源RSS阅读器
- **项目地址**：https://github.com/WCY-dt/MrRSS/blob/main/README_zh.md
- **技术基础**：基于**Wails v3**构建
- **核心定位**：现代化**开源RSS阅读器**
- **核心功能**
  1. 支持**AI自动摘要**
  2. 具备**全文抓取**能力
  3. 集成**多引擎翻译**
- **支持平台**：Windows、macOS、Linux
- **产品目标**：提供**私密、高效、智能**的本地RSS阅读体验

---

### KnowNote AI工作空间

- **时间**：2026-04-17T02:16:32Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/4MARGSnvTkPzwWneJE4YNp)

## KnowNote AI工作空间
- **项目地址**：https://github.com/MrSibe/KnowNote
- **项目定位**：一款对标Notebook LM，以**用户自有知识**为核心的AI工作空间
- **核心功能**：助力用户高效完成**思考、研究、写作**等知识相关工作
- **产品优势**：使用更便捷、体量更轻量化、更贴合用户使用需求

---

### OmniBox（小黑）产品介绍

- **时间**：2026-04-17T02:25:18Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/FAR4ucuj83hjk2i5ghXtQf)

## OmniBox（小黑）产品介绍
**OmniBox（小黑）**是一款简洁、跨平台的一站式**AI知识枢纽**，核心逻辑为先收集内容，再进行交互提问。

### 核心功能
- 可通过浏览器插件将网页主要内容保存至OmniBox
- 支持上传PDF、Word、PPT、MP3等格式文件，实现端到端解析与索引
- 提供Markdown编辑与渲染功能，支持公式、思维导图、流程图、时序图、甘特图、乐谱等展示
- 基于网络与本地数据库实现问答及内容创作
- iOS端Flash功能：快速捕捉灵感，支持语音录制与文本笔记
- iOS端可直接将文件无缝分享至OmniBox
- 微信机器人可随时随地保存文件、网页、视频、语音、文本及聊天记录至OmniBox
- 具备用户与团队系统、权限管理、共享管理、多租户、多语言、深色模式、移动端适配等功能

https://github.com/import-ai/omnibox

---

## 学习与知识管理

### 学习即遗忘，理解即压缩。

- **时间**：2026-04-16T01:08:25Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/XpeivLXdzvtTdvtMV3fwEs)

学习即遗忘，理解即压缩。

---

### DocFlow团队协作块级文档编辑器

- **时间**：2026-04-17T01:27:40Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/maG7GE8CDcLwaMm7NLa9aR)

## DocFlow团队协作块级文档编辑器
- **项目地址**：https://github.com/xun082/DocFlow
- **项目定位**：面向团队协作的**块级文档编辑器**
- **核心优势**
  1. 融合**Notion的灵活性**与**飞书的协作能力**
  2. 采用**块级内容架构**，内容组织更灵活
  3. 支持**实时协同编辑**，提升团队协作效率
  4. 搭载**AI辅助功能**，优化创作体验
- **项目价值**：助力团队高效完成文档创作与知识管理工作

---

### NoteDiscovery 简介

- **时间**：2026-04-17T02:20:54Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/h5omRS9FVdSgowZkMaN3J3)

## NoteDiscovery 简介
**NoteDiscovery** 是一款**轻量级、可自托管**的笔记应用，让用户完全掌控个人知识库。

其核心功能与特点如下：
- 支持**编写、整理、检索**笔记内容
- 拥有**美观、现代化**的操作界面
- 所有数据与服务均运行在**用户自有服务器**上

https://github.com/gamosoft/NoteDiscovery

---

## 工具与流程 · Hexo

### Hexo Skill 详细介绍

- **时间**：2026-04-19T02:28:39Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/56xUfv2Hmd4a6a6LtGkktd)

## Hexo Skill 详细介绍

这是一个 **Hexo 静态博客管理** 的 Skill，覆盖了从建站到发布的完整工作流。

### 是什么

Hexo 是基于 Node.js 的静态博客框架，用 Markdown 写文章，生成静态 HTML。这个 Skill 就是让 AI 能帮你操作 Hexo 的完整指南。

### 前置条件

- Node.js 20.19.0+
- Git
- `npm install -g hexo-cli`

### 覆盖的 6 大核心能力

| 能力 | 说明 |
|------|------|
| **初始化建站** | `hexo init` 创建项目，自动生成 `_config.yml`、`source/`、`scaffolds/`、`themes/` 等目录结构 |
| **内容创建** | 支持三种类型：`post`（文章）、`page`（页面）、`draft`（草稿），以及草稿发布 `hexo publish` |
| **Front-Matter** | 完整的 YAML 元数据规范——title、date、tags、categories、permalink、excerpt、comments 等字段 |
| **自定义 Scaffold** | 模板机制，支持 `{{ layout }}`、`{{ title }}`、`{{ date }}` 占位符，可创建 photo、video、link、quote 等自定义布局 |
| **生成 & 预览** | `hexo server` 本地预览（默认 4000 端口），`hexo generate` 生成静态文件到 `public/` |
| **部署** | 支持 Git 部署到 GitHub Pages，包含 `hexo g -d` 一键生成+部署组合命令 |

### 内置的常见工作流

1. **从零建站**：`init` → 配置 `_config.yml` → `new post` → `server` 预览
2. **发布文章**：`new draft` → 编辑 → `server --drafts` 预览 → `publish` → `clean && g -d` 部署
3. **自定义布局**：在 `scaffolds/` 创建模板 → `hexo new <layout>` 使用

### 配置要点

Skill 里列出了 `_config.yml` 的关键配置项：站点信息（title/subtitle/author）、URL 规则（permalink 格式）、写作设置（文件命名格式、默认布局）、目录结构、分页等。

### 故障排除

- 端口冲突 → `hexo server -p 5000`
- 改了不生效 → `hexo clean && hexo generate`
- 部署失败 → 检查 `hexo-deployer-git` 插件、deploy 配置、Git 凭证

### 引用的子文档

Skill 提到了 4 个参考文档（`references/` 和 `examples/` 目录下），包括命令参考、Front-Matter 完整指南、GitHub Pages 部署指南、自定义 Scaffold 示例。不过这些文档目前不一定存在于 skill 目录中——刚才 glob 扫描目录都没找到，说明这个 skill 只有主文件 `SKILL.md`，没有附带引用文件。

### 一句话总结

这个 Skill 的定位是 **Hexo 全流程操作手册**，让 AI 能帮你初始化博客、创建内容（文章/页面/草稿）、配置站点、自定义模板、本地预览、部署上线。触发词包括"create a Hexo site"、"initialize Hexo"、"create a Hexo post"等。

---

## 工具与流程 · Memos

### Memos Skill 更新日志

- **时间**：2026-04-19T01:57:30Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/4ebdu8ZnxpuRfCSkR49PyE)

# Memos Skill 更新日志

## 2026-04-19 修复 Windows 下中文乱码问题

### 问题背景

在 Windows 环境下使用 `memos.py create` 保存中文内容到 Memos 时遇到一系列编码问题：

1. PowerShell 把 Markdown 中的 `—`、引号等特殊字符当成参数分隔符
2. `sys.argv` 无法可靠传递包含中文+特殊字符+多行的长内容
3. `requests` 的 `json=` 参数在 Windows 上不保证 UTF-8 编码，导致服务端存储乱码
4. Windows 控制台默认 GBK 编码，遇到 emoji 直接崩溃

### 改动内容（4 处）

#### 1. `_request` 函数显式 UTF-8 编码

有 body 时改为手动序列化并发送 UTF-8 bytes，而非依赖 `requests` 的 `json=` 参数：

```python
if data is not None:
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req_headers = {**HEADERS, "Content-Type": "application/json; charset=utf-8"}
    resp = requests.request(method, url, headers=req_headers, data=body, params=params, timeout=30)
else:
    resp = requests.request(method, url, headers=HEADERS, params=params, timeout=30)
```

#### 2. `create` 命令支持 `--file` 和 stdin

新增两种内容输入方式，彻底绕开 shell 编码问题：

```bash
# 从文件读取（推荐长内容和非 ASCII 内容使用）
python memos.py create --file content.md "PUBLIC"

# 从 stdin 读取（管道友好）
type content.md | python memos.py create - "PUBLIC"
```

原有直接传字符串的方式保留不变，三种模式互不干扰。

#### 3. 所有 `json.dumps` 输出加 `ensure_ascii=False`

`__main__` 入口的 5 处 `json.dumps` 调用全部加上 `ensure_ascii=False`，控制台返回中文原字而非 `\uXXXX` 转义。

#### 4. stdout/stderr 强制 UTF-8

在 `__main__` 入口处添加：

```python
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
```

解决 Windows GBK 控制台遇到 emoji（如 🌱）就崩溃的问题。

### 同步更新

- `SKILL.md` 命令表新增 `--file` 和 stdin 两种用法
- Direct Python Usage 示例新增对应示例

### 影响范围

仅修改 `memos.py` 一个文件 + `SKILL.md` 文档更新，所有改动向后兼容，原有 API 调用方式不受影响。

#AI-Agent

---

## 阅读与思辨

### 拥抱稀缺：如何培养深度阅读与批判性思维能力-36氪

- **时间**：2026-04-19T01:33:05Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/a4ypFEgsonSJSJLckzk2YX)

## 拥抱稀缺：如何培养深度阅读与批判性思维能力-36氪

### 摘要
在信息过载和社交媒体主导的时代，深度阅读与批判性思维能力变得稀缺但至关重要；作者主张通过主动、缓慢、社交化的深度阅读来抵御虚假信息、缓解孤独感，并培养更有意义的信息消费习惯。

### 要点
- 社交媒体算法通过重复曝光制造'虚假真相'效应，削弱批判判断
- 深度阅读是主动的批判性思考、分析解读和共情理解的过程
- 盲目刷屏与无聊感、孤独感、存在焦虑相关，而深度阅读能强化目标感和社交联结
- 放慢阅读节奏、主动判断信息真伪可以抵消虚假信息的影响
- 从短篇文本开始，设定社交共读目标，逐步培养深度阅读习惯

### 引述
> 深度阅读既能有效抵御虚假信息，又能缓解压力与孤独感。
> 深度阅读则指通过批判性思考、分析性解读和共情性理解主动接触信息的过程。
> 深度阅读意味着主动掌控阅读节奏：在遇到艰深段落时放慢速度反复揣摩，品味精彩的文字，批判性地看待信息，并思考文本的深层含义。

### 不同意见与局限
- 深度阅读过程可能引发烦躁或困惑等负面情绪，往往令人不适
- 人们能投入的精力和注意力是有限的，深度阅读需要刻意引导认知资源
- 社交媒体也可成为积极工具，如BookTok社区证明深度解析在社交媒体中仍有立足之地

---
来源: https://36kr.com/p/3652837081719170
#深度阅读 #批判性思维 #信息消费

---

## 阅读摘录

### 如何在一天之内重塑你的人生-36氪

- **时间**：2026-04-19T01:31:06Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/b4PTmGrVBNYQGPowwnF7Ct)

## 如何在一天之内重塑你的人生-36氪

### 摘要
认为新年计划失败源于人们错误地追求表面行为改变而非身份重塑，提出通过一天内完成心理挖掘、中断自动驾驶模式、整合洞察的暴力方案，将人生重构为一场有愿景、目标、约束的电子游戏，以实现真正的身份转变和持续进步。

### 要点
- 真正的改变不是靠自律硬撑，而是身份的彻底推倒重来
- 人们失败是因为追求错误的目标，这些目标往往服务于无意识的自我保护目的
- 身份由目标、行动、反馈循环构建，改变必须打破身份维持的心理一致性
- 智力是获取理想生活的能力，表现为迭代、坚持和理解大局的控制论系统
- 提出一天内完成的三部分方案：心理挖掘揭示隐藏动机，中断自动驾驶模式，整合洞察确立行动方向
- 将人生重构为有反面愿景、愿景、年度目标、月度项目、每日杠杆、约束条件的电子游戏
- 游戏化设计能产生痴迷、心流，使新身份成为自然享受而非勉强坚持

### 引述
> 预期的结果，源于长期的预演。在目标达成之前，你的生活方式必须先行。
> 测试智力唯一的真正手段，就是看你是否得到了你想要的生活。
> 我人生中最美好的阶段，总是出现在我对停滞不前感到彻底厌倦之后。
> 内在体验的最佳状态是意识中充满了秩序。当心理能量（即注意力）投入到现实的目标中，且个人技能与行动机会相匹配时，这种状态就会出现。

### 不同意见与局限
- 作者承认无法保证方案对每个人都有效，因为需要读者恰好处在人生的特定篇章
- 方案需要整整一天时间完成，对忙碌人群可能构成实践门槛
- 身份转变的快速发生（6个月取得6年进展）可能过于理想化
- 游戏化比喻可能简化了现实生活的复杂性和不可控因素

---
来源: https://36kr.com/p/3667384945468291
#身份转变 #行为改变 #游戏化设计

---

## 随笔与摘录

### 公开分享的好处，是让人知道你的能力，然后当有人有需求且你的能力匹配时，会主动找上你。

- **时间**：2026-04-16T00:33:48Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/7gmPbJsR7364bdYZfxYyxN)

公开分享的好处，是让人知道你的能力，然后当有人有需求且你的能力匹配时，会主动找上你。

---

### 美图推出AI设计工具Zawa（原名X-Design）

- **时间**：2026-04-16T00:38:39Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/nUpFg2pw3BVWf5H8JhfNdL)

## 美图推出AI设计工具Zawa（原名X-Design）
美图推出**AI设计工具Zawa（原名X-Design）**，可助力用户快速完成品牌视觉设计，涵盖Logo、海报、社媒素材等创作。该工具提供一站式设计服务，支持搭建品牌库，内置基础图片编辑功能与多元AI工具，用户还能通过标注改图功能调整设计细节。

### 核心亮点
1. 由**美图公司**研发，主打**品牌视觉设计**场景。
2. 提供一站式服务，可制作Logo、海报、社媒素材等设计内容。
3. 支持创建**品牌库**，保障设计风格统一规范。
4. 集成常用图片编辑功能与丰富AI设计工具。
5. 支持**标注改图**，可灵活精细化调整设计细节。

https://zawa.ai

---

### 如果一篇文章 不是 AI 写的 都没啥兴趣看了 AI 的质量 高人类太多

- **时间**：2026-04-16T00:47:23Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/8yfTKMT5tZjY7sKGdEw76c)

如果一篇文章
不是 AI 写的
都没啥兴趣看了

AI 的质量
高人类太多

---

### AI时代不易被替代的谦狂之人

- **时间**：2026-04-16T00:57:31Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/bgUMq3HxrkAaJRtrvEqA56)

## AI时代不易被替代的谦狂之人
AI时代，不会被替代的核心是**谦狂兼具**的人，这类人因“可爱”而具备不可替代性。

- **谦**：是智识上的诚实与人格上的自律。懂得倾听并融合他人想法，懂得换位思考；即便与AI对话，也能为其创造条件、善用工具，始终保持谦逊姿态。
- **狂**：是精神上的勇气与生命中的行动力。拥有坚定自信，敢于判断、敢于抉择，敢于凭借审美与直觉行事，正如“仰天大笑出门去，我辈岂是蓬蒿人”的气魄。

木心曾言：不谦而狂，狂无根基；不狂而谦，谦无意义。
唯有**谦狂交作**，方能成为独特且鲜活的人，在AI时代始终不可被替代。

---

### “在场”：真诚联结的核心

- **时间**：2026-04-16T01:02:45Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/DbrLQ9rVdzo3QreUvJTcf9)

## “在场”：真诚联结的核心
“在场”越品越有味，它不只是回应，更是**注视、感受与看见**对方。

1. 我们反感敷衍式沟通，本质是缺少**在场感**
- 反感朋友敷衍回复，因对方并未真正在场
- 反感心不在焉的交流，因彼此都不在场
- 反感群发消息，因发信人并未在场
- 冰冷编号的群聊易沉寂，因群主缺乏在场

2. **活人感**，就是最真实的在场
- 偏爱有活人感的内容，排斥刻板背稿，因背稿时不在场
- 偏爱有温度的活动，排斥空洞高大上，因流程化执行时不在场

3. 关系的转折，藏在关键时刻的在场或缺席
当再也感受不到一个人的**在场**时，便意味着彻底失去了对方。

---

### 对你而言最珍贵的三个词是什么呢？ 如果是名词：健康，家人，复利 如果是动词：聚焦，对齐，分享

- **时间**：2026-04-16T01:26:43Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/AHGg9Jj4eyZKHXAqp3CDYP)

对你而言最珍贵的三个词是什么呢？

如果是名词：健康，家人，复利
如果是动词：聚焦，对齐，分享
如果是形容词：安全的，自由的，简单的
如果是数词：2（多维度阴阳二分），7（5W2H），20（20条清单体）

---

### 帮助你的人可以不用多，但坏你事儿的人一定要少

- **时间**：2026-04-16T01:47:40Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/bt4Etb6gW58YYyrgyeveTU)

帮助你的人可以不用多，但坏你事儿的人一定要少

---

### cloudimgs云图库项目

- **时间**：2026-04-17T01:51:53Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/VC38ykDiLHmKWWJgh9ebtx)

## cloudimgs云图库项目
- **项目地址**：https://github.com/qazzxxx/cloudimgs
- **项目定位**：**极简风格无数据库云图库与图床项目**
- **部署支持**：支持**NAS部署**
- **安全能力**：支持**设置密钥**保障使用安全
- **扩展能力**：提供**灵活API开放接口**
- **便捷使用**：可作为**NAS图床**，支持**PicGo插件直接安装使用**

---

### markdown2png工具介绍

- **时间**：2026-04-17T01:56:54Z
- **原文**：[在 Memos 中打开](https://ke.zixi.run/memos/gAvqgA4wLBRBj3N6CgoqHP)

## markdown2png工具介绍
- **项目地址**：https://github.com/nicejade/markdown2png
- **项目说明**：
  1. 可**一键将Markdown转换为精美图片**
  2. 支持**书摘模式**
  3. 支持**自定义主题、字体及背景**

---
