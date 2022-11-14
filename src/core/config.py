from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Parser"
    debug: bool
    
    db_name: str
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    
    redis_host: str 
    redis_port: int 
    redis_database: str
    
    @property
    def database_connection_url(self):
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def redis_connection_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_database}"


class DevSettings(Settings):
    debug: bool = True
    
    db_name: str = "parser"
    db_host: str = "localhost"
    db_port: int = 6000
    db_user: str = "root"
    db_pass: str = "root"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_database: str = 1
    

class ProdSettings(Settings):
    debug: bool = False

    class Meta:
        env_file = ".env"


config = DevSettings()
