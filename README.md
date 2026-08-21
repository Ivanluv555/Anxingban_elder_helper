# 安伴行（重庆试点）

这是一个可本地直接运行的真实产品 MVP（非演示模型），核心目标是帮助子女与长辈在出行过程中实现协同建档、行程安全保障、代际互动和回忆沉淀。

## 1. 这个 App 是怎么工作的

系统由两部分组成：

- 后端：FastAPI + SQLAlchemy + MySQL 8.0（PyMySQL 驱动）
- 前端：静态 Web App（PWA），由浏览器访问并调用后端 API

核心业务链路如下：

1. 家庭协同建档

- 子女填写父母和自己的联系方式、健康信息、兴趣偏好。
- 数据写入 profiles 表。

1. 创建行程并生成动态通行码

- 基于 profile 创建 trip。
- 服务端按 profile_id + trip_id + 时间戳 + 随机 nonce 生成 HMAC token。
- token 同步生成 SVG 二维码，返回给前端展示与复制。

1. 紧急求助（双通道）

- 前端触发 SOS 后调用 /api/sos/trigger。
- 服务端并行走短信与企业微信 webhook 两个通道（默认可 mock）。
- 同时记录 SOS 轨迹、网络状态、健康快照、通知状态。
- 前端离线时会先入本地队列，网络恢复后自动补发。

1. 代际挑战任务

- 子女创建任务（如拍照、打卡）。
- 长辈完成后可标记完成，子女发送反馈，累计爱心值。

1. 安伴行讲解（知识有限）

- 目前为重庆核心景点的受限问答。
- 返回 answer + confidence + scope（knowledge_limited）。

1. 生成数字回忆卡

- 从行程与已完成任务生成摘要。
- 结果写入 memory_cards 表，便于分享与回看。

## 2. 项目结构

- app/main.py：FastAPI 入口，挂载 API 路由和静态资源
- app/models.py：数据库模型（Profile/Trip/Task/SOSRecord/MemoryCard）
- app/routers/：各业务接口
- app/services/：动态通行码、通知、讲解服务
- app/static/：前端页面、脚本、样式、PWA 资源
- tests/test_api.py：核心流程回归测试
- scripts/smoke_test.py：HTTP 级冒烟链路脚本

## 3. 环境要求

### 3.1 运行环境

- 操作系统：Linux、macOS 或 Windows
- Python：3.10+
- MySQL：8.0+
- 包管理：pip
- 浏览器：Chrome / Edge 最新版（用于 PWA 与本地调试）

### 3.2 Python 依赖

依赖已在 requirements.txt 中声明：

- fastapi==0.115.0
- uvicorn[standard]==0.30.6
- sqlalchemy==2.0.36
- pymysql==1.1.1
- pydantic-settings==2.6.1
- httpx==0.27.2
- segno==1.6.1
- python-multipart==0.0.12
- pytest==8.3.3

### 3.3 环境配置

项目根目录需要 `.env` 文件，可由模板复制：

```bash
cp .env.example .env
```

将 `DATABASE_URL` 中的用户名、密码、主机和数据库名替换为实际配置：

```dotenv
DATABASE_URL=mysql+pymysql://elder_helper:your-password@127.0.0.1:3306/elder_helper?charset=utf8mb4
```

后端只接受 MySQL，`mysql://` 会自动规范为 `mysql+pymysql://`；SQLite 或其他数据库 URL 会在启动时被拒绝。

其余配置项包括：

- APP_NAME
- ENVIRONMENT
- DATABASE_URL
- TOKEN_SECRET
- WECHAT_WEBHOOK_URL
- SMS_PROVIDER
- PILOT_CITY
- GUIDE_SCOPE

短信与企业微信默认可使用 mock。不要提交包含真实密码的 `.env`。

## 4. 初始化 MySQL

### 4.1 创建空数据库和账号

使用管理员账号进入 MySQL 后执行：

```sql
CREATE DATABASE elder_helper CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'elder_helper'@'localhost' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON elder_helper.* TO 'elder_helper'@'localhost';
FLUSH PRIVILEGES;
```

应用首次启动时会通过 SQLAlchemy 创建缺失表。`create_all` 不会升级已有表结构，后续结构变更应使用 Alembic 迁移。

### 4.2 导入已有结构和历史数据

仓库中的 `elder_helper_mysql.sql` 包含建库、表结构和历史数据，也包含 `DROP TABLE`。仅在允许覆盖目标库现有表时执行：

```bash
mysql -u root -p < elder_helper_mysql.sql
```

## 5. 本地启动

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env，填写真实的 MySQL 凭据
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- 业务主页：<http://127.0.0.1:8000>
- API 文档：<http://127.0.0.1:8000/docs>

## 6. 验证

回归测试必须使用独立 MySQL 数据库，且数据库名必须以 `_test` 结尾。测试会在开始和结束时删除并重建其中的业务表，禁止指向开发库或生产库。

```sql
CREATE DATABASE elder_helper_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON elder_helper_test.* TO 'elder_helper'@'localhost';
```

```bash
TEST_DATABASE_URL='mysql+pymysql://elder_helper:your-password@127.0.0.1:3306/elder_helper_test?charset=utf8mb4' \
 python -m pytest -q
```

运行 HTTP 级冒烟脚本前，需先启动服务：

```bash
python scripts/smoke_test.py
```

## 7. 常见问题

### MySQL 连接失败

- 确认 MySQL 服务已启动且监听 `DATABASE_URL` 中的主机和端口。
- 确认用户已获得目标数据库权限。
- 密码中的 `@`、`:`、`/` 等特殊字符需要进行 URL 编码。
- 确认 URL 带有 `charset=utf8mb4`。

### 8000 端口占用

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

### 前端改了但页面没变化

- 由于启用了 Service Worker 缓存，建议先 Ctrl+F5 强刷。
- 若仍无变化，可在浏览器 DevTools 中清理站点缓存后重开。

## 8. 当前试点约束

- 试点城市固定重庆
- 求助通知为双通道（短信 + 企业微信）
- 讲解能力为知识有限范围
- 先做数字回忆卡，不含线下兑换
