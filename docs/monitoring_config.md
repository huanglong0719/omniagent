# OmniAgent 监控系统配置

## 1. 监控系统架构

### 1.1 组件
- **Prometheus**：时间序列数据库，用于存储监控指标
- **Grafana**：可视化仪表板，用于展示监控数据
- **Node Exporter**：收集主机级别的监控指标
- **Application Exporter**：收集应用级别的监控指标

### 1.2 监控指标

#### 1.2.1 系统级指标
- CPU 使用率
- 内存使用率
- 磁盘使用率
- 网络流量

#### 1.2.2 应用级指标
- 消息处理时间
- 消息队列长度
- API 响应时间
- 错误率
- 技能调用次数
- 内存操作性能

## 2. 配置文件

### 2.1 Docker Compose 配置

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:v2.45.0
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    restart: always

  grafana:
    image: grafana/grafana:9.5.0
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    restart: always

  node_exporter:
    image: prom/node-exporter:v1.5.0
    ports:
      - "9100:9100"
    restart: always

volumes:
  prometheus_data:
  grafana_data:
```

### 2.2 Prometheus 配置

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['node_exporter:9100']

  - job_name: 'omniagent'
    static_configs:
      - targets: ['host.docker.internal:8000']
    metrics_path: '/metrics'
```

### 2.3 Grafana 仪表板配置

#### 2.3.1 系统监控仪表板

```json
{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "id": null,
  "links": [],
  "panels": [
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 0
      },
      "id": 2,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "9.5.0",
      "targets": [
        {
          "datasource": "Prometheus",
          "expr": "100 - (avg by(instance) (irate(node_cpu_seconds_total{mode='idle'}[5m])) * 100)",
          "interval": "",
          "legendFormat": "{{instance}}",
          "refId": "A"
        }
      ],
      "title": "CPU 使用率",
      "type": "stat"
    },
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 0
      },
      "id": 3,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "9.5.0",
      "targets": [
        {
          "datasource": "Prometheus",
          "expr": "100 * (1 - ((node_memory_MemAvailable_bytes) / (node_memory_MemTotal_bytes)))",
          "interval": "",
          "legendFormat": "{{instance}}",
          "refId": "A"
        }
      ],
      "title": "内存使用率",
      "type": "stat"
    },
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 8
      },
      "id": 4,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "9.5.0",
      "targets": [
        {
          "datasource": "Prometheus",
          "expr": "100 * (1 - ((node_filesystem_avail_bytes{mountpoint='/'} ) / (node_filesystem_size_bytes{mountpoint='/'})))",
          "interval": "",
          "legendFormat": "{{instance}}",
          "refId": "A"
        }
      ],
      "title": "磁盘使用率",
      "type": "stat"
    },
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 8
      },
      "id": 5,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "9.5.0",
      "targets": [
        {
          "datasource": "Prometheus",
          "expr": "rate(node_network_transmit_bytes_total[5m]) + rate(node_network_receive_bytes_total[5m])",
          "interval": "",
          "legendFormat": "{{instance}}",
          "refId": "A"
        }
      ],
      "title": "网络流量",
      "type": "stat"
    }
  ],
  "refresh": "10s",
  "schemaVersion": 38,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-1h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "系统监控",
  "uid": "system-monitoring",
  "version": 1
}
```

#### 2.3.2 应用监控仪表板

```json
{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "id": null,
  "links": [],
  "panels": [
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 0
      },
      "id": 2,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "9.5.0",
      "targets": [
        {
          "datasource": "Prometheus",
          "expr": "rate(omniagent_message_processing_time_seconds_sum[5m]) / rate(omniagent_message_processing_time_seconds_count[5m])",
          "interval": "",
          "legendFormat": "平均处理时间",
          "refId": "A"
        }
      ],
      "title": "消息处理时间",
      "type": "stat"
    },
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 0
      },
      "id": 3,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "9.5.0",
      "targets": [
        {
          "datasource": "Prometheus",
          "expr": "omniagent_message_queue_length",
          "interval": "",
          "legendFormat": "队列长度",
          "refId": "A"
        }
      ],
      "title": "消息队列长度",
      "type": "stat"
    },
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 8
      },
      "id": 4,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "9.5.0",
      "targets": [
        {
          "datasource": "Prometheus",
          "expr": "rate(omniagent_api_response_time_seconds_sum[5m]) / rate(omniagent_api_response_time_seconds_count[5m])",
          "interval": "",
          "legendFormat": "平均响应时间",
          "refId": "A"
        }
      ],
      "title": "API 响应时间",
      "type": "stat"
    },
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 8
      },
      "id": 5,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "9.5.0",
      "targets": [
        {
          "datasource": "Prometheus",
          "expr": "rate(omniagent_error_count[5m])",
          "interval": "",
          "legendFormat": "错误率",
          "refId": "A"
        }
      ],
      "title": "错误率",
      "type": "stat"
    },
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 16
      },
      "id": 6,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "9.5.0",
      "targets": [
        {
          "datasource": "Prometheus",
          "expr": "rate(omniagent_skill_calls_total[5m])",
          "interval": "",
          "legendFormat": "技能调用次数",
          "refId": "A"
        }
      ],
      "title": "技能调用次数",
      "type": "stat"
    },
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 16
      },
      "id": 7,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "9.5.0",
      "targets": [
        {
          "datasource": "Prometheus",
          "expr": "rate(omniagent_memory_operations_seconds_sum[5m]) / rate(omniagent_memory_operations_seconds_count[5m])",
          "interval": "",
          "legendFormat": "平均操作时间",
          "refId": "A"
        }
      ],
      "title": "内存操作性能",
      "type": "stat"
    }
  ],
  "refresh": "10s",
  "schemaVersion": 38,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-1h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "应用监控",
  "uid": "application-monitoring",
  "version": 1
}
```

## 3. 应用监控指标实现

### 3.1 安装依赖

```bash
pip install prometheus-client
```

### 3.2 监控指标代码

```python
# app/monitoring/metrics.py
from prometheus_client import Counter, Gauge, Histogram

# 消息处理指标
message_processing_time = Histogram(
    'omniagent_message_processing_time_seconds',
    'Time taken to process messages',
    ['channel', 'message_type']
)

message_queue_length = Gauge(
    'omniagent_message_queue_length',
    'Current message queue length'
)

# API 指标
api_response_time = Histogram(
    'omniagent_api_response_time_seconds',
    'API response time',
    ['endpoint', 'method']
)

# 错误指标
error_count = Counter(
    'omniagent_error_count',
    'Number of errors',
    ['error_type']
)

# 技能指标
skill_calls = Counter(
    'omniagent_skill_calls_total',
    'Number of skill calls',
    ['skill_name']
)

# 内存操作指标
memory_operations = Histogram(
    'omniagent_memory_operations_seconds',
    'Memory operation time',
    ['operation_type']
)
```

### 3.3 集成到 FastAPI

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import start_http_server, Summary
from app.monitoring.metrics import (
    message_processing_time,
    api_response_time,
    error_count,
    skill_calls,
    memory_operations
)

app = FastAPI(
    title="OmniAgent API",
    description="OmniAgent - 综合性AI代理系统",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 启动 Prometheus 指标服务器
start_http_server(8000)

# 示例路由
@app.get("/metrics")
def get_metrics():
    """Prometheus metrics endpoint"""
    from prometheus_client import generate_latest
    return generate_latest()

@app.post("/messages")
async def process_message(message: dict):
    """Process incoming message"""
    with message_processing_time.labels(channel=message.get('channel', 'unknown'), message_type=message.get('type', 'text')).time():
        # 处理消息逻辑
        pass
    return {"status": "success"}

@app.get("/skills")
async def get_skills():
    """Get available skills"""
    with api_response_time.labels(endpoint="/skills", method="GET").time():
        # 获取技能逻辑
        pass
    return {"skills": []}
```

## 4. 部署和运行

### 4.1 启动监控服务

```bash
# 启动 Prometheus 和 Grafana
docker-compose up -d

# 查看服务状态
docker-compose ps
```

### 4.2 访问监控仪表板

- **Prometheus**：http://localhost:9090
- **Grafana**：http://localhost:3000 (用户名: admin, 密码: admin)

### 4.3 导入仪表板

1. 登录 Grafana
2. 点击左侧菜单的 "+" 图标
3. 选择 "Import"
4. 粘贴仪表板 JSON 配置
5. 点击 "Import"

## 5. 告警配置

### 5.1 Prometheus 告警规则

```yaml
# prometheus/rules/alert.rules
groups:
- name: omniagent_alerts
  rules:
  - alert: HighCPUUsage
    expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode='idle'}[5m])) * 100) > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High CPU Usage"
      description: "CPU usage is above 80% for 5 minutes"

  - alert: HighMemoryUsage
    expr: 100 * (1 - ((node_memory_MemAvailable_bytes) / (node_memory_MemTotal_bytes))) > 85
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High Memory Usage"
      description: "Memory usage is above 85% for 5 minutes"

  - alert: HighErrorRate
    expr: rate(omniagent_error_count[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High Error Rate"
      description: "Error rate is above 0.1 errors per second for 5 minutes"

  - alert: SlowResponseTime
    expr: rate(omniagent_api_response_time_seconds_sum[5m]) / rate(omniagent_api_response_time_seconds_count[5m]) > 1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Slow Response Time"
      description: "API response time is above 1 second for 5 minutes"
```

### 5.2 Grafana 告警渠道

1. 登录 Grafana
2. 点击左侧菜单的 "Alerting" -> "Notification channels"
3. 点击 "New channel"
4. 配置告警渠道（如 Email、Slack、Webhook 等）
5. 点击 "Save"

## 6. 总结

本监控系统配置提供了全面的系统和应用监控能力，包括：

- 系统级指标监控（CPU、内存、磁盘、网络）
- 应用级指标监控（消息处理、API 响应、错误率、技能调用）
- 可视化仪表板展示
- 告警机制

通过这套监控系统，您可以实时了解 OmniAgent 的运行状态，及时发现并解决潜在问题，确保系统的稳定性和可靠性。
