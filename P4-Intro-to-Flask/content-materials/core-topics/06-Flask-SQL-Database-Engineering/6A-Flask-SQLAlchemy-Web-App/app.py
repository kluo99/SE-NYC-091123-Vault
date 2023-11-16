"""
FILENAME:       `app.py`
TITLE:          Flask REST API integrated with SQLite3 and SQLAlchemy.
AUTHOR:         Aakash 'Kash' Sudhakar
DESCRIPTION:    A tutorial mini-project on setting up backend servers
                that handle RESTful API calls via HTTP requests and store,
                modify, and query data via tabular SQLite3 databases extended
                with SQL-Alchemy for additional functionalities, validations,
                security, and authentication.
USAGE:          Run in CLI with command `python(3) app.py`, `flask run`, or
                `flask --app app.py --debug run`. 
"""


################################################################################
### IMPORTATIONS AND INITIALIZATIONS FOR DEVELOPING FLASK-SQLALCHEMY SERVERS ###
################################################################################


from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
import os

# Import Database Prototype and Defined Model Architecture(s).
from models import db, Mob


################################################################################
##################### FLASK SERVER SETUP AND CONFIGURATIONS ####################
################################################################################


# Establish Correct Path to SQL Database Source.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'mobs.db')}")

# Create Flask Application Instance and Configure with SQLAlchemy.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
app.debug = True


################################################################################
##################### DATABASE MIGRATION AND INSTANTIATION #####################
################################################################################


# Migrate Database to Most Recent Application Instance.
migrate = Migrate(app, db)

# Reinstantiate Application.
db.init_app(app)


################################################################################
####################### FLASK API DEVELOPMENT AND TESTING ######################
################################################################################


# NOTE: For all API routes, you can use either `http://localhost` or 
#       `http://AAA.B.C.D`, where the latter option's letters are replaced by 
#       the actual IP address from which your application loads.


# GET Request to Access Root of API.
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Minecraft Mobs API!"})

# GET Request to Access API Entry Point.
@app.route("/api", methods=["GET"])
def api():
    return jsonify({
        "message": "This API supports access to GET, POST, PATCH, and DELETE requests.",
        "addendum": "This API is powered by Flask-SQLAlchemy for improved database validation."
        })
    
# GET Request to Access All Mob Data.
@app.route("/api/mobs", methods=["GET"])
def get_mobs():
    mobs = Mob.query.all()
    data = [mob.to_dict() for mob in mobs]
    return make_response(jsonify(data), 200)

# GET Request to Access Single Mob Data by ID.
@app.route("/api/mobs/<int:mob_id>", methods=["GET"])
def get_mob_by_id(mob_id: int):
    mob = Mob.query.filter(Mob.mob_id == mob_id).first()
    if not mob:
        return make_response(jsonify({"error": "Mob not found"}), 404)
    return make_response(jsonify(mob.to_dict()), 200)

# POST Request to Add New Mob to Database.
@app.route("/api/mobs", methods=["POST"])
def create_mob():
    try:
        mob = Mob(
            name = request.json["name"],
            hit_points = request.json["hit_points"],
            damage = request.json["damage"],
            speed = request.json["speed"],
            is_hostile = request.json["is_hostile"])
        db.session.add(mob)
        db.session.commit()
        return make_response(jsonify(mob.to_dict()), 200)
    except:
        return make_response(jsonify({"error": "Validation Error"}), 404)

# PATCH Request to Update One Mob Metric for Single Mob in Database.
@app.route("/api/mobs/<int:mob_id>", methods=["PATCH"])
def update_mob_by_id(mob_id: int):
    mob = Mob.query.filter(Mob.mob_id == mob_id).first()
    if not mob:
        return make_response(jsonify({"error": "Mob not found"}), 404)
    payload = request.json
    try:
        for key in payload:
            setattr(mob, key, payload[key])
        db.session.add(mob)
        db.session.commit()
        return make_response(jsonify(mob.to_dict()), 202)
    except:
        return make_response(jsonify({"error": "Validation Error"}), 404)

# DELETE Request to Delete Mob from Database.
@app.route("/api/mobs/<int:mob_id>", methods=["DELETE"])
def delete_mob_by_id(mob_id: int):
    mob = Mob.query.filter(Mob.mob_id == mob_id).first()
    if not mob:
        return make_response(jsonify({"error": "Mob not found"}), 404)
    db.session.delete(mob)
    db.session.commit()
    return make_response(jsonify(mob.to_dict()), 200)

# Error-Handling Routing Function for 404 Resource Not Found.
@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({"error": "Page Not Found!"}), 404)