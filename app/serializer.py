from app_init.app_factory import ma ,fields,validate,validates_schema
from app.models import ToDo,Users
from app.utils import get_hash_password

class TodoSchema(ma.ModelSchema):
    date = fields.Date(required=True)  # default formati ISO formatidi,dunya standartinda
    whattodo = fields.Str(required=True,validate=[validate.Length(min=2,max=255)])

    class Meta:
        model = ToDo


class UpdateSchema(ma.Schema):
    date = fields.Date()  # default formati ISO formatidi,dunya standartinda
    whattodo = fields.Str(validate=[validate.Length(min=2,max=255)])


class UserSchema(ma.ModelSchema):
    name =  fields.Str(required=True,validate=[validate.Length(min=2,max=255)])
    surname =  fields.Str(required=True,validate=[validate.Length(min=2,max=255)])
    email = fields.Email(required=True)
    password = fields.Str(required=True,validate=[validate.Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?#&]{8,}$")])

    @validates_schema(skip_on_field_errors=True)
    def hash_password(self,data,**kwargs):
        hashed_password = get_hash_password(data.get("password"))
        data.update({"password" : hashed_password})


    class Meta:
        model = Users