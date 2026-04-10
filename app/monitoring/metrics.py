from prometheus_client import Counter, Gauge, Histogram, Summary
import time

# 定义监控指标

# 请求计数器
REQUEST_COUNT = Counter('omniagent_requests_total', 'Total number of requests', ['method', 'endpoint', 'status'])

# 处理时间直方图
REQUEST_DURATION = Histogram('omniagent_request_duration_seconds', 'Request processing time in seconds', ['method', 'endpoint'])

# 内存使用情况
MEMORY_USAGE = Gauge('omniagent_memory_usage_bytes', 'Memory usage in bytes')

# 技能使用计数器
SKILL_USAGE = Counter('omniagent_skill_usage_total', 'Total number of skill executions', ['skill_name'])

# 消息处理计数器
MESSAGE_PROCESSED = Counter('omniagent_messages_processed_total', 'Total number of messages processed')

# 记忆操作计数器
MEMORY_OPERATIONS = Counter('omniagent_memory_operations_total', 'Total number of memory operations', ['operation'])

# 错误计数器
ERROR_COUNT = Counter('omniagent_errors_total', 'Total number of errors', ['error_type'])

# 系统健康状态
SYSTEM_HEALTH = Gauge('omniagent_system_health', 'System health status (1=healthy, 0=unhealthy)')

# 处理时间摘要
PROCESSING_TIME = Summary('omniagent_processing_time_seconds', 'Processing time summary')

# 向量存储操作计数器
VECTOR_STORAGE_OPERATIONS = Counter('omniagent_vector_storage_operations_total', 'Total number of vector storage operations', ['operation'])

# 技能验证状态
SKILL_VERIFICATION_STATUS = Gauge('omniagent_skill_verification_status', 'Skill verification status (1=verified, 0=pending, -1=rejected)', ['skill_name'])

# 装饰器：记录请求处理时间
def track_request_duration(method, endpoint):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                status = 200
                return result
            except Exception as e:
                status = 500
                ERROR_COUNT.labels(error_type=type(e).__name__).inc()
                raise
            finally:
                duration = time.time() - start_time
                REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
                REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
        return wrapper
    return decorator

# 装饰器：记录处理时间
def track_processing_time(func):
    def wrapper(*args, **kwargs):
        with PROCESSING_TIME.time():
            return func(*args, **kwargs)
    return wrapper

# 记录技能使用
def record_skill_usage(skill_name):
    SKILL_USAGE.labels(skill_name=skill_name).inc()

# 记录消息处理
def record_message_processed():
    MESSAGE_PROCESSED.inc()

# 记录内存操作
def record_memory_operation(operation):
    MEMORY_OPERATIONS.labels(operation=operation).inc()

# 记录向量存储操作
def record_vector_storage_operation(operation):
    VECTOR_STORAGE_OPERATIONS.labels(operation=operation).inc()

# 更新系统健康状态
def set_system_health(healthy):
    SYSTEM_HEALTH.set(1 if healthy else 0)

# 更新技能验证状态
def set_skill_verification_status(skill_name, status):
    # status: 1=verified, 0=pending, -1=rejected
    if status == 'Verified':
        SKILL_VERIFICATION_STATUS.labels(skill_name=skill_name).set(1)
    elif status == 'Pending Review':
        SKILL_VERIFICATION_STATUS.labels(skill_name=skill_name).set(0)
    elif status == 'Rejected':
        SKILL_VERIFICATION_STATUS.labels(skill_name=skill_name).set(-1)