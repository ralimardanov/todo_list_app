from settings.settings import Settings
import os

class PRDsettings(Settings):
    DEBUG = False
    SQLALCHEMY_ECHO = False

    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PASS = os.getenv("DB_PASS")
    DB_USER = os.getenv("DB_USER", "postgres")

    PRODUCTION = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"