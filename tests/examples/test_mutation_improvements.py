"""
变异测试改进示例
展示如何编写测试来捕获常见的存活变异
"""
import pytest
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


# ============= 示例1: 测试Pydantic字段验证 =============

def test_login_request_phone_required():
    """测试手机号必填 - 捕获nullable相关变异"""
    from app.modules.auth.dto.AuthDto import LoginRequest
    
    with pytest.raises(ValidationError) as exc_info:
        LoginRequest(phone=None, password="test123")
    
    errors = exc_info.value.errors()
    assert any(e['loc'] == ('phone',) for e in errors)


def test_login_request_password_required():
    """测试密码必填 - 捕获nullable相关变异"""
    from app.modules.auth.dto.AuthDto import LoginRequest
    
    with pytest.raises(ValidationError) as exc_info:
        LoginRequest(phone="13800138000", password=None)
    
    errors = exc_info.value.errors()
    assert any(e['loc'] == ('password',) for e in errors)


# ============= 示例2: 测试静态方法调用 =============

def test_auth_service_register_user_as_static_method(db_session):
    """验证register_user可以作为静态方法调用 - 捕获@staticmethod移除的变异"""
    from app.modules.auth.service.AuthService import AuthService
    from app.modules.auth.dto.AuthDto import RegisterUserRequest
    
    request = RegisterUserRequest(
        nickname="TestUser",
        phone="13800138001",
        password="Test@1234"
    )
    
    # 直接通过类调用（不创建实例）
    user, token = AuthService.register_user(db_session, request)
    
    assert user is not None
    assert user.nickname == "TestUser"
    assert token is not None


# ============= 示例3: 测试数据库约束 =============

def test_user_phone_unique_constraint(db_session):
    """测试手机号唯一约束 - 捕获约束相关变异"""
    from app.modules.auth.entity.UserEntity import UserEntity
    from app.modules.auth.utils.password import hash_password
    
    # 创建第一个用户
    user1 = UserEntity(
        nickname="User1",
        phone="13800138002",
        password=hash_password("Test@1234")
    )
    db_session.add(user1)
    db_session.commit()
    
    # 尝试创建相同手机号的用户
    user2 = UserEntity(
        nickname="User2",
        phone="13800138002",  # 相同手机号
        password=hash_password("Test@5678")
    )
    db_session.add(user2)
    
    with pytest.raises(IntegrityError):
        db_session.commit()


# ============= 示例4: 测试边界条件 =============

def test_elder_name_not_empty(db_session):
    """测试老人姓名不能为空 - 捕获nullable/空字符串变异"""
    from app.modules.auth.entity.ElderEntity import ElderEntity
    
    with pytest.raises((IntegrityError, ValidationError)):
        elder = ElderEntity(
            name="",  # 空字符串
            gender="男",
            birth_date="1950-01-01",
            relationship="父亲"
        )
        db_session.add(elder)
        db_session.commit()


# ============= 示例5: 测试业务逻辑分支 =============

def test_auth_service_login_wrong_password(db_session):
    """测试错误密码登录 - 捕获错误处理分支的变异"""
    from app.modules.auth.service.AuthService import AuthService
    from app.modules.auth.dto.AuthDto import LoginRequest, RegisterUserRequest
    
    # 先注册用户
    register_req = RegisterUserRequest(
        nickname="TestUser",
        phone="13800138003",
        password="Test@1234"
    )
    AuthService.register_user(db_session, register_req)
    
    # 使用错误密码登录
    login_req = LoginRequest(
        phone="13800138003",
        password="WrongPassword"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        AuthService.login(db_session, login_req)
    
    assert exc_info.value.status_code == 401


def test_auth_service_login_user_not_found(db_session):
    """测试用户不存在 - 捕获错误处理分支的变异"""
    from app.modules.auth.service.AuthService import AuthService
    from app.modules.auth.dto.AuthDto import LoginRequest
    
    login_req = LoginRequest(
        phone="19999999999",  # 不存在的手机号
        password="Test@1234"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        AuthService.login(db_session, login_req)
    
    assert exc_info.value.status_code in [401, 404]


# ============= 示例6: 测试Repository查询逻辑 =============

def test_profile_repository_get_by_user_id_not_found(db_session):
    """测试查询不存在的用户 - 捕获查询逻辑变异"""
    from app.modules.profile.repository.ProfileRepository import ProfileRepository
    
    result = ProfileRepository.get_by_user_id(db_session, user_id=99999)
    
    assert result is None


def test_profile_repository_get_by_user_id_found(db_session):
    """测试查询存在的用户 - 确保正常路径正确"""
    from app.modules.auth.entity.UserEntity import UserEntity
    from app.modules.auth.utils.password import hash_password
    from app.modules.profile.repository.ProfileRepository import ProfileRepository
    
    # 创建用户
    user = UserEntity(
        nickname="TestUser",
        phone="13800138004",
        password=hash_password("Test@1234")
    )
    db_session.add(user)
    db_session.commit()
    
    # 查询用户
    result = ProfileRepository.get_by_user_id(db_session, user_id=user.id)
    
    assert result is not None
    assert result.id == user.id


# ============= 示例7: 测试数值边界 =============

@pytest.mark.parametrize("invalid_id", [0, -1, -999])
def test_service_invalid_id_values(db_session, invalid_id):
    """测试无效ID值 - 捕获边界条件变异"""
    from app.modules.profile.repository.ProfileRepository import ProfileRepository
    
    result = ProfileRepository.get_by_user_id(db_session, user_id=invalid_id)
    
    # 应该返回None或抛出异常
    assert result is None


# ============= 示例8: 测试Entity字段默认值 =============

def test_elder_entity_default_values(db_session):
    """测试实体默认值 - 捕获default参数变异"""
    from app.modules.auth.entity.ElderEntity import ElderEntity
    from datetime import datetime
    
    elder = ElderEntity(
        name="测试老人",
        gender="男",
        birth_date="1950-01-01",
        relationship="父亲"
    )
    db_session.add(elder)
    db_session.commit()
    
    # 验证created_at是否自动设置
    assert elder.created_at is not None
    assert isinstance(elder.created_at, datetime)
    
    # 验证updated_at是否自动设置
    assert elder.updated_at is not None
    assert isinstance(elder.updated_at, datetime)


# ============= 运行指南 =============
"""
这些测试示例展示了如何捕获常见的变异类型：

1. 字段验证变异（nullable, required）
2. 装饰器变异（@staticmethod）
3. 数据库约束变异（unique, nullable）
4. 边界条件变异（空值, 负数, 极大值）
5. 错误处理分支变异
6. 查询逻辑变异
7. 默认值变异

运行这些测试：
    pytest tests/examples/test_mutation_improvements.py -v

将这些模式应用到实际模块：
1. 在每个模块的测试中添加类似的测试
2. 重点关注业务逻辑关键路径
3. 确保错误分支都有测试覆盖
"""
