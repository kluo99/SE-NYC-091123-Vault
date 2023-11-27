#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


# Configured database instance.
from config import db
# SQLAlchemy object model serialization tools.
from sqlalchemy_serializer import SerializerMixin


#######################################################
######### RELATIONAL DATABASE OBJECT MODEL(S) #########
#######################################################


# Database object model definition for user(s).
# NOTE: `User.password` must be cryptographically hashed prior to database storage.
class User(db.Model, SerializerMixin):
    __tablename__ = "user_table"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())