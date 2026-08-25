from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "安行伴-重庆试点"
    environment: str = "development"
    database_url: str = "mysql+pymysql://root:password@localhost:3306/anbanx?charset=utf8mb4"
    token_secret: str = "dev-secret-change-in-production"
    wechat_webhook_url: str = ""
    sms_provider: str = "mock"
    pilot_city: str = "Chongqing"
    guide_scope: str = "knowledge_limited"
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    log_max_bytes: int = 104857600  # 100MB
    log_backup_count: int = 10
    
    # 端口配置
    port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("database_url")
    @classmethod
    def require_mysql(cls, value: str) -> str:
        if value.startswith("mysql://"):
            value = value.replace("mysql://", "mysql+pymysql://", 1)
        if not value.startswith("mysql+pymysql://"):
            raise ValueError("DATABASE_URL must use the mysql+pymysql driver")
        return value


settings = Settings()
