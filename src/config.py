from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # Application Settings
    app_name: str = "Void"
    app_version: str = "0.1.0"
    app_description: str = "Answers from the Void"
    
    # Database Settings
    database_url: str = "sqlite:///./void.sqlite"
    db_service: str = "sqlmodel"
    
    # Authentication Settings
    auth_method: str = "fasthtml"
    
    # Supabase Settings (if using Supabase)
    supabase_url: str | None = "https://void.supabase.co"
    supabase_key: str | None = "your-supabase-anon-key"
    supabase_service_key: str | None = "your-supabase-service-key"
    
    # Email Settings
    smtp_server: str = "smtp.resend.com"
    smtp_port: int = 465
    smtp_username: str = "resend"
    smtp_password: str = "re_xxxx"
    resend_api_key: str = "re_xxxx"
    
    # OAuth Settings
    google_oauth_id: str | None = "your-google-oauth-id"
    google_oauth_secret: str | None = "your-google-oauth-secret"
    github_oauth_id: str | None = "your-github-oauth-id"
    github_oauth_secret: str | None = "your-github-oauth-secret"

    @property
    def is_using_supabase(self) -> bool:
        return self.db_service == "supabase" or self.auth_method == "supabase"

    @property
    def is_using_oauth(self) -> bool:
        return bool(self.google_oauth_id or self.github_oauth_id)

    @property
    def is_using_subscriptions(self) -> bool:
        return bool(self.lemonsqeezy_api_key)

