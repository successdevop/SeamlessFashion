from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import user


class AddressSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = user.Address
        load_instance = True
        include_fk = True
        fields = ("address_id", "street", "city", "state", "zipcode", "user_id")

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)