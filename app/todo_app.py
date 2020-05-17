from flask import Blueprint,jsonify,request
from app.models import ToDo
from app.serializer import TodoSchema,ToDoUpdateSchema
from extensions.extension import csrf


todo_app = Blueprint("todo_app",__name__)


@todo_app.route("/api/todo", methods=["GET"])
@csrf.exempt
def get_results():
    # results = db.session.query(ToDo).all()         - this method is pure SqlAlchemy method
    results = ToDo.query.all()                       # this one works only on Flask-Sqlalchemy
    return TodoSchema().jsonify(results,many=True)
                                                     # if you want to serialize objects inside list, you should use many=True

@todo_app.route("/api/todo/<id>", methods=["GET"])
@csrf.exempt
def get_result(id):
    data = ToDo.query.filter_by(id=id).first() 
    if data:
        return TodoSchema().jsonify(data)
    return jsonify({"result": f"Id {id} wasn't found"}),404

@todo_app.route("/api/todo", methods=["POST"])
@csrf.exempt
def create():
    data = request.json
    todo = TodoSchema().load(data)
    todo.save_db()
    return TodoSchema().jsonify(todo)

@todo_app.route("/api/todo/<id>", methods=["PUT"])
@csrf.exempt
def update(id):
    result = ToDo.query.filter_by(id=id).first()
    if result:
        data = request.json
        data = ToDoUpdateSchema().load(data)
        result = result.update_db(**data)
        return TodoSchema().jsonify(result)        
    return jsonify({"result": f"Id {id} wasn't found"}),404

@todo_app.route("/api/todo/<id>", methods=["DELETE"])
@csrf.exempt
def delete_id(id):
    data = ToDo.query.filter_by(id=id).first()
    if data:
        data.delete_from_db()
        return jsonify({"result": f"Id {id} was deleted"})
    return jsonify({"result": f" Id {id} wasn't found"}),404