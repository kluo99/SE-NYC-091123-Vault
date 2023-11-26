from config import db
from sqlalchemy_serializer import SerializerMixin

class Pet(db.Model, SerializerMixin):
    __tablename__ = "pet_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    species = db.Column(db.String, nullable=False)
    is_adoptable = db.Column(db.Boolean, default=True)

class User(db.Model, SerializerMixin):
    __tablename__ = "user_table"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def is_administrator(self):
        return self.is_admin