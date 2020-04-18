from flask import Flask
import os
from db_setup.db_conf import db
from flask_marshmallow import Marshmallow

ma = Marshmallow()

settings = {
    "prod": "settings.prdsettings.PRDsettings",
    "dev": "settings.devsettings.DEVsettings"
}

def get_settings(settings_name):
    if settings.get(settings_name):
        return settings.get(settings_name)

def create_app(settings_name):
    
    app = Flask(__name__)
    db.init_app(app)
    ma.init_app(app)
    settings_obj = get_settings(settings_name)
    app.config.from_object(settings_obj) #this loads the config from the settings_obj. also can be loaded from_envvar
    with app.app_context():
        db.create_all()

    return app