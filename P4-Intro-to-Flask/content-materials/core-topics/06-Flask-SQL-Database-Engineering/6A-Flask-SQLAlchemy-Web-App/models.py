"""
FILENAME:       `models.py`
TITLE:          Flask REST API integrated with SQLite3 and SQLAlchemy.
AUTHOR:         Aakash 'Kash' Sudhakar
DESCRIPTION:    A tutorial mini-project on setting up backend servers
                that handle RESTful API calls via HTTP requests and store,
                modify, and query data via tabular SQLite3 databases extended
                with SQL-Alchemy for additional functionalities, validations,
                security, and authentication.
USAGE:          Imports automatically into `app.py` and `seed.py`. 
"""


################################################################################
##### IMPORTATIONS AND INITIALIZATIONS FOR WRITING FLASK-SQLALCHEMY MODELS #####
################################################################################


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# Define Metadata Structure for SQLAlchemy Models.
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Reinitialize Database Instance Using Updated Metadata.
db = SQLAlchemy(metadata=metadata)


################################################################################
####################### DATABASE OBJECT MODEL DEFINITIONS ######################
################################################################################


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