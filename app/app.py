from app_init.app_factory import create_app
from app.models import ToDo
from flask import request,jsonify
from db_setup.db_conf import db
import os
from app.serializer import TodoSchema

settings_name = os.getenv("APP_SETTINGS")

app = create_app(settings_name)   # migration elave ele

@app.route("/todo/all", methods=["GET"])
def get_results():
    results = db.session.query(ToDo).all()
    tlist = []
    for ind in results:
        tdict = {
            "id" : ind.id,
            "date" : ind.date,
            "whattodo" : ind.whattodo
        }
        tlist.append(tdict)

    return jsonify(tlist) # default 200 qaytarir onsuz

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
    result = ToDo(**data)
    db.session.add(result)
    db.session.commit()
    schema = TodoSchema()
    data = schema.dump(result) # use this ToDoSchema everywhere where you return dictionary.
    return jsonify(data),201

@app.route("/todo/<id>", methods=["PUT"])
def update(id):
    result = db.session.query(ToDo).filter_by(id=id).first()
    if result:
        data = request.json
        result.date = data.get("date")
        result.whattodo = data.get("whattodo")
        db.session.commit()
        schema = TodoSchema
        data = schema.dump(result)
        return jsonify({"changes": f"{data}"}),201
    return jsonify({"result": f"Id {id} wasn't found"}),404

@app.route("/todo/<id>", methods=["DELETE"])
def delete_id(id):
    data = db.session.query(ToDo).filter_by(id=id).first()
    if data:
        db.session.delete(data)
        db.session.commit()
        return jsonify({"result": f"Id {id} was deleted"})
    return jsonify({"result": f" Id {id} wasn't found"}),404