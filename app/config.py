from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-5-mini"
    reddit_user_agent: str = "ClosvantaAI/0.1"
    reddit_subreddits: str = "saas,Entrepreneur,ecommerce"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def subreddits(self) -> list[str]:
        return [x.strip() for x in self.reddit_subreddits.split(",") if x.strip()]


settings = Settings()
