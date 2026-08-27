"""
错误码定义模块
提供标准化的错误码和错误信息
"""
from enum import Enum
from typing import Dict, Optional


class ErrorCode(str, Enum):
    """错误码枚举"""
    
    # 成功 (200)
    SUCCESS = "SUCCESS"
    
    # 客户端错误 (400-499)
    BAD_REQUEST = "BAD_REQUEST"                      # 400 - 请求参数错误
    UNAUTHORIZED = "UNAUTHORIZED"                     # 401 - 未授权
    FORBIDDEN = "FORBIDDEN"                           # 403 - 禁止访问
    NOT_FOUND = "NOT_FOUND"                          # 404 - 资源不存在
    METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED"        # 405 - 方法不允许
    CONFLICT = "CONFLICT"                             # 409 - 资源冲突
    VALIDATION_ERROR = "VALIDATION_ERROR"             # 422 - 验证失败
    
    # 业务错误 (1000-1999)
    PROFILE_NOT_FOUND = "PROFILE_NOT_FOUND"          # 1001 - 档案不存在
    PROFILE_ALREADY_EXISTS = "PROFILE_ALREADY_EXISTS" # 1002 - 档案已存在
    TRIP_NOT_FOUND = "TRIP_NOT_FOUND"                # 1003 - 行程不存在
    TRIP_EXPIRED = "TRIP_EXPIRED"                    # 1004 - 行程已过期
    TASK_NOT_FOUND = "TASK_NOT_FOUND"                # 1005 - 任务不存在
    TASK_ALREADY_COMPLETED = "TASK_ALREADY_COMPLETED" # 1006 - 任务已完成
    SOS_SEND_FAILED = "SOS_SEND_FAILED"              # 1007 - SOS发送失败
    CARD_NOT_FOUND = "CARD_NOT_FOUND"                # 1008 - 卡片不存在
    GUIDE_SERVICE_ERROR = "GUIDE_SERVICE_ERROR"      # 1009 - 导游服务错误
    INVALID_PHONE_FORMAT = "INVALID_PHONE_FORMAT"    # 1010 - 手机号格式错误
    PROFILE_NOT_BOUND = "PROFILE_NOT_BOUND"          # 1011 - 档案未绑定
    
    # 服务器错误 (500-599)
    INTERNAL_ERROR = "INTERNAL_ERROR"                 # 500 - 服务器内部错误
    DATABASE_ERROR = "DATABASE_ERROR"                 # 501 - 数据库错误
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR" # 502 - 外部服务错误
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"       # 503 - 服务不可用


# 错误码对应的HTTP状态码
ERROR_CODE_HTTP_STATUS: Dict[ErrorCode, int] = {
    # 成功
    ErrorCode.SUCCESS: 200,
    
    # 客户端错误
    ErrorCode.BAD_REQUEST: 400,
    ErrorCode.UNAUTHORIZED: 401,
    ErrorCode.FORBIDDEN: 403,
    ErrorCode.NOT_FOUND: 404,
    ErrorCode.METHOD_NOT_ALLOWED: 405,
    ErrorCode.CONFLICT: 409,
    ErrorCode.VALIDATION_ERROR: 422,
    
    # 业务错误
    ErrorCode.PROFILE_NOT_FOUND: 404,
    ErrorCode.PROFILE_ALREADY_EXISTS: 409,
    ErrorCode.TRIP_NOT_FOUND: 404,
    ErrorCode.TRIP_EXPIRED: 400,
    ErrorCode.TASK_NOT_FOUND: 404,
    ErrorCode.TASK_ALREADY_COMPLETED: 400,
    ErrorCode.SOS_SEND_FAILED: 500,
    ErrorCode.CARD_NOT_FOUND: 404,
    ErrorCode.GUIDE_SERVICE_ERROR: 500,
    ErrorCode.INVALID_PHONE_FORMAT: 400,
    ErrorCode.PROFILE_NOT_BOUND: 404,
    
    # 服务器错误
    ErrorCode.INTERNAL_ERROR: 500,
    ErrorCode.DATABASE_ERROR: 500,
    ErrorCode.EXTERNAL_SERVICE_ERROR: 502,
    ErrorCode.SERVICE_UNAVAILABLE: 503,
}


# 错误码对应的中文消息
ERROR_CODE_MESSAGE: Dict[ErrorCode, str] = {
    # 成功
    ErrorCode.SUCCESS: "操作成功",
    
    # 客户端错误
    ErrorCode.BAD_REQUEST: "请求参数错误",
    ErrorCode.UNAUTHORIZED: "未授权，请先登录",
    ErrorCode.FORBIDDEN: "无权限访问该资源",
    ErrorCode.NOT_FOUND: "请求的资源不存在",
    ErrorCode.METHOD_NOT_ALLOWED: "不支持的请求方法",
    ErrorCode.CONFLICT: "资源冲突",
    ErrorCode.VALIDATION_ERROR: "数据验证失败",
    
    # 业务错误
    ErrorCode.PROFILE_NOT_FOUND: "档案不存在",
    ErrorCode.PROFILE_ALREADY_EXISTS: "档案已存在",
    ErrorCode.TRIP_NOT_FOUND: "行程不存在",
    ErrorCode.TRIP_EXPIRED: "行程已过期",
    ErrorCode.TASK_NOT_FOUND: "任务不存在",
    ErrorCode.TASK_ALREADY_COMPLETED: "任务已完成",
    ErrorCode.SOS_SEND_FAILED: "紧急求助发送失败",
    ErrorCode.CARD_NOT_FOUND: "卡片不存在",
    ErrorCode.GUIDE_SERVICE_ERROR: "导游服务异常",
    ErrorCode.INVALID_PHONE_FORMAT: "手机号格式错误",
    ErrorCode.PROFILE_NOT_BOUND: "绑定子女账号，享受安全出行",
    
    # 服务器错误
    ErrorCode.INTERNAL_ERROR: "服务器内部错误",
    ErrorCode.DATABASE_ERROR: "数据库操作失败",
    ErrorCode.EXTERNAL_SERVICE_ERROR: "外部服务调用失败",
    ErrorCode.SERVICE_UNAVAILABLE: "服务暂时不可用",
}


class BusinessException(Exception):
    """业务异常基类"""
    
    def __init__(
        self,
        error_code: ErrorCode,
        message: Optional[str] = None,
        detail: Optional[str] = None
    ):
        self.error_code = error_code
        self.message = message or ERROR_CODE_MESSAGE.get(error_code, "未知错误")
        self.detail = detail
        self.http_status = ERROR_CODE_HTTP_STATUS.get(error_code, 500)
        super().__init__(self.message)


def get_error_response(error_code: ErrorCode, detail: Optional[str] = None) -> dict:
    """
    获取标准错误响应
    
    Args:
        error_code: 错误码
        detail: 详细错误信息（可选）
    
    Returns:
        标准错误响应字典
    """
    return {
        "code": ERROR_CODE_HTTP_STATUS.get(error_code, 500),
        "error": error_code.value,
        "message": ERROR_CODE_MESSAGE.get(error_code, "未知错误"),
        "detail": detail
    }
