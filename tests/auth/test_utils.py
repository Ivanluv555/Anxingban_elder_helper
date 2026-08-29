"""
Auth 模块测试 - 密码工具单元测试
"""
from app.modules.auth.utils.password import (
    hash_password, 
    verify_password, 
    validate_password_complexity
)


class TestPasswordUtils:
    """密码工具函数测试"""
    
    def test_hash_password(self):
        """测试密码哈希"""
        password = "Test1234!@#"
        hashed = hash_password(password)
        assert hashed is not None
        assert len(hashed) > 50
        assert hashed.startswith("$argon2")
    
    def test_verify_password_success(self):
        """测试密码验证成功"""
        password = "Test1234!@#"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_password_fail(self):
        """测试密码验证失败"""
        password = "Test1234!@#"
        hashed = hash_password(password)
        assert verify_password("WrongPassword", hashed) is False
    
    def test_validate_password_complexity_success(self):
        """测试密码复杂度验证通过"""
        valid, msg = validate_password_complexity("Test1234!@#")
        assert valid is True
    
    def test_validate_password_too_short(self):
        """测试密码过短"""
        valid, msg = validate_password_complexity("Test1!")
        assert valid is False
        assert "8" in msg or "至少" in msg
    
    def test_validate_password_no_uppercase(self):
        """测试缺少大写字母"""
        valid, msg = validate_password_complexity("test1234!@#")
        assert valid is False
        assert "大写字母" in msg
    
    def test_validate_password_no_lowercase(self):
        """测试缺少小写字母"""
        valid, msg = validate_password_complexity("TEST1234!@#")
        assert valid is False
        assert "小写字母" in msg
    
    def test_validate_password_no_digit(self):
        """测试缺少数字"""
        valid, msg = validate_password_complexity("TestTest!@#")
        assert valid is False
        assert "数字" in msg
    
    def test_validate_password_no_special(self):
        """测试缺少特殊字符"""
        valid, msg = validate_password_complexity("Test12345678")
        assert valid is False
        assert "特殊字符" in msg
