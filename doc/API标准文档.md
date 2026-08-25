# 安行伴后端 API 文档

**基础地址**: `http://localhost:8000` (开发) / `http://47.237.188.77:8000` (生产)  
**接口总数**: 18 个  
**版本**: v1.0  
**最后更新**: 2026-08-25

---

## 📖 快速开始

### 接口调用示例

```javascript
// 创建档案
const response = await fetch('http://localhost:8000/api/profiles', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    parent_name: '张三',
    parent_phone: '13800000000',
    child_name: '张小明',
    child_phone: '13900000000',
    chronic_diseases: '高血压',
    allergies: '无',
    mobility_limitations: '轻度',
    interests: '文化,美食,历史'
  })
});
const data = await response.json();
```

---

## 📚 接口列表

### 1. 档案管理 `/api/profiles`

#### 1.1 获取档案列表

```
GET /api/profiles?limit=20
```

**查询参数**:

- `limit` (int, 可选): 返回数量，默认 20，最大 100

**响应示例**:

```json
[
  {
    "id": 1,
    "parent_name": "张三",
    "parent_phone": "13800000000",
    "child_name": "张小明",
    "child_phone": "13900000000",
    "health_info": "{\"chronic_diseases\":\"高血压\"}",
    "interests": "文化,美食",
    "created_at": "2026-08-25T10:00:00"
  }
]
```

#### 1.2 创建家庭档案

```
POST /api/profiles
```

**请求体**:

```json
{
  "parent_name": "张三",
  "parent_phone": "13800000000",
  "child_name": "张小明",
  "child_phone": "13900000000",
  "chronic_diseases": "高血压",
  "allergies": "无",
  "mobility_limitations": "轻度",
  "interests": "文化,美食,历史",
  "wechat_webhook_url": ""
}
```

**响应**: 返回创建的档案对象 (201)

#### 1.3 获取档案详情

```
GET /api/profiles/{profile_id}
```

**路径参数**:

- `profile_id` (int): 档案 ID

**错误**: 404 - 档案不存在

#### 1.4 更新档案信息

```
PATCH /api/profiles/{profile_id}
```

**请求体** (部分更新):

```json
{
  "parent_phone": "13800000001",
  "interests": "文化,美食,历史,艺术"
}
```

**错误**: 404 - 档案不存在

---

### 2. 行程管理 `/api/trips`

#### 2.1 创建行程

```
POST /api/trips
```

**请求体**:

```json
{
  "profile_id": 1,
  "destination": "洪崖洞",
  "travel_date": "2026-08-26"
}
```

**响应**:

```json
{
  "id": 1,
  "profile_id": 1,
  "destination": "洪崖洞",
  "travel_date": "2026-08-26",
  "pass_token": "ELDER-abc123...",
  "pass_qr_svg": "<svg>...</svg>",
  "status": "created",
  "created_at": "2026-08-25T10:00:00"
}
```

#### 2.2 获取行程详情

```
GET /api/trips/{trip_id}
```

**错误**: 404 - 行程不存在

#### 2.3 获取行程通行码

```
GET /api/trips/{trip_id}/pass
```

**响应**:

```json
{
  "pass_token": "ELDER-abc123...",
  "pass_qr_svg": "<svg>...</svg>",
  "destination": "洪崖洞",
  "travel_date": "2026-08-26"
}
```

#### 2.4 获取档案行程列表

```
GET /api/trips/profile/{profile_id}
```

---

### 3. 亲子任务 `/api/tasks`

#### 3.1 创建任务

```
POST /api/tasks
```

**请求体**:

```json
{
  "profile_id": 1,
  "trip_id": 1,
  "title": "拍一张江景照片",
  "description": "在江边拍照并上传"
}
```

#### 3.2 完成任务

```
POST /api/tasks/{task_id}/complete
```

**请求体**:

```json
{
  "completed_note": "已完成",
  "photo_url": "https://example.com/photo.jpg"
}
```

**错误**: 404 - 任务不存在

#### 3.3 任务反馈

```
POST /api/tasks/{task_id}/feedback
```

**请求体**:

```json
{
  "feedback_text": "拍得真好！",
  "hearts": 1
}
```

#### 3.4 获取档案任务列表

```
GET /api/tasks/profile/{profile_id}
```

---

### 4. 紧急求助 `/api/sos`

#### 4.1 触发紧急求助

```
POST /api/sos/trigger
```

**请求体**:

```json
{
  "profile_id": 1,
  "trip_id": 1,
  "latitude": 29.56,
  "longitude": 106.55,
  "network_status": "online"
}
```

**功能**:

- 自动发送短信给子女
- 发送企业微信通知（如已配置）

**响应**:

```json
{
  "id": 1,
  "profile_id": 1,
  "sms_status": "sent:mock",
  "wechat_status": "not_configured",
  "created_at": "2026-08-25T10:00:00"
}
```

#### 4.2 获取 SOS 历史

```
GET /api/sos/profile/{profile_id}
```

---

### 5. 回忆卡片 `/api/cards`

#### 5.1 生成回忆卡片

```
POST /api/cards/generate
```

**请求体**:

```json
{
  "trip_id": 1,
  "title": "洪崖洞之旅",
  "summary": "今天游览了美丽的洪崖洞...",
  "image_url": "https://example.com/photo.jpg"
}
```

**错误**: 404 - 行程不存在

#### 5.2 获取卡片详情

```
GET /api/cards/{card_id}
```

**错误**: 404 - 卡片不存在

#### 5.3 获取行程卡片列表

```
GET /api/cards/trip/{trip_id}
```

---

### 6. 景点讲解 `/api/guide`

#### 6.1 景点智能问答

```
POST /api/guide/ask
```

**请求体**:

```json
{
  "question": "洪崖洞有什么历史故事？"
}
```

**响应**:

```json
{
  "answer": "洪崖洞是重庆著名的吊脚楼建筑群...",
  "confidence": 0.95
}
```

---

## 🔧 数据模型

### Profile（档案）

```typescript
interface Profile {
  id: number;
  parent_name: string;
  parent_phone: string;
  child_name: string;
  child_phone: string;
  health_info: string;       // JSON 字符串
  interests: string;         // 逗号分隔
  wechat_webhook_url?: string;
  created_at: string;        // ISO 8601
}
```

### Trip（行程）

```typescript
interface Trip {
  id: number;
  profile_id: number;
  destination: string;
  travel_date: string;       // YYYY-MM-DD
  pass_token: string;
  pass_qr_svg: string;       // SVG 字符串
  status: 'created' | 'completed';
  created_at: string;
}
```

### Task（任务）

```typescript
interface Task {
  id: number;
  profile_id: number;
  trip_id: number;
  title: string;
  description: string;
  status: 'pending' | 'completed';
  completed_note?: string;
  photo_url?: string;
  feedback_text?: string;
  hearts: number;
  created_at: string;
  completed_at?: string;
}
```

---

## ⚠️ 错误处理

所有接口统一错误响应格式：

```json
{
  "detail": "错误描述信息"
}
```

**常见错误码**:

- `404 Not Found` - 资源不存在
- `422 Unprocessable Entity` - 请求参数验证失败
- `500 Internal Server Error` - 服务器内部错误

**示例**:

```javascript
try {
  const response = await fetch('/api/profiles/999');
  if (!response.ok) {
    const error = await response.json();
    console.error('错误:', error.detail);  // "档案不存在"
  }
} catch (err) {
  console.error('网络错误:', err);
}
```

---

## 📋 典型业务流程

### 完整出游流程

```javascript
// 1. 创建档案
const profile = await fetch('/api/profiles', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({...})
}).then(r => r.json());

// 2. 创建行程
const trip = await fetch('/api/trips', {
  method: 'POST',
  body: JSON.stringify({
    profile_id: profile.id,
    destination: "洪崖洞",
    travel_date: "2026-08-26"
  })
}).then(r => r.json());

// 3. 创建任务
const task = await fetch('/api/tasks', {
  method: 'POST',
  body: JSON.stringify({
    profile_id: profile.id,
    trip_id: trip.id,
    title: "拍照打卡"
  })
}).then(r => r.json());

// 4. 完成任务
await fetch(`/api/tasks/${task.id}/complete`, {
  method: 'POST',
  body: JSON.stringify({
    completed_note: "已完成",
    photo_url: "https://..."
  })
});

// 5. 生成回忆卡片
await fetch('/api/cards/generate', {
  method: 'POST',
  body: JSON.stringify({
    trip_id: trip.id,
    title: "美好回忆",
    summary: "今天很开心..."
  })
});
```

---

## 📱 前端集成建议

### API 封装示例

```javascript
// api/client.js
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const config = {
    headers: { 'Content-Type': 'application/json' },
    ...options
  };
  
  const response = await fetch(url, config);
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || '请求失败');
  }
  
  return response.json();
}

export const api = {
  // 档案
  profiles: {
    list: (limit = 20) => request(`/api/profiles?limit=${limit}`),
    create: (data) => request('/api/profiles', { method: 'POST', body: JSON.stringify(data) }),
    get: (id) => request(`/api/profiles/${id}`),
    update: (id, data) => request(`/api/profiles/${id}`, { method: 'PATCH', body: JSON.stringify(data) })
  },
  
  // 行程
  trips: {
    create: (data) => request('/api/trips', { method: 'POST', body: JSON.stringify(data) }),
    get: (id) => request(`/api/trips/${id}`),
    getPass: (id) => request(`/api/trips/${id}/pass`),
    listByProfile: (profileId) => request(`/api/trips/profile/${profileId}`)
  },
  
  // SOS
  sos: {
    trigger: (data) => request('/api/sos/trigger', { method: 'POST', body: JSON.stringify(data) }),
    listByProfile: (profileId) => request(`/api/sos/profile/${profileId}`)
  }
};
```

### 使用示例

```javascript
import { api } from './api/client';

// 创建档案
try {
  const profile = await api.profiles.create({
    parent_name: '张三',
    parent_phone: '13800000000',
    child_name: '张小明',
    child_phone: '13900000000',
    chronic_diseases: '高血压',
    allergies: '无',
    mobility_limitations: '轻度',
    interests: '文化,美食'
  });
  console.log('档案创建成功:', profile);
} catch (err) {
  console.error('创建失败:', err.message);
}
```

---

## 🧪 在线测试

### Swagger UI

访问 `http://localhost:8000/docs` 可以：

- 查看完整接口文档
- 在线测试所有接口
- 查看请求/响应示例

### OpenAPI 定义

访问 `http://localhost:8000/openapi.json` 获取 OpenAPI 3.0 规范，可导入到：

- Postman
- Apifox
- Insomnia

---

## 🚀 环境配置

### 开发环境 (.env.development)

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 生产环境 (.env.production)

```env
VITE_API_BASE_URL=http://服务器IP:8000
```

---

**文档维护**: 后端团队  
**联系方式**: 通过 Swagger UI 查看详细文档
