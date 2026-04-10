# OmniAgent 产品验收标准 (Acceptance Criteria)

本文档定义了 OmniAgent 从原型到产品化过程中必须满足的验收标准。每个功能点需通过对应的测试场景验证方可视为“完成”。

---

## 1. 接口层 (OmniGateway) 验收标准

### AC 1.1: 多渠道统一接入
- **验收项**：系统能够同时接收来自 Telegram, WhatsApp, Web 等至少三种渠道的消息。
- **验证场景**：
    - **WHEN** 用户在 Telegram 发送消息 $\rightarrow$ **THEN** 服务器能正确解析并路由至 OmniBrain。
    - **WHEN** 用户在 WhatsApp 发送消息 $\rightarrow$ **THEN** 服务器能正确解析并路由至 OmniBrain。

### AC 1.2: 跨渠道会话一致性
- **验收项**：同一用户在不同渠道的对话能够共享同一个 Session。
- **验证场景**：
    - **WHEN** 用户在 Web 端告知 AI 自己的姓名 $\rightarrow$ 随后在 Telegram 端询问“我是谁” $\rightarrow$ **THEN** AI 能准确回答。

### AC 1.3: 隐私过滤有效性
- **验收项**：所有进入存储层的数据必须经过脱敏处理。
- **验证场景**：
    - **WHEN** 用户输入包含信用卡号或密码 $\rightarrow$ **THEN** 存储在 L3 存档中的内容应被替换为 `[SENSITIVE_DATA]`。

---

## 2. 存储层 (OmniMemory) 验收标准

### AC 2.1: 分级存储结构
- **验收项**：L1 (Redis), L2 (Vector DB), L3 (SQL) 存储链路畅通。
- **验证场景**：
    - **WHEN** 消息产生 $\rightarrow$ **THEN** 验证该消息同时存在于 L3 (全量) 和 L2 (向量索引) 中。

### AC 2.2: 虚拟内存分页 (Paging)
- **验收项**：AI 能根据当前需求自主触发 `page_in` 和 `page_out`。
- **验证场景**：
    - **WHEN** 用户询问一个一个月前的细节 $\rightarrow$ **THEN** 观察日志，确认系统触发了 L2 $\rightarrow$ L1 的 `page_in` 操作。

### AC 2.3: 预测性预取 (Prefetching)
- **验收项**：在 LLM 生成响应前，相关记忆已提前加载至 L1。
- **验证场景**：
    - **WHEN** 用户输入“关于之前的那个项目...” $\rightarrow$ **THEN** 验证系统在调用 LLM 之前已异步加载相关项目记忆。

---

## 3. 认知层 (EvolutionEngine) 验收标准

### AC 3.1: 技能自主提取
- **验收项**：任务成功后，系统能自动生成结构化的 Markdown 技能文件。
- **验证场景**：
    - **WHEN** AI 成功完成一个复杂任务并收到用户肯定 $\rightarrow$ **THEN** `omniagent/skills/` 目录下出现一个新的 `.md` 技能文件。

### AC 3.2: 技能检索与应用
- **验收项**：在类似任务中，AI 能优先调用已习得的技能而非重新思考。
- **验证场景**：
    - **WHEN** 用户发起一个与已存技能匹配的任务 $\rightarrow$ **THEN** 响应中应包含 `[Applied Skill]` 标记，且执行步骤与技能库一致。

### AC 3.3: 技能验证机制
- **验收项**：只有通过验证的技能才被标记为 `Stable`。
- **验证场景**：
    - **WHEN** 新技能生成 $\rightarrow$ **THEN** 系统自动运行 3 个测试用例 $\rightarrow$ 只有全部通过才更新状态为 `Stable`。

---

## 4. 编排层 (OmniBrain) 验收标准

### AC 4.1: 动态模式切换
- **验收项**：系统能根据任务复杂度自动选择单体或多体模式。
- **验证场景**：
    - **WHEN** 输入“你好” $\rightarrow$ **THEN** 触发 `Single-Agent` 模式。
    - **WHEN** 输入“调研 AI 市场并写报告” $\rightarrow$ **THEN** 触发 `Multi-Agent Crew` 模式。

### AC 4.2: 多智能体协作质量
- **验收项**：协作流（研究 $\rightarrow$ 撰写 $\rightarrow$ 审核）完整执行且结果连贯。
- **验证场景**：
    - **WHEN** 启动 Crew 模式 $\rightarrow$ **THEN** 验证日志中依次出现 Researcher, Writer, Critic 的执行记录。

---

## 5. 综合性能与安全验收

### AC 5.1: 响应延迟
- **验收项**：简单请求端到端延迟 $< 2s$。

### AC 5.2: 数据加密
- **验收项**：L3 存储中的敏感字段必须经过 AES-256 加密。

### AC 5.3: 稳定性
- **验收项**：在 10 次连续复杂请求中，无 503/429 导致的任务中断（通过重试机制实现）。
