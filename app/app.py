from app_init.app_factory import create_app
from app.models import ToDo
from flask import request,jsonify
from db_setup.db_conf import db
import os

settings_name = os.getenv("APP_SETTINGS")

app = create_app(settings_name)

@app.route("/all", methods=["GET"])
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

    return jsonify(tlist),200

@app.route("/<id>", methods=["GET"])
def get_result(id):
    data = db.session.query(ToDo).filter_by(id=id).first()
    if data:
        tdict = {
            "date": data.date,
            "whattodo": data.whattodo
        } 
        return jsonify(tdict),200
    else:
        return jsonify({"result": f"Id {id} wasn't found"}),404

@app.route("/", methods=["POST"])
def create():
    data = request.json
    result = ToDo(**data)
    db.session.add(result)
    db.session.commit()
    tdict = {
        "date": result.date,
        "whattodo": result.whattodo
    }
    return jsonify(tdict),201

@app.route("/<id>", methods=["DELETE"])
def delete_id(id):
    data = db.session.query(ToDo).filter_by(id=id).first()
    if data:
        db.session.delete(data)
        db.session.commit()
        return jsonify({"result": f"Id {id} was deleted"}),200
    else:
        return jsonify({"result": f" Id {id} wasn't found"}),404