"""
Auth 依赖注入测试 - dependencies 单元测试
"""
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from app.modules.auth.dependencies import (
    get_current_user,
    get_current_elder,
    get_current_user_or_elder
)
from app.modules.auth.service.AuthService import AuthService
from app.modules.auth.dto.AuthDto import RegisterUserRequest, RegisterElderRequest


class TestGetCurrentUser:
    """测试 get_current_user 依赖"""
    
    def test_get_current_user_success(self, db_session):
        """测试获取当前用户成功"""
        request = RegisterUserRequest(
            nickname="TestUser",
            phone="13800138000",
            password="Test1234!@#"
        )
        user, token = AuthService.register_user(db_session, request)
        
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        current_user = get_current_user(credentials, db_session)
        
        assert current_user is not None
        assert current_user.id == user.id
        assert current_user.phone == "13800138000"
    
    def test_get_current_user_with_elder_token(self, db_session):
        """测试使用老人 token 访问用户接口（权限错误）"""
        request = RegisterElderRequest(
            name="TestElder",
            phone="13900139000",
            password="Elder1234!@#",
            health_info='{}',
            interests="culture"
        )
        elder, token = AuthService.register_elder(db_session, request)
        
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials, db_session)
        assert exc_info.value.status_code == 403
    
    def test_get_current_user_not_exists(self, db_session):
        """测试用户不存在的情况"""
        from app.modules.auth.utils.jwt_handler import create_access_token
        
        # 创建一个不存在用户的 token
        token = create_access_token({"sub": "999999", "type": "user"})
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials, db_session)
        assert exc_info.value.status_code == 404
        assert "不存在" in exc_info.value.detail


class TestGetCurrentElder:
    """测试 get_current_elder 依赖"""
    
    def test_get_current_elder_success(self, db_session):
        """测试获取当前老人成功"""
        request = RegisterElderRequest(
            name="TestElder",
            phone="13900139000",
            password="Elder1234!@#",
            health_info='{}',
            interests="culture"
        )
        elder, token = AuthService.register_elder(db_session, request)
        
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        current_elder = get_current_elder(credentials, db_session)
        
        assert current_elder is not None
        assert current_elder.id == elder.id
        assert current_elder.phone == "13900139000"
    
    def test_get_current_elder_with_user_token(self, db_session):
        """测试使用用户 token 访问老人接口（权限错误）"""
        request = RegisterUserRequest(
            nickname="TestUser",
            phone="13800138000",
            password="Test1234!@#"
        )
        user, token = AuthService.register_user(db_session, request)
        
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_elder(credentials, db_session)
        assert exc_info.value.status_code == 403
    
    def test_get_current_elder_not_exists(self, db_session):
        """测试老人不存在的情况"""
        from app.modules.auth.utils.jwt_handler import create_access_token
        
        token = create_access_token({"sub": "999999", "type": "elder"})
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_elder(credentials, db_session)
        assert exc_info.value.status_code == 404
        assert "不存在" in exc_info.value.detail


class TestGetCurrentUserOrElder:
    """测试 get_current_user_or_elder 依赖"""
    
    def test_get_user_success(self, db_session):
        """测试获取用户成功"""
        request = RegisterUserRequest(
            nickname="TestUser",
            phone="13800138000",
            password="Test1234!@#"
        )
        user, token = AuthService.register_user(db_session, request)
        
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        result_user, result_elder, user_type = get_current_user_or_elder(credentials, db_session)
        
        assert result_user is not None
        assert result_elder is None
        assert user_type == "user"
        assert result_user.id == user.id
    
    def test_get_elder_success(self, db_session):
        """测试获取老人成功"""
        request = RegisterElderRequest(
            name="TestElder",
            phone="13900139000",
            password="Elder1234!@#",
            health_info='{}',
            interests="culture"
        )
        elder, token = AuthService.register_elder(db_session, request)
        
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        result_user, result_elder, user_type = get_current_user_or_elder(credentials, db_session)
        
        assert result_user is None
        assert result_elder is not None
        assert user_type == "elder"
        assert result_elder.id == elder.id
    
    def test_get_user_not_exists(self, db_session):
        """测试用户不存在"""
        from app.modules.auth.utils.jwt_handler import create_access_token
        
        token = create_access_token({"sub": "999999", "type": "user"})
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user_or_elder(credentials, db_session)
        assert exc_info.value.status_code == 404
    
    def test_get_elder_not_exists(self, db_session):
        """测试老人不存在"""
        from app.modules.auth.utils.jwt_handler import create_access_token
        
        token = create_access_token({"sub": "999999", "type": "elder"})
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user_or_elder(credentials, db_session)
        assert exc_info.value.status_code == 404
    
    def test_invalid_user_type(self, db_session):
        """测试无效的用户类型"""
        from app.modules.auth.utils.jwt_handler import create_access_token
        
        token = create_access_token({"sub": "1", "type": "invalid"})
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user_or_elder(credentials, db_session)
        assert exc_info.value.status_code == 401
        assert "无效" in exc_info.value.detail
