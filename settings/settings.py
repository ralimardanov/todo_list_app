# With flask-env you can define your default configuration options in code and very easily override via environment variables.
from flask_env import MetaFlaskEnv
import os
from datetime import timedelta

project_name = "todo_list_app"

class Settings(metaclass=MetaFlaskEnv): #you instruct your class to use this metaclass exactly
    DEBUG = True
    JWT_SECRET_KEY = os.urandom(32)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    SECRET_KEY = os.urandom(32) #for generating crytographically suitable random bytes to use for the secret key
    SQLALCHEMY_ECHO = True      #If set to True SQLAlchemy will log all the statements issued to stderr which can be useful for debugging.

    LOGGER_NAME = "%s.logger" % project_name
    LOG_FILENAME = "app.%s.log" % project_name  
    JWT_PUBLIC_KEY = open("public.pem").read()
    JWT_PRIVATE_KEY = open("my-passless-private.key").read()
    JWT_ALGORITHM = "RS256"