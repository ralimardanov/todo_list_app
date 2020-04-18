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

    return jsonify(tlist),200  # default 200 qaytarir onsuz

@app.route("/todo/<id>", methods=["GET"])
def get_result(id):
    data = db.session.query(ToDo).filter_by(id=id).first()  # db.session.query(ToDo).get(id)
    if data:
        tdict = {
            "id": data.id, # id-de qayitmaliydi
            "date": data.date,
            "whattodo": data.whattodo
        } 
        return jsonify(tdict),200

    return jsonify({"result": f"Id {id} wasn't found"}),404

@app.route("/todo", methods=["POST"])
def create():
    data = request.json
    
    result = ToDo(**data)
    db.session.add(result)
    db.session.commit()
    # tdict = {
    #     # id-ni elav elememisen
    #     "date": result.date,
    #     "whattodo": result.whattodo
    # }
    schema = TodoSchema()
    data = schema.dump(result)
    return jsonify(data),201

@app.route("/todo/<id>", methods=["PUT"])
def update(id):
    result = db.session.query(ToDo).filter_by(id=id).first()
    if result:
        data = request.json
        result.date = data.get("date")
        result.whattodo = data.get("whattodo")
        db.session.commit()
        tdict = {
            "date": result.date,
            "whattodo": result.whattodo
        }
        return jsonify({"changes": f"{tdict}"}),201

    return jsonify({"result": f"Id {id} wasn't found"}),404

@app.route("/todo/<id>", methods=["DELETE"])
def delete_id(id):
    data = db.session.query(ToDo).filter_by(id=id).first()
    if data:
        db.session.delete(data)
        db.session.commit()
        return jsonify({"result": f"Id {id} was deleted"}),200

    return jsonify({"result": f" Id {id} wasn't found"}),404