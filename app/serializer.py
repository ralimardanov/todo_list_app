from app_init.app_factory import ma,fields,validate,validates_schema
from app.models import ToDo,Users
from app.utils import get_hash_password

class TodoSchema(ma.ModelSchema):                                                # db model is required here, flask-nan integratsiya olunduguna gore flask_marshmallow modulunnan goturulur
    date = fields.Date(required=True)                                              # by default is used ISO format. fields ise independent funksionalliq 9olduguna gore burda adi marshmallow-dan istifade edirik
    whattodo = fields.Str(required=True,validate=[validate.Length(min=2,max=255)]) # validate is a list and several validations can be used, that's why [] brackets are used

    class Meta:
        model = ToDo

class ToDoUpdateSchema(ma.Schema):  # this one only creates schema for validation and doesn't need db model
    date = fields.Date()  
    whattodo = fields.Str(validate=[validate.Length(min=2,max=255)])

class UserSchema(ma.ModelSchema):
    name =  fields.Str(required=True,validate=[validate.Length(min=2,max=255)])
    surname =  fields.Str(required=True,validate=[validate.Length(min=2,max=255)])
    email = fields.Email(required=True)
    password = fields.Str(required=True,validate=[validate.Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?#&]{8,}$")])
    password2 = fields.Str(required=True,validate=[validate.Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?#&]{8,}$")])

    @validates_schema(skip_on_field_errors=True) #if there will be an error above, it won't go in here
    def hash_password(self, data, **kwargs): 
        hashed_password = get_hash_password(data.get("password"))
        data.update({"password" : hashed_password})
        data.update({"email" : data.get("email").lower()})
        del data["password2"]
    class Meta:
        model = Users

class UserUpdateSchema(ma.Schema): #flask-nan integratsiya olunduguna gore flask_marshmallow modulunnan goturulur
    name =  fields.Str(validate=[validate.Length(min=2,max=255)])
    surname =  fields.Str(validate=[validate.Length(min=2,max=255)])
    email = fields.Email()
    password = fields.Str(validate=[validate.Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?#&]{8,}$")])

    @validates_schema(skip_on_field_errors=True)
    def hash_password(self,data,**kwargs):
        hashed_password = get_hash_password(data.get("password"))
        data.update({"password" : hashed_password})

        
class UserUpdateFormSchema(ma.Schema):
    name =  fields.Str(validate=[validate.Length(min=2,max=255)])
    surname =  fields.Str(validate=[validate.Length(min=2,max=255)])
    email = fields.Email()
    password = fields.Str(validate=[validate.Length(min=3,max=123)])

    @validates_schema(skip_on_field_errors=True)
    def hash_password(self,data,**kwargs):
        hashed_password = get_hash_password(data.get("password"))
        data.update({"password" : hashed_password})