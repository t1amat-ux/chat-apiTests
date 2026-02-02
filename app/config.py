from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "chat_db"
    

    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    

    DEFAULT_MESSAGE_LIMIT: int = 20
    MAX_MESSAGE_LIMIT: int = 100
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    class Config:
        env_file = ".env"

settings = Settings()