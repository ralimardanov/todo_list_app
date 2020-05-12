from flask import Flask
import os
from db_setup.db_conf import db
from flask_marshmallow import Marshmallow
from marshmallow import fields,validate,validates_schema
from flask_migrate import Migrate
from passlib.context import CryptContext
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager 
from flask_login import LoginManager 

pwd_context = CryptContext(schemes="sha256_crypt")
ma = Marshmallow()
csrf = CSRFProtect()
jwt = JWTManager()
login_manager = LoginManager()

settings = {
    "prod": "settings.prdsettings.PRDsettings",  # if it's a file or a directory, path will be like this - ../../
    "dev": "settings.devsettings.DEVsettings"
}

def get_settings(settings_name):
    if settings.get(settings_name):
        return settings.get(settings_name)
    raise Exception("Setting name you select %s isn't supported" % settings_name)

def create_app(settings_name):
    app = Flask(__name__,template_folder="../app/templates",static_folder="../app/static")
    db.init_app(app)
    ma.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    settings_obj = get_settings(settings_name)
    app.config.from_object(settings_obj)             #this loads the config from the settings_obj. also can be loaded from_envvar
    Migrate(app,db) 

    return app