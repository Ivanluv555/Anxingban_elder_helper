# API对照检查报告

**日期**: 2026-08-25  
**检查范围**: 移动端 vs 后端API

---

## ✅ 已匹配的API

| 模块 | 方法 | 路径 | 状态 |
| ------ | ------ | ------ | ------ |
| Profile | POST | /api/profiles | ✅ 完全匹配 |
| Profile | GET | /api/profiles | ✅ 完全匹配 |
| Profile | GET | /api/profiles/{id} | ✅ 完全匹配 |
| Trip | POST | /api/trips | ✅ 完全匹配 |
| Trip | GET | /api/trips/{id} | ✅ 完全匹配 |
| Trip | GET | /api/trips/{id}/pass | ✅ 完全匹配 |
| Task | POST | /api/tasks | ✅ 完全匹配 |
| Task | POST | /api/tasks/{id}/complete | ✅ 完全匹配 |
| SOS | POST | /api/sos/trigger | ✅ 完全匹配 |
| Guide | POST | /api/guide/ask | ✅ 完全匹配 |
| Card | POST | /api/cards/generate | ✅ 完全匹配 |
| Card | GET | /api/cards/{id} | ✅ 完全匹配 |

---

## ⚠️ 不匹配的问题

### 1. HTTP方法不一致

| 接口 | 移动端 | 后端 | 影响 |
|------|--------|------|------|
| 更新档案 | PUT /profiles/{id} | PATCH /profiles/{id} | ⚠️ 可能工作但不规范 |

**修复建议**: 移动端改用PATCH或后端同时支持PUT

### 2. 后端缺少的接口（移动端需要但后端未实现）

#### 🔴 高优先级（功能闭环必需）

| 功能 | 移动端调用 | 后端状态 | 影响 |
| ------ | ------------ | ---------- | ------ |
| 获取行程列表 | GET /trips | ❌ 不存在 | 旅途页面无法显示列表 |
| 获取任务列表 | GET /tasks | ❌ 不存在 | 回忆页面无法显示任务 |
| 获取卡片列表 | GET /cards | ❌ 不存在 | 回忆页面无法显示卡片 |
| 删除行程 | DELETE /trips/{id} | ❌ 不存在 | 无法删除行程 |
| 删除卡片 | DELETE /cards/{id} | ❌ 不存在 | 无法删除卡片 |

#### 🟡 中优先级

| 功能 | 移动端调用 | 后端状态 | 影响 |
| ------ | ------------ | ---------- | ------ |
| 获取单个任务 | GET /tasks/{id} | ❌ 不存在 | 查看任务详情失败 |
| 删除任务 | DELETE /tasks/{id} | ❌ 不存在 | 无法删除任务 |
| 删除档案 | DELETE /profiles/{id} | ❌ 不存在 | 无法删除档案 |

### 3. 路径不匹配

| 功能 | 移动端 | 后端 | 问题 |
|------|--------|------|------|
| 获取SOS记录 | GET /sos | GET /sos/profile/{id} | ❌ 路径完全不同 |

**说明**:

- 移动端期望: `GET /api/sos?profileId=1`
- 后端实际: `GET /api/sos/profile/1`

---

## 📊 统计

- **完全匹配**: 12个接口 ✅
- **方法不一致**: 1个接口 ⚠️
- **后端缺失**: 8个接口 ❌
- **路径不匹配**: 1个接口 ❌

**总体匹配率**: 54.5% (12/22)

---

## 🔧 修复方案

### 方案A: 修复移动端（快速）

修改 `mobile/anxingban/lib/core/api/api_client.dart`:

```dart
// 1. 更新档案 - 改用PATCH
Future<Map<String, dynamic>> updateProfile(int id, Map<String, dynamic> data) async {
  return await _request('/profiles/$id', method: 'PATCH', body: data);
}

// 2. SOS记录 - 使用正确路径
Future<List<dynamic>> getSOSRecords({int? profileId}) async {
  final endpoint = profileId != null ? '/sos/profile/$profileId' : '/sos';
  final result = await _request(endpoint);
  return result is List ? result : [];
}

// 3. 暂时移除不存在的调用
// - 注释掉 getTrips, getTasks, getCards
// - 或者这些方法返回空列表
```

### 方案B: 增强后端（推荐）

需要添加以下接口：

#### 1. Trip Controller

```python
@router.get("", response_model=list[TripResponseDto])
def list_trips(profile_id: int = None, limit: int = 20, db: Session = Depends(get_db)):
    # 获取行程列表

@router.delete("/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    # 删除行程
```

#### 2. Task Controller

```python
@router.get("", response_model=list[TaskResponseDto])
def list_tasks(profile_id: int = None, db: Session = Depends(get_db)):
    # 获取任务列表

@router.get("/{task_id}", response_model=TaskResponseDto)
def get_task(task_id: int, db: Session = Depends(get_db)):
    # 获取单个任务

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    # 删除任务
```

#### 3. Card Controller

```python
@router.get("", response_model=list[CardResponseDto])
def list_cards(profile_id: int = None, trip_id: int = None, db: Session = Depends(get_db)):
    # 获取卡片列表

@router.delete("/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db)):
    # 删除卡片
```

#### 4. SOS Controller

```python
@router.get("", response_model=list[SosResponseDto])
def list_sos(profile_id: int = None, db: Session = Depends(get_db)):
    # 获取SOS列表（兼容路径）
```

#### 5. Profile Controller

```python
@router.put("/{profile_id}", response_model=ProfileResponseDto)
def update_profile_put(profile_id: int, payload: ProfileUpdateDto, db: Session = Depends(get_db)):
    # 同时支持PUT方法
    return update_profile(profile_id, payload, db)

@router.delete("/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    # 删除档案
```

---

## 🎯 推荐行动

### 立即修复（方案A - 30分钟）

1. 修改移动端PATCH方法
2. 修改SOS路径
3. 临时禁用删除功能按钮

### 完整修复（方案B - 2小时）

1. 后端添加列表查询接口
2. 后端添加删除接口
3. 后端支持PUT方法
4. 测试所有接口

**建议**: 先执行方案A让应用可用，再逐步实施方案B完善功能。

---

**检查完成** ✅
