from pydantic import Field
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    token: str = Field("token", env="TOKEN")