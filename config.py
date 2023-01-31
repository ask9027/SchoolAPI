from pydantic import BaseSettings


class Settings(BaseSettings):
    apiKey:str
    authDomain:str
    projectId:str
    storageBucket:str
    messagingSenderId:str
    appId:str
    databaseURL:str

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
