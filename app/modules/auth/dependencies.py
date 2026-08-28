from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.modules.auth.entity.ElderEntity import ElderEntity
from app.modules.auth.entity.UserEntity import UserEntity
from app.modules.auth.service.AuthService import AuthService
from app.modules.auth.utils.jwt_handler import decode_access_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserEntity:
    """获取当前子女用户（需要JWT认证）"""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    user_type = payload.get("type")
    user_id = payload.get("sub")
    
    if user_type != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要子女用户权限"
        )
    
    user = AuthService.get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return user


def get_current_elder(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> ElderEntity:
    """获取当前老人用户（需要JWT认证）"""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    user_type = payload.get("type")
    elder_id = payload.get("sub")
    
    if user_type != "elder":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要老人用户权限"
        )
    
    elder = AuthService.get_elder_by_id(db, int(elder_id))
    if not elder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return elder


def get_current_user_or_elder(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> tuple[Optional[UserEntity], Optional[ElderEntity], str]:
    """获取当前用户（子女或老人）"""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    user_type = payload.get("type")
    user_id = payload.get("sub")
    
    if user_type == "user":
        user = AuthService.get_user_by_id(db, int(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        return user, None, "user"
    elif user_type == "elder":
        elder = AuthService.get_elder_by_id(db, int(user_id))
        if not elder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        return None, elder, "elder"
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的用户类型"
        )
