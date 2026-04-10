# OmniAgent

## 项目简介

OmniAgent 是一个综合性的 AI 代理系统，整合了多个现有项目的优秀特性，包括 Hermes Agent、OpenClaw、MemGPT、AutoGen/CrewAI 等，实现了一个功能强大、性能优异的智能代理系统。

## 核心功能

### 1. 安全与隐私保护
- **AES-256 加密存储**：实现了敏感数据的加密存储，确保用户数据安全
- **隐私过滤**：自动检测和过滤敏感信息，保护用户隐私
- **环境变量配置**：通过环境变量管理敏感配置，避免硬编码

### 2. 多渠道支持
- **Telegram 适配器**：实现了 Telegram 消息接收和发送功能
- **WhatsApp 适配器**：实现了 WhatsApp 消息接收和发送功能
- **统一消息路由**：统一处理不同渠道的消息，确保一致性

### 3. 内存管理系统
- **分层内存架构**：L1 (快速缓存)、L2 (语义索引)、L3 (持久存储)
- **LRU 分页机制**：基于最近使用频率的智能分页，提高内存利用率
- **预测性预取**：基于主题频率的智能预取，提高响应速度
- **批处理优化**：实现了数据库操作的批处理，显著提高插入速度
- **数据库连接池**：减少数据库连接开销，提高性能

### 4. 技能进化系统
- **技能创建与管理**：支持创建、更新和删除技能
- **HITL 审核机制**：人工审核确保技能质量
- **技能验证系统**：自动验证技能的有效性和安全性

### 5. 多代理协作
- **LangGraph 集成**：实现了基于 LangGraph 的复杂协作流
- **动态模式切换**：根据任务复杂度自动切换单代理/多代理模式
- **任务类型识别**：基于关键词和内容分析识别任务类型，选择合适的工作流

### 6. 性能优化
- **消息插入速度**：100 条消息插入仅需 0.77 秒
- **并发性能**：50 个并发操作仅需 0.33 秒
- **压力测试**：1000 条消息插入仅需 7.00 秒

## 技术栈

- **后端框架**：FastAPI
- **数据库**：SQLite (本地存储)
- **向量存储**：本地向量索引 (模拟)
- **AI 模型**：Google Gemini API (支持代理)
- **多代理协作**：LangGraph
- **加密**：AES-256
- **消息渠道**：Telegram, WhatsApp

## 安装说明

### 1. 克隆仓库

```bash
git clone https://github.com/huanglong0719/omniagent.git
cd omniagent
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件并添加以下配置：

```env
# 加密密钥
ENCRYPTION_KEY=your_encryption_key

# LLM 配置
LLM_PROVIDER=google
GOOGLE_API_KEY=your_google_api_key

# 代理配置（可选）
HTTP_PROXY=http://localhost:10808

# 数据库配置
DB_PATH=omniagent.db
VECTOR_DB_URL=http://localhost:6333
```

### 4. 生成加密密钥

```bash
python scripts/generate_key.py
```

## 使用方法

### 1. 启动服务器

```bash
python main.py
```

### 2. 访问 API

默认情况下，服务器会在 `http://localhost:8000` 启动。

### 3. 测试核心功能

```bash
# 测试核心功能
python test_core_functions.py

# 测试性能
python tests/test_performance.py
```

## 项目结构

```
omniagent/
├── app/
│   ├── brain/          # 大脑模块（智能决策）
│   ├── core/           # 核心模块（配置、模型）
│   ├── evolution/      # 进化模块（技能管理）
│   ├── gateway/        # 网关模块（多渠道支持）
│   ├── memory/         # 内存模块（分层存储）
│   └── security/       # 安全模块（加密、隐私）
├── docs/               # 文档
├── scripts/            # 脚本工具
├── tests/              # 测试代码
├── .gitignore
├── main.py             # 主入口
└── requirements.txt    # 依赖配置
```

## 性能指标

| 测试项 | 性能 |
|-------|------|
| 100 条消息插入 | 0.77 秒 |
| 50 个并发操作 | 0.33 秒 |
| 1000 条消息插入 | 7.00 秒 |
| 操作/秒 | 151.80 ops/s |

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 联系方式

- GitHub: [huanglong0719](https://github.com/huanglong0719)
- 邮箱: your.email@example.com

---

**OmniAgent - 智能代理的未来**
