from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Parser"
    debug: bool
    
    db_name: str
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    
    @property
    def database_connection_url(self):
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


class DevSettings(Settings):
    debug: bool = True
    
    db_name: str = "parser"
    db_host: str = "db"
    db_port: int = 5432
    db_user: str = "root"
    db_pass: str = "root"


class ProdSettings(Settings):
    debug: bool = False

    class Meta:
        env_file = ".env"


config = DevSettings()
