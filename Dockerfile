# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt 文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p omniagent/skills/templates

# 暴露端口（如果需要）
EXPOSE 8000

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV OMNIA_GENT_CONFIG=config.json

# 运行应用
CMD ["python", "app/main.py"]