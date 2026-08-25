# 🐳 Docker 部署文档

## 文件说明

### 1. Dockerfile

后端应用的 Docker 镜像定义：

- 基础镜像：`python:3.11-slim`
- 安装 MySQL 客户端依赖
- 复制代码和依赖
- 暴露端口 8000
- 启动 uvicorn 服务器

### 2. docker-compose.yml

编排配置，简化部署：

- 自动构建镜像
- 环境变量配置
- 端口映射
- 健康检查
- 自动重启策略

### 3. .dockerignore

排除不必要的文件：

- Python 缓存
- 前端代码
- 开发工具配置
- 敏感的 .env 文件

### 4. .env.docker

Docker Compose 环境变量文件

---

## 快速开始

### 方式 1: 使用构建脚本（推荐）

```bash
# 1. 构建镜像
./docker-build.sh

# 2. 启动容器
docker-compose --env-file .env.docker up -d

# 3. 查看日志
docker logs -f anxingban-backend

# 4. 访问服务
curl http://localhost:8000/docs
```

### 方式 2: 手动构建

```bash
# 1. 构建镜像
docker build -t anxingban-backend:latest .

# 2. 运行容器
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL='mysql+pymysql://root:12345@47.237.188.77:3306/anbanx?charset=utf8mb4' \
  -e TOKEN_SECRET='your-secret-key' \
  --name anxingban-backend \
  anxingban-backend:latest

# 3. 查看日志
docker logs -f anxingban-backend
```

---

## 常用命令

### 容器管理

```bash
# 启动
docker-compose up -d

# 停止
docker-compose down

# 重启
docker-compose restart

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
```

### 镜像管理

```bash
# 查看镜像
docker images | grep anxingban

# 删除旧镜像
docker rmi anxingban-backend:latest

# 重新构建
docker-compose build --no-cache
```

### 容器操作

```bash
# 进入容器
docker exec -it anxingban-backend bash

# 查看资源使用
docker stats anxingban-backend

# 查看健康状态
docker inspect anxingban-backend | grep Health -A 10
```

---

## 环境变量配置

### 必需变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `DATABASE_URL` | 数据库连接字符串 | `mysql+pymysql://user:pass@host:3306/db` |
| `TOKEN_SECRET` | JWT 密钥 | 随机生成的长字符串 |

### 可选变量

| 变量 | 默认值 | 说明 |
| ------ | -------- | ------ |
| `APP_NAME` | 安行伴-重庆试点 | 应用名称 |
| `ENVIRONMENT` | production | 运行环境 |
| `SMS_PROVIDER` | mock | 短信服务商 |
| `PILOT_CITY` | Chongqing | 试点城市 |

### 配置方式

**方式 1: 修改 .env.docker**

```bash
DB_HOST=your-db-host
DB_PASSWORD=your-password
TOKEN_SECRET=your-secret
```

**方式 2: docker-compose.yml 中直接设置**

```yaml
environment:
  - DATABASE_URL=mysql+pymysql://...
  - TOKEN_SECRET=...
```

**方式 3: docker run 命令行参数**

```bash
docker run -e DATABASE_URL='...' -e TOKEN_SECRET='...' ...
```

---

## 生产部署建议

### 1. 安全配置

```bash
# 生成安全的 TOKEN_SECRET
openssl rand -hex 32

# 使用密码管理工具（如 Docker Secrets）
echo "your-secret" | docker secret create token_secret -
```

### 2. 反向代理（Nginx）

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. HTTPS 配置

```bash
# 使用 Let's Encrypt
apt-get install certbot python3-certbot-nginx
certbot --nginx -d api.example.com
```

### 4. 资源限制

```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          memory: 512M
```

### 5. 日志管理

```yaml
# docker-compose.yml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 健康检查

容器自带健康检查，每 30 秒检查一次：

```bash
# 查看健康状态
docker inspect anxingban-backend | grep Health -A 10

# 手动测试健康端点
curl http://localhost:8000/docs
```

---

## 故障排查

### 容器无法启动

```bash
# 查看详细日志
docker logs anxingban-backend

# 检查配置
docker inspect anxingban-backend

# 检查网络
docker network ls
docker network inspect anxingban-network
```

### 数据库连接失败

```bash
# 进入容器测试连接
docker exec -it anxingban-backend bash
python3 -c "from app.database import engine; print(engine.connect())"
```

### 端口冲突

```bash
# 检查端口占用
netstat -tulpn | grep 8000

# 修改映射端口
docker run -p 8001:8000 ...
```

---

## 镜像优化

当前镜像大小约 **300MB**，可进一步优化：

### 1. 多阶段构建

```dockerfile
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app/ ./app/
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. 使用 Alpine

```dockerfile
FROM python:3.11-alpine
RUN apk add --no-cache gcc musl-dev mariadb-connector-c-dev
...
```

---

## CI/CD 集成

### GitHub Actions 示例

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t anxingban-backend:${{ github.sha }} .
      - name: Push to registry
        run: docker push anxingban-backend:${{ github.sha }}
```

---

## 监控和维护

### 1. 资源监控

```bash
# 实时监控
docker stats anxingban-backend

# 导出监控数据
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### 2. 日志分析

```bash
# 查看最近日志
docker logs --tail 100 anxingban-backend

# 跟踪日志
docker logs -f anxingban-backend

# 按时间过滤
docker logs --since 1h anxingban-backend
```

### 3. 定期更新

```bash
# 拉取最新代码
git pull

# 重新构建并部署
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

**完成时间**: 2026-08-21 17:15  
**Docker 版本**: 20.10+  
**Docker Compose 版本**: 2.0+
