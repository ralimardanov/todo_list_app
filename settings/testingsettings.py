from settings.settings import Settings
import os


class Testsettings(Settings):
    TESTING = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = f"postgresql:///testlessondb"
