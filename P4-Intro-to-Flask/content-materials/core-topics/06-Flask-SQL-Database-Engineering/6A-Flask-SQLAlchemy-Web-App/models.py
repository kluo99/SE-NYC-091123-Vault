from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Mob(db.Model, SerializerMixin):
    __tablename__ = "mobs"

    mob_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    hit_points = db.Column(db.Integer, unique=False, nullable=False)
    damage = db.Column(db.Integer, unique=False, nullable=False)
    speed = db.Column(db.Integer, unique=False, nullable=False)
    is_hostile = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Mob '{self.name}'> (HP: {self.hit_points}, DMG: {self.damage}, SPD: {self.speed})"