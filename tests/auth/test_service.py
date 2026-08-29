"""
Auth 模块测试 - Service 层单元测试
"""
import pytest
from app.modules.auth.service.AuthService import AuthService
from app.modules.auth.dto.AuthDto import RegisterUserRequest, RegisterElderRequest
from app.utils.error_codes import BusinessException


class TestAuthServiceUser:
    """用户认证服务测试"""
    
    def test_register_user_success(self, db_session):
        """测试用户注册成功"""
        request = RegisterUserRequest(
            nickname="TestUser",
            phone="13800138000",
            password="Test1234!@#"
        )
        
        user, token = AuthService.register_user(db_session, request)
        
        assert user is not None
        assert user.nickname == "TestUser"
        assert user.phone == "13800138000"
        assert token is not None
    
    def test_register_user_duplicate_phone(self, db_session):
        """测试重复手机号注册"""
        request = RegisterUserRequest(
            nickname="User1",
            phone="13800138000",
            password="Test1234!@#"
        )
        AuthService.register_user(db_session, request)
        
        with pytest.raises(BusinessException) as exc_info:
            AuthService.register_user(db_session, request)
        assert exc_info.value.error_code == "CONFLICT"
    
    def test_register_user_weak_password(self, db_session):
        """测试弱密码注册"""
        request = RegisterUserRequest(
            nickname="TestUser",
            phone="13800138000",
            password="123456"
        )
        
        with pytest.raises(BusinessException):
            AuthService.register_user(db_session, request)
    
    def test_login_user_success(self, db_session):
        """测试用户登录成功"""
        request = RegisterUserRequest(
            nickname="TestUser",
            phone="13800138000",
            password="Test1234!@#"
        )
        AuthService.register_user(db_session, request)
        
        user, token = AuthService.login_user(db_session, "13800138000", "Test1234!@#")
        
        assert user is not None
        assert user.phone == "13800138000"
        assert token is not None
    
    def test_login_user_wrong_password(self, db_session):
        """测试错误密码登录"""
        request = RegisterUserRequest(
            nickname="TestUser",
            phone="13800138000",
            password="Test1234!@#"
        )
        AuthService.register_user(db_session, request)
        
        with pytest.raises(BusinessException) as exc_info:
            AuthService.login_user(db_session, "13800138000", "WrongPassword")
        assert "密码错误" in str(exc_info.value.detail)
    
    def test_login_user_not_found(self, db_session):
        """测试用户不存在"""
        with pytest.raises(BusinessException):
            AuthService.login_user(db_session, "99999999999", "Test1234!@#")


class TestAuthServiceElder:
    """老人认证服务测试"""
    
    def test_register_elder_success(self, db_session):
        """测试老人注册成功"""
        request = RegisterElderRequest(
            name="TestElder",
            phone="13900139000",
            password="Elder1234!@#",
            health_info='{"chronic_diseases": "none"}',
            interests="culture,food"
        )
        
        elder, token = AuthService.register_elder(db_session, request)
        
        assert elder is not None
        assert elder.name == "TestElder"
        assert elder.phone == "13900139000"
        assert token is not None
    
    def test_register_elder_with_empty_webhook(self, db_session):
        """测试 webhook_url 为 None 时的 or 分支"""
        request = RegisterElderRequest(
            name="TestElder",
            phone="13900139000",
            password="Elder1234!@#",
            health_info='{"chronic_diseases": "none"}',
            interests="culture,food",
            wechat_webhook_url=None
        )
        
        elder, token = AuthService.register_elder(db_session, request)
        
        assert elder.wechat_webhook_url == ""
    
    def test_register_elder_duplicate_phone(self, db_session):
        """测试老人重复手机号注册"""
        request = RegisterElderRequest(
            name="Elder1",
            phone="13900139000",
            password="Elder1234!@#",
            health_info='{}',
            interests="culture"
        )
        AuthService.register_elder(db_session, request)
        
        with pytest.raises(BusinessException):
            AuthService.register_elder(db_session, request)
    
    def test_login_elder_success(self, db_session):
        """测试老人登录成功"""
        request = RegisterElderRequest(
            name="TestElder",
            phone="13900139000",
            password="Elder1234!@#",
            health_info='{}',
            interests="culture"
        )
        AuthService.register_elder(db_session, request)
        
        elder, token = AuthService.login_elder(db_session, "13900139000", "Elder1234!@#")
        
        assert elder is not None
        assert token is not None
    
    def test_login_elder_wrong_password(self, db_session):
        """测试老人错误密码登录"""
        request = RegisterElderRequest(
            name="TestElder",
            phone="13900139000",
            password="Elder1234!@#",
            health_info='{}',
            interests="culture"
        )
        AuthService.register_elder(db_session, request)
        
        with pytest.raises(BusinessException):
            AuthService.login_elder(db_session, "13900139000", "WrongPassword")
