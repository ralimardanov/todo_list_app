from flask import Flask
import os
from extensions.extension import ma,csrf,cors,db,login_manager,migrate,jwt
from app.user_app import user_app
from app.todo_app import todo_app
# import requests



settings = {
    "prod": "settings.prdsettings.PRDsettings",  # if it's a file or a directory, path will be like this - ../../
    "dev": "settings.devsettings.DEVsettings"
}

def get_settings(settings_name):
    if settings.get(settings_name):
        return settings.get(settings_name)
    raise Exception("Setting name you select %s isn't supported" % settings_name)

# def get_secret():  # eger token server daxilinde deilse bawqa yerden url uzerinnen goturmek ucun
#     url_private = os.getenv("PRIVATE_KEY_URL")
#     url_public= os.getenv("PUBLIC_KEY_URL")

#     private_key = requests.get(url_private)
#     public_key = requests.get(url_public)


#     return private_key.content,public_key.content

def create_app(settings_name):
    app = Flask(__name__,template_folder="../app/templates",static_folder="../app/static")
    app.register_blueprint(user_app)
    app.register_blueprint(todo_app)
    db.init_app(app)
    ma.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    login_manager.init_app(app)
    settings_obj = get_settings(settings_name)
    app.config.from_object(settings_obj)     #this loads the config from the settings_obj. also can be loaded from_envvar
    # app.config["JWT_PRIVATEKEY"],app.config["JWT_PUBLIC_KEY"] = get_secret()  burda ise configleri otuzdururuq        
    migrate.init_app(app,db) 

    return app