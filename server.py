from app_init.app_factory import create_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple 
import os

# werkzeug modulu flask-in icinde gelir,test serveri run eden odu, ve uswgi-i run edende odu

settings_name = os.getenv("APP_SETTINGS")

flask_app = create_app(settings_name)

app = DispatcherMiddleware(flask_app)

if  __name__ == "__main__":
    run_simple(application=app,port=5000,hostname="127.0.0.1",use_debugger=flask_app.config["DEBUG"])

