from db_setup.db_conf import db

class ToDo(db.Model):
    __tablename__ = "todo_list"
    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    date = db.Column(db.String(),nullable=False)
    whattodo = db.Column(db.String,nullable=False)