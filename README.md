# OmniAgent

## 项目简介

OmniAgent 是一个综合性的 AI 代理系统，整合了多个现有项目的优秀特性，包括 Hermes Agent、OpenClaw、MemGPT、AutoGen/CrewAI 等，实现了一个功能强大、性能优异的智能代理系统。

## 核心功能

### 1. 安全与隐私保护
- **AES-256 加密存储**：实现了敏感数据的加密存储，确保用户数据安全
- **隐私过滤**：自动检测和过滤敏感信息，保护用户隐私
- **环境变量配置**：通过环境变量管理敏感配置，避免硬编码
- **认证和授权**：基于 JWT 的认证系统，支持用户注册、登录和权限管理

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
- **内存清理机制**：自动清理 inactive 会话和过期数据，避免内存泄漏
- **会话超时管理**：自动管理会话超时，释放资源

### 4. 技能进化系统
- **技能创建与管理**：支持创建、更新和删除技能
- **HITL 审核机制**：人工审核确保技能质量
- **技能验证系统**：自动验证技能的有效性和安全性
- **技能生成器**：基于模板自动生成技能
- **技能市场**：支持技能共享、评分和下载

### 5. 多代理协作
- **LangGraph 集成**：实现了基于 LangGraph 的复杂协作流
- **动态模式切换**：根据任务复杂度自动切换单代理/多代理模式
- **任务类型识别**：基于关键词和内容分析识别任务类型，选择合适的工作流

### 6. 用户界面
- **Vue.js 前端**：现代化的用户界面，支持响应式设计
- **仪表盘**：实时显示系统状态和关键指标
- **技能管理**：可视化的技能创建、编辑和管理
- **设置页面**：系统配置和用户偏好设置
- **监控页面**：系统性能和活动监控
- **多语言支持**：中文和英文国际化

### 7. API 接口
- **FastAPI 后端**：高性能的 RESTful API
- **系统状态接口**：获取系统健康状态和资源使用情况
- **技能管理接口**：创建、更新、删除和验证技能
- **监控数据接口**：获取系统性能和使用统计
- **用户管理接口**：用户注册、登录和权限管理

### 8. 性能优化
- **消息插入速度**：100 条消息插入仅需 0.77 秒
- **并发性能**：50 个并发操作仅需 0.33 秒
- **压力测试**：1000 条消息插入仅需 7.00 秒
- **内存优化**：自动清理和管理内存，避免内存泄漏
- **数据库优化**：批处理和连接池，减少数据库开销

## 技术栈

- **后端框架**：FastAPI
- **数据库**：SQLite (本地存储)
- **向量存储**：Qdrant (支持本地和远程部署)
- **AI 模型**：Google Gemini API (支持代理)
- **多代理协作**：LangGraph
- **加密**：AES-256
- **认证**：JWT
- **消息渠道**：Telegram, WhatsApp
- **前端框架**：Vue.js 3
- **UI 组件**：Element Plus
- **图表库**：ECharts
- **部署**：Docker, Kubernetes

## 安装说明

### 1. 克隆仓库

```bash
git clone https://github.com/huanglong0719/omniagent.git
cd omniagent
```

### 2. 安装后端依赖

```bash
pip install -r requirements.txt
```

### 3. 安装前端依赖

```bash
cd ui
npm install
```

### 4. 配置环境变量

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

# 认证配置
SECRET_KEY=your_jwt_secret_key
```

### 5. 生成加密密钥

```bash
python scripts/generate_key.py
```

## 使用方法

### 1. 启动后端服务器

```bash
python main.py
```

默认情况下，服务器会在 `http://localhost:8002` 启动。

### 2. 启动前端开发服务器

```bash
cd ui
npm run dev
```

### 3. 构建前端应用

```bash
cd ui
npm run build
```

### 4. 测试核心功能

```bash
# 测试核心功能
python test_core_functions.py

# 测试性能
python tests/test_performance.py
```

## 部署指南

### Docker 部署

1. 构建 Docker 镜像

```bash
docker build -t omniagent .
```

2. 运行 Docker 容器

```bash
docker run -p 8002:8002 --env-file .env omniagent
```

### Docker Compose 部署

1. 配置 `docker-compose.yml` 文件

2. 启动服务

```bash
docker-compose up -d
```

### Kubernetes 部署

1. 配置 Kubernetes 资源文件

2. 应用部署

```bash
kubectl apply -f k8s/deployment.yaml
```

## 项目结构

```
omniagent/
├── app/
│   ├── api/            # API 接口
│   ├── brain/          # 大脑模块（智能决策）
│   ├── core/           # 核心模块（配置、模型）
│   ├── evolution/      # 进化模块（技能管理）
│   ├── gateway/        # 网关模块（多渠道支持）
│   ├── memory/         # 内存模块（分层存储）
│   └── security/       # 安全模块（加密、隐私）
├── ui/                 # 前端应用
│   ├── public/         # 静态资源
│   ├── src/            # 源代码
│   │   ├── components/ # 组件
│   │   ├── i18n/       # 国际化
│   │   ├── pages/      # 页面
│   │   └── router/     # 路由
│   ├── index.html      # 入口 HTML
│   ├── package.json    # 前端依赖
│   └── vite.config.js  # Vite 配置
├── docker/             # Docker 配置
├── k8s/                # Kubernetes 配置
├── docs/               # 文档
├── scripts/            # 脚本工具
├── tests/              # 测试代码
├── .gitignore
├── docker-compose.yml  # Docker Compose 配置
├── Dockerfile          # Docker 配置
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

## API 文档

启动服务器后，可以访问以下地址查看 API 文档：

- Swagger UI: `http://localhost:8002/docs`
- ReDoc: `http://localhost:8002/redoc`

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
