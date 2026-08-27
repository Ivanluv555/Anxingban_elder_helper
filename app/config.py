from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类 - 从环境变量或.env文件读取配置"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # 应用基础配置
    app_name: str = "安行伴-重庆试点"
    environment: str = "development"
    port: int = 8000
    
    # 数据库配置
    database_url: str
    
    # 安全配置
    token_secret: str
    secret_key: str
    
    # 微信配置
    wechat_webhook_url: str = ""
    
    # 短信配置
    sms_provider: str = "mock"
    
    # 业务配置
    pilot_city: str = "Chongqing"
    guide_scope: str = "knowledge_limited"
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    log_max_bytes: int = 104857600  # 100MB
    log_backup_count: int = 10

    @field_validator("database_url")
    @classmethod
    def require_mysql(cls, value: str) -> str:
        if value.startswith("mysql://"):
            value = value.replace("mysql://", "mysql+pymysql://", 1)
        if not value.startswith("mysql+pymysql://"):
            raise ValueError("DATABASE_URL must use the mysql+pymysql driver")
        return value


settings = Settings()
