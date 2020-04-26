from app_init.app_factory import create_app
from app.models import ToDo,Users
from flask import request,jsonify,make_response,render_template
from db_setup.db_conf import db
import os
from app.serializer import TodoSchema,ToDoUpdateSchema,UserSchema,UserUpdateSchema
from pprint import pprint
from marshmallow import ValidationError
from app.utils import verify_password


settings_name = os.getenv("APP_SETTINGS")
app = create_app(settings_name)


# flask login-e baxarsan https://flask-login.readthedocs.io/en/latest/
#bootstrap cdn https://www.bootstrapcdn.com/
# user datani edit etmek ucun endpoint yazmaga caliw
#jinja https://jinja.palletsprojects.com/en/2.11.x/

########################################################
                    # after changes:
########################################################

# ToDo part:
@app.route("/todo", methods=["GET"])
def get_results():
    # results = db.session.query(ToDo).all() # bu method pure SqlAlchemy-ide verilme qaydasidi
    results = ToDo.query.all() # ancaq Flask-Sqlalchemy-de iwleyir
    return TodoSchema().jsonify(results,many=True)
    # eger list-in icinde objectleri serialize elemek isdesen many=True vermelisen

@app.route("/todo/<id>", methods=["GET"])
def get_result(id):
    data = ToDo.query.filter_by(id=id).first() 
    if data:
        return TodoSchema().jsonify(data)
    return jsonify({"result": f"Id {id} wasn't found"}),404

@app.route("/todo", methods=["POST"])
def create():
    data = request.json
    todo = TodoSchema().load(data)
    todo.save_db()
    return TodoSchema().jsonify(todo)

@app.route("/todo/<id>", methods=["PUT"])
def update(id):
    result = ToDo.query.filter_by(id=id).first()
    if result:
        data = request.json
        data = ToDoUpdateSchema().load(data)
        result = result.update_db(**data)
        return TodoSchema().jsonify(result)        
    return jsonify({"result": f"Id {id} wasn't found"}),404

@app.route("/todo/<id>", methods=["DELETE"])
def delete_id(id):
    data = ToDo.query.filter_by(id=id).first()
    if data:
        data.delete_from_db()
        return jsonify({"result": f"Id {id} was deleted"})
    return jsonify({"result": f" Id {id} wasn't found"}),404

# Users part:
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    try:
        user = UserSchema().load(data)
        user.save_db()
    except ValidationError as err:
        return jsonify(err.messages),400
    except Exception as err:
        return jsonify({"result": str(err)}),400
    return UserSchema(exclude=("password",)).jsonify(user)

@app.route("/users", methods=["GET"])
def get_users_results():
    results = Users.query.all()
    return UserSchema(exclude=("password",)).jsonify(results,many=True)

@app.route("/users/<id>", methods=["GET"])
def get_user_id(id):
    data = Users.query.filter_by(id=id).first()
    if data:
        return UserSchema(exclude=("password",)).jsonify(data)
    return jsonify({"result": f"Id {id} wasn't found"}),404

@app.route("/users/<id>", methods=["PUT"])
def update_user_id(id):
    result = Users.query.filter_by(id=id).first()
    if result:
        data = request.json
        data = UserUpdateSchema().load(data)
        result = result.update_db(**data)
        return UserSchema(exclude=("password",)).jsonify(result)
    return jsonify({"result": f"Id {id} wasn't found"}),404

@app.route("/users/<id>", methods=["DELETE"])
def delete_user_id(id):
    data = Users.query.filter_by(id=id).first()
    if data:
        data.delete_from_db()
        return jsonify({"result": f"Id {id} was deleted"})
    return jsonify({"result": f" Id {id} wasn't found"}),404

@app.route("/api/users/login", methods=["POST"]) # api-i callarin qabagina api artir
def login_user():
    data = request.get_json()
    user = Users.query.filter_by(email=data.get("email").lower()).first()
    if user:
        if verify_password(data.get("password"),user.password):
            return UserSchema(exclude=("password",)).jsonify(user)
    return jsonify({"message": "email or password incorrect"}),404


@app.route("/users/signedup",methods=["GET","POST"])
def signed_up():
    if request.method == "GET":
        return make_response(render_template("index.html"),200)

    elif request.method == "POST":
        if request.form["password"] == request.form["password2"]:
            user = UserSchema().load(data = request.form)
            user.save_db()
            schema = UserSchema()
            user = schema.dump(user)
            user.pop("password")

            return make_response(render_template("dashboard.html",user=user),200)

@app.route("/users/login", methods=["POST","GET"])
def login_user_html():
    if request.method == "GET":
        return make_response(render_template("login.html"))
    elif request.method == "POST":
        user = Users.query.filter_by(email=request.form.get("email").lower()).first()
        if user:
            if verify_password(request.form.get("password"),user.password):

                schema = UserSchema()
                user = schema.dump(user)
                user.pop("password")
                return make_response(render_template("dashboard.html",user=user),200)

    return jsonify({"message": "email or password incorrect"}),404

