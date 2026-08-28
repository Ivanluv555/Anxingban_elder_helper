from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.utils.error_codes import BusinessException, ErrorCode
from app.modules.auth.dto.AuthDto import RegisterElderRequest, RegisterUserRequest
from app.modules.auth.entity.ElderEntity import ElderEntity
from app.modules.auth.entity.UserEntity import UserEntity
from app.modules.auth.repository.AuthRepository import UserRepository, ElderRepository
from app.modules.auth.utils.jwt_handler import create_access_token
from app.modules.auth.utils.password import hash_password, validate_password_complexity, verify_password


class AuthService:
    @staticmethod
    def register_user(db: Session, request: RegisterUserRequest) -> tuple[UserEntity, str]:
        """注册子女用户"""
        is_valid, message = validate_password_complexity(request.password)
        if not is_valid:
            raise BusinessException(ErrorCode.VALIDATION_ERROR, detail=message)
        
        repo = UserRepository(db)
        existing_user = repo.find_by_phone(request.phone)
        if existing_user:
            raise BusinessException(ErrorCode.CONFLICT, detail="该手机号已注册")
        
        user = UserEntity(
            nickname=request.nickname,
            phone=request.phone,
            password_hash=hash_password(request.password)
        )
        user = repo.create(user)
        
        token = create_access_token({"sub": str(user.id), "type": "user"})
        return user, token

    @staticmethod
    def register_elder(db: Session, request: RegisterElderRequest) -> tuple[ElderEntity, str]:
        """注册老人用户"""
        is_valid, message = validate_password_complexity(request.password)
        if not is_valid:
            raise BusinessException(ErrorCode.VALIDATION_ERROR, detail=message)
        
        repo = ElderRepository(db)
        existing_elder = repo.find_by_phone(request.phone)
        if existing_elder:
            raise BusinessException(ErrorCode.CONFLICT, detail="该手机号已注册")
        
        elder = ElderEntity(
            name=request.name,
            phone=request.phone,
            password_hash=hash_password(request.password),
            health_info=request.health_info,
            interests=request.interests,
            wechat_webhook_url=request.wechat_webhook_url or ""
        )
        elder = repo.create(elder)
        
        token = create_access_token({"sub": str(elder.id), "type": "elder"})
        return elder, token

    @staticmethod
    def login_user(db: Session, phone: str, password: str) -> tuple[UserEntity, str]:
        """子女用户登录"""
        repo = UserRepository(db)
        user = repo.find_by_phone(phone)
        if not user or not verify_password(password, user.password_hash):
            raise BusinessException(ErrorCode.UNAUTHORIZED, detail="手机号或密码错误")
        
        user.last_login_at = datetime.utcnow()
        user = repo.update(user)
        
        token = create_access_token({"sub": str(user.id), "type": "user"})
        return user, token

    @staticmethod
    def login_elder(db: Session, phone: str, password: str) -> tuple[ElderEntity, str]:
        """老人用户登录"""
        repo = ElderRepository(db)
        elder = repo.find_by_phone(phone)
        if not elder or not verify_password(password, elder.password_hash):
            raise BusinessException(ErrorCode.UNAUTHORIZED, detail="手机号或密码错误")
        
        elder.last_login_at = datetime.utcnow()
        elder = repo.update(elder)
        
        token = create_access_token({"sub": str(elder.id), "type": "elder"})
        return elder, token

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[UserEntity]:
        """根据ID获取子女用户"""
        repo = UserRepository(db)
        return repo.find_by_id(user_id)

    @staticmethod
    def get_elder_by_id(db: Session, elder_id: int) -> Optional[ElderEntity]:
        """根据ID获取老人用户"""
        repo = ElderRepository(db)
        return repo.find_by_id(elder_id)
        return db.get(ElderEntity, elder_id)
