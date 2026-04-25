# 安伴行（重庆试点）

这是一个可本地直接运行的真实产品 MVP（非演示模型），核心目标是帮助子女与长辈在出行过程中实现协同建档、行程安全保障、代际互动和回忆沉淀。

## 1. 这个 App 是怎么工作的

系统由两部分组成：

- 后端：FastAPI + SQLAlchemy + SQLite
- 前端：静态 Web App（PWA），由浏览器访问并调用后端 API

核心业务链路如下：

1. 家庭协同建档
- 子女填写父母和自己的联系方式、健康信息、兴趣偏好。
- 数据写入 profiles 表。

2. 创建行程并生成动态通行码
- 基于 profile 创建 trip。
- 服务端按 profile_id + trip_id + 时间戳 + 随机 nonce 生成 HMAC token。
- token 同步生成 SVG 二维码，返回给前端展示与复制。

3. 紧急求助（双通道）
- 前端触发 SOS 后调用 /api/sos/trigger。
- 服务端并行走短信与企业微信 webhook 两个通道（默认可 mock）。
- 同时记录 SOS 轨迹、网络状态、健康快照、通知状态。
- 前端离线时会先入本地队列，网络恢复后自动补发。

4. 代际挑战任务
- 子女创建任务（如拍照、打卡）。
- 长辈完成后可标记完成，子女发送反馈，累计爱心值。

5. 安伴行讲解（知识有限）
- 目前为重庆核心景点的受限问答。
- 返回 answer + confidence + scope（knowledge_limited）。

6. 生成数字回忆卡
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

## 3. 必要 Requirement

### 3.1 运行环境 Requirement

- 操作系统：Windows（你当前环境）
- Python：3.10.x（建议与当前 conda 环境一致）
- 包管理：pip（或 conda + pip）
- 浏览器：Chrome / Edge 最新版（用于 PWA 与本地调试）

### 3.2 Python 依赖 Requirement

依赖已在 requirements.txt 中声明：

- fastapi==0.115.0
- uvicorn[standard]==0.30.6
- sqlalchemy==2.0.36
- pydantic-settings==2.6.1
- httpx==0.27.2
- segno==1.6.1
- python-multipart==0.0.12
- pytest==8.3.3

### 3.3 配置 Requirement（.env）

项目根目录需要 .env 文件（可由 .env.example 复制）：

- APP_NAME
- ENVIRONMENT
- DATABASE_URL
- TOKEN_SECRET
- WECHAT_WEBHOOK_URL
- SMS_PROVIDER
- PILOT_CITY
- GUIDE_SCOPE

默认配置可直接本地运行，短信与企业微信可使用 mock。

## 4. 在你电脑本地启动运行（Windows + conda）

以下命令可直接在 PowerShell 执行。

1. 进入项目目录

```powershell
Set-Location D:\Code\Anbanxing_elder_helper
```

2. 激活 conda 环境（你当前用的是 my_pytorch）

```powershell
C:\Users\LoveS\anaconda3\Scripts\activate
conda activate my_pytorch
```

3. 安装依赖

```powershell
pip install -r requirements.txt
```

4. 准备环境变量

```powershell
Copy-Item .env.example .env -Force
```

5. 启动服务

```powershell
C:/Users/LoveS/anaconda3/envs/my_pytorch/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

6. 打开页面

- 业务主页：http://127.0.0.1:8000
- API 文档：http://127.0.0.1:8000/docs

## 5. 常用验证命令

1. 运行回归测试

```powershell
C:/Users/LoveS/anaconda3/envs/my_pytorch/python.exe -m pytest -q
```

2. 运行端到端冒烟脚本（需服务已启动）

```powershell
C:/Users/LoveS/anaconda3/envs/my_pytorch/python.exe scripts/smoke_test.py
```

## 6. 常见问题

1. 8000 端口占用，服务启动失败

```powershell
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess, LocalAddress, LocalPort, State
Stop-Process -Id <PID> -Force
```

或改端口启动：

```powershell
C:/Users/LoveS/anaconda3/envs/my_pytorch/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

2. 前端改了但页面没变化

- 由于启用了 Service Worker 缓存，建议先 Ctrl+F5 强刷。
- 若仍无变化，可在浏览器 DevTools 中清理站点缓存后重开。

## 7. 当前试点约束

- 试点城市固定重庆
- 求助通知为双通道（短信 + 企业微信）
- 讲解能力为知识有限范围
- 先做数字回忆卡，不含线下兑换
