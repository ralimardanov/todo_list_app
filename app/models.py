from extensions.extension import db
from sqlalchemy.sql import func              #to be able to use functions in DB
from flask_login import UserMixin
from flask_wtf import FlaskForm

class ToDo(db.Model):
    __tablename__ = "todo_list"
    
    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    date = db.Column(db.Date(),nullable=False)
    whattodo = db.Column(db.String,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def save_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update_db(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)        
        return self.save_db()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return True # return self-de ede bilersen eger silennen sora lazim olacagsa

class Users(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    name = db.Column(db.String(),nullable=False)
    surname = db.Column(db.String,nullable=False)
    email = db.Column(db.String(),nullable=False,unique=True)
    password = db.Column(db.String(),nullable=False)
    created = db.Column(db.DateTime(timezone=True), default=func.now()) #this will save datetime as it is in db
    todos = db.relationship("ToDo", backref="user", lazy=True)

    def __repr__(self):
        return "<User {} {} {}>".format(self.name,self.surname,self.email)

    def save_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update_db(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)
        return self.save_db()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return True            #you can do return self, in case if you'll use it somewhere else