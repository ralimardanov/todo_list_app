from app_init.app_factory import create_app
from app.models import ToDo,Users
from flask import request,jsonify
from db_setup.db_conf import db
import os
from app.serializer import TodoSchema,UpdateSchema,UserSchema
from pprint import pprint
from marshmallow import ValidationError
from app.utils import verify_password

#Butun queryleri deyish ve jsonyfylarida
#User endpointlerin duzelt hamsin
# user datalarin qaytaranda passwordu exclude ele
# user-in update schemasin yaz


settings_name = os.getenv("APP_SETTINGS")

app = create_app(settings_name)   # migration elave ele

@app.route("/todo", methods=["GET"])
def get_results():
    # results = db.session.query(ToDo).all() # bu method pure SqlAlchemy-ide verilme qaydasidi
    results = ToDo.query.all() # ancaq Flask-Sqlalchemy-de iwleyir
    # tlist = []
    # for ind in results:
    #     tdict = {
    #         "id" : ind.id,
    #         "date" : ind.date,
    #         "whattodo" : ind.whattodo
    #     }
    #     tlist.append(tdict)
    return TodoSchema().jsonify(results,many=True) # eger list-in icinde objectleri serialize elemek isdesen many=True vermelisen
    # return jsonify(tlist) # default 200 qaytarir onsuz

@app.route("/todo/<id>", methods=["GET"])
def get_result(id):
    data = db.session.query(ToDo).filter_by(id=id).first()  # db.session.query(ToDo).get(id)
    if data:
        tdict = {
            "id": data.id,
            "date": data.date,
            "whattodo": data.whattodo
        } 
        return jsonify(tdict)
    return jsonify({"result": f"Id {id} wasn't found"}),404

@app.route("/todo", methods=["POST"])
def create():
    data = request.json
    # result = ToDo(**data)
    # db.session.add(result)
    # db.session.commit()
    # schema = TodoSchema()
    # data = schema.dump(result) # use this ToDoSchema everywhere where you return dictionary.
    todo = TodoSchema().load(data)
    todo.save_db()
    return TodoSchema().jsonify(todo)
    # return jsonify(data),201

@app.route("/todo/<id>", methods=["PUT"])
def update(id):
    result = db.session.query(ToDo).filter_by(id=id).first() # ozun duzeldersen
    print(result)
    if result:
        data = request.json
        # result.date = data.get("date")
        # result.whattodo = data.get("whattodo")
        # db.session.commit()
        # schema = TodoSchema
        # data = schema.dump(result)
        # return jsonify({"changes": f"{data}"}),201
        data = UpdateSchema().load(data)
        result = result.update_db(**data)
        return TodoSchema().jsonify(result)
        
    return jsonify({"result": f"Id {id} wasn't found"}),404

@app.route("/todo/<id>", methods=["DELETE"])
def delete_id(id):
    data = db.session.query(ToDo).filter_by(id=id).first() # isdesen duzelt
    if data:
        data.delete_from_db()
        return jsonify({"result": f"Id {id} was deleted"})
    return jsonify({"result": f" Id {id} wasn't found"}),404


@app.route("/users",methods=["POST"])
def create_user():
    data = request.get_json()
    try:
        user = UserSchema().load(data)
        user.save_db()
    except ValidationError as err:
        return jsonify(err.messages),400

   

    return UserSchema().jsonify(user)

@app.route("/users/login", methods=["POST"])
def login_user():
    data = request.get_json()
    user = Users.query.filter_by(email=data.get("email")).first()
    if user:
        if verify_password(data.get("password"),user.password):
            return UserSchema().jsonify(user)

    return jsonify({"message": "email or password incorrect"}),404



