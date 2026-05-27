from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.user import UserModel


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        fields = ("user_id", "full_name", "email", "password", "role", "is_verified", "created_at")

user_schema = UserSchema()
users_schema = UserSchema(many=True)