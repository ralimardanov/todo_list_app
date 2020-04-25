from flask import Flask
import os
from db_setup.db_conf import db
from flask_marshmallow import Marshmallow
from marshmallow import fields,validate,validates_schema
from flask_migrate import Migrate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes="sha256_crypt")
ma = Marshmallow()

settings = {
    "prod": "settings.prdsettings.PRDsettings",
    "dev": "settings.devsettings.DEVsettings"
}

def get_settings(settings_name):
    if settings.get(settings_name):
        return settings.get(settings_name)
    raise Exception("Setting name you select %s isn't supported" % settings_name)

def create_app(settings_name):
    app = Flask(__name__)
    db.init_app(app)
    ma.init_app(app)
    settings_obj = get_settings(settings_name)
    app.config.from_object(settings_obj) #this loads the config from the settings_obj. also can be loaded from_envvar
    migrate = Migrate(app,db)
    # with app.app_context():
    #     db.create_all()

    return app