from app_init.app_factory import ma,fields,validate,validates_schema
from app.models import ToDo,Users
from app.utils import get_hash_password
class TodoSchema(ma.ModelSchema):   # burda db model lazimdi ve requireddi gostermesen error verecey
    date = fields.Date(required=True)  # default formati ISO formatidi,dunya standartinda
    whattodo = fields.Str(required=True,validate=[validate.Length(min=2,max=255)]) # validate listdi ona goreki bir nece validatsiyan ola biler

    class Meta:
        model = ToDo

class ToDoUpdateSchema(ma.Schema):  # bu ancag schema yaradirki validatsiya olsun ve model teleb etmir
    date = fields.Date()  # default formati ISO formatidi,dunya standartinda
    whattodo = fields.Str(validate=[validate.Length(min=2,max=255)])

class UserSchema(ma.ModelSchema):
    name =  fields.Str(required=True,validate=[validate.Length(min=2,max=255)])
    surname =  fields.Str(required=True,validate=[validate.Length(min=2,max=255)])
    email = fields.Email(required=True)
    password = fields.Str(required=True,validate=[validate.Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?#&]{8,}$")])
    password2 = fields.Str(required=True,validate=[validate.Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?#&]{8,}$")])

    @validates_schema(skip_on_field_errors=True) #eger error olsa yuxarida, bura girmiyecek
    def hash_password(self, data, **kwargs): 
        hashed_password = get_hash_password(data.get("password"))
        data.update({"password" : hashed_password})
        data.update({"email" : data.get("email").lower()})
        del data["password2"]
    class Meta:
        model = Users
class UserUpdateSchema(ma.Schema):
    name =  fields.Str(validate=[validate.Length(min=2,max=255)])
    surname =  fields.Str(validate=[validate.Length(min=2,max=255)])
    email = fields.Email()
    password = fields.Str(validate=[validate.Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?#&]{8,}$")])

    @validates_schema(skip_on_field_errors=True)
    def hash_password(self,data,**kwargs):
        hashed_password = get_hash_password(data.get("password"))
        data.update({"password" : hashed_password})
