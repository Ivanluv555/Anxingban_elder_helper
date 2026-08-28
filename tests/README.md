# 测试框架文档

## 概述

本项目使用 pytest 作为测试框架，提供完整的单元测试和集成测试覆盖。

## 测试结构

```
tests/
├── conftest.py           # 测试配置和 fixtures
├── test_auth.py          # 认证模块测试
├── test_profile.py       # 档案模块测试
├── test_trip.py          # 行程模块测试
├── test_task.py          # 任务模块测试
├── test_integration.py   # 集成测试
└── test_*.py            # 其他模块测试
```

## 环境准备

### 1. 安装测试依赖

```bash
pip install pytest pytest-asyncio pytest-cov faker httpx
```

### 2. 配置测试数据库

创建测试数据库（必须以 `_test` 结尾）：

```sql
CREATE DATABASE anxingban_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

设置环境变量：

```bash
export TEST_DATABASE_URL="mysql+pymysql://root:password@localhost:3306/anxingban_test"
```

或在 `.env` 文件中添加：

```
TEST_DATABASE_URL=mysql+pymysql://root:password@localhost:3306/anxingban_test
```

## 运行测试

### 运行所有测试

```bash
pytest
# 或
python run_tests.py
```

### 运行特定模块

```bash
pytest tests/test_auth.py
pytest tests/test_profile.py
```

### 运行特定测试类

```bash
pytest tests/test_auth.py::TestPasswordUtils
```

### 运行特定测试函数

```bash
pytest tests/test_auth.py::TestPasswordUtils::test_hash_password
```

### 只运行单元测试

```bash
pytest -m unit
```

### 只运行集成测试

```bash
pytest -m integration
```

### 生成覆盖率报告

```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
# 报告位于: htmlcov/index.html
```

### 详细输出

```bash
pytest -v      # 详细输出
pytest -vv     # 更详细输出
pytest -s      # 显示 print 输出
```

## 测试 Fixtures

### 基础 Fixtures

- `db_session`: 提供数据库会话（事务回滚）
- `client`: FastAPI 测试客户端
- `clean_db`: 清空所有表数据

### 数据 Fixtures

- `test_user_data`: 测试用户数据
- `test_elder_data`: 测试老人数据
- `create_test_user`: 创建测试用户并返回认证信息
- `create_test_elder`: 创建测试老人并返回认证信息
- `create_test_profile`: 创建测试档案
- `create_test_trip`: 创建测试行程
- `create_test_task`: 创建测试任务

## 测试示例

### 单元测试示例

```python
def test_password_validation(db_session):
    """测试密码验证"""
    from app.modules.auth.utils.password import validate_password_complexity
    
    valid, msg = validate_password_complexity("Test1234!@#")
    assert valid is True
```

### API 集成测试示例

```python
def test_create_profile(client, create_test_user, create_test_elder):
    """测试创建档案 API"""
    response = client.post(
        "/api/user/profiles",
        json={"elder_id": create_test_elder["elder_id"]},
        headers=create_test_user["headers"]
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["elder_id"] == create_test_elder["elder_id"]
```

### Service 单元测试示例

```python
def test_profile_service(db_session):
    """测试 ProfileService"""
    from app.modules.profile.service.ProfileService import ProfileService
    
    profile = ProfileService.create_profile(db_session, elder_id=1, user_id=1)
    
    assert profile is not None
    assert profile.elder_id == 1
```

## 测试覆盖范围

### Auth 模块
- ✅ 密码哈希和验证
- ✅ 密码复杂度验证
- ✅ 用户注册（成功/失败）
- ✅ 用户登录（成功/失败）
- ✅ 老人注册和登录
- ✅ JWT token 生成

### Profile 模块
- ✅ 创建档案
- ✅ 查询档案列表
- ✅ 删除档案
- ✅ 权限验证

### Trip 模块
- ✅ 创建行程
- ✅ 生成通行码和二维码
- ✅ 列表查询（不含二维码）
- ✅ 详情查询（含二维码）
- ✅ 删除行程

### Task 模块
- ✅ 创建任务
- ✅ 子女完成任务
- ✅ 老人完成任务
- ✅ 双方完成状态
- ✅ 列表/详情返回字段区分

### 集成测试
- ✅ 完整业务流程
- ✅ 权限控制
- ✅ 数据隔离

## 最佳实践

1. **测试隔离**: 每个测试独立，使用事务回滚确保数据不污染
2. **明确断言**: 使用具体的断言，避免模糊验证
3. **测试命名**: 使用描述性名称，说明测试目的
4. **Fixtures 复用**: 使用 fixtures 减少重复代码
5. **错误测试**: 不仅测试成功路径，也测试错误处理

## CI/CD 集成

在 CI 管道中运行测试：

```yaml
# .github/workflows/test.yml
- name: Run tests
  env:
    TEST_DATABASE_URL: mysql+pymysql://root:root@localhost:3306/test_db
  run: |
    pytest --cov=app --cov-report=xml
```

## 故障排查

### 测试数据库连接失败
- 检查 `TEST_DATABASE_URL` 环境变量
- 确认数据库存在且名称以 `_test` 结尾
- 检查数据库用户权限

### Fixture 未找到
- 确保 `conftest.py` 在 `tests/` 目录中
- 检查 fixture 名称拼写

### 导入错误
- 确保项目根目录在 Python 路径中
- 运行 `pytest` 时在项目根目录

## 持续改进

- 定期更新测试用例
- 提高测试覆盖率（目标 >80%）
- 添加性能测试
- 添加压力测试
