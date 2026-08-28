import re
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Argon2 是现代推荐的密码哈希算法，无长度限制，更安全
ph = PasswordHasher()


def hash_password(password: str) -> str:
    """生成密码哈希值"""
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False


def validate_password_complexity(password: str) -> tuple[bool, str]:
    """
    验证密码复杂度
    要求：
    - 至少8个字符
    - 包含至少一个大写字母
    - 包含至少一个小写字母
    - 包含至少一个数字
    - 包含至少一个特殊字符
    """
    if len(password) < 8:
        return False, "密码长度至少为8个字符"
    
    if not re.search(r"[A-Z]", password):
        return False, "密码必须包含至少一个大写字母"
    
    if not re.search(r"[a-z]", password):
        return False, "密码必须包含至少一个小写字母"
    
    if not re.search(r"\d", password):
        return False, "密码必须包含至少一个数字"
    
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        return False, "密码必须包含至少一个特殊字符"
    
    return True, "密码符合复杂度要求"
