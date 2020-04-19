from app_init.app_factory import ma 
from app.models import ToDo

class TodoSchema(ma.ModelSchema):
    class Meta:
        model = ToDo
