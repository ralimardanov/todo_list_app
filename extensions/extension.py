from flask_marshmallow import Marshmallow
from marshmallow import fields,validate,validates_schema
from flask_migrate import Migrate
from passlib.context import CryptContext
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager 
from flask_login import LoginManager 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
pwd_context = CryptContext(schemes="sha256_crypt")
ma = Marshmallow()
csrf = CSRFProtect()
jwt = JWTManager()
login_manager = LoginManager()
cors = CORS()
migrate = Migrate()