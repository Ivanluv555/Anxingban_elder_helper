from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "安行伴-重庆试点"
    environment: str = "dev"
    database_url: str = "sqlite:///./elder_helper.db"
    token_secret: str = "replace-with-env-secret"
    wechat_webhook_url: str = ""
    sms_provider: str = "mock"
    pilot_city: str = "Chongqing"
    guide_scope: str = "knowledge_limited"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
