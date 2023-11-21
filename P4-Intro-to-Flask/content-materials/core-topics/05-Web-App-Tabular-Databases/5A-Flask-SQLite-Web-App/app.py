"""
FILENAME:       `app.py`
TITLE:          Flask REST API integrated with SQLite3.
AUTHOR:         Aakash 'Kash' Sudhakar
DESCRIPTION:    A tutorial mini-project on setting up backend servers
                that handle RESTful API calls via HTTP requests and store,
                modify, and query data via tabular SQLite3 databases. 
USAGE:          Run in CLI with command `python(3) app.py`, `flask run`, or
                `flask --app app.py --debug run`. 
"""


################################################################################
#### IMPORTATIONS AND INITIALIZATIONS FOR SERVER DEVELOPMENT IN FLASK & SQL ####
################################################################################


from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

import utils


################################################################################
##################### FLASK SERVER SETUP AND CONFIGURATIONS ####################
################################################################################


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


################################################################################
####################### FLASK API DEVELOPMENT AND TESTING ######################
################################################################################


# NOTE: For all API routes, you can use either `http://localhost` or 
#       `http://AAA.B.C.D`, where the latter option's letters are replaced by 
#       the actual IP address from which your application loads.


# GET Request to Access Root of API.
@app.route("/", methods=["GET"])
def api_home():
    return jsonify({"message": "Welcome to the Minecraft Mobs API!"})

# GET Request to Access API Entry Point.
@app.route("/api", methods=["GET"])
def api_access():
    return jsonify({"message": "This API supports access to GET, POST, PATCH, and DELETE requests."})

# GET Request to Access All Mob Data.
@app.route("/api/mobs", methods=["GET"])
def api_get_mobs():
    return jsonify(utils.get_mobs())

# GET Request to Access Single Mob Data by ID.
@app.route("/api/mobs/<int:mob_id>", methods=["GET"])
def api_get_mob_by_id(mob_id):
    return jsonify(utils.get_mob_by_id(mob_id))

# POST Request to Add New Mob to Database.
@app.route("/api/mobs", methods=["POST"])
def api_add_mob():
    new_mob = request.json
    return jsonify(utils.create_mob(new_mob))

# PATCH Request to Update One Mob Metric for Single Mob in Database.
@app.route("/api/mobs/<int:mob_id>", methods=["PATCH"])
def api_update_mob(mob_id):
    new_mob_info = request.json
    return jsonify(utils.update_mob(mob_id, new_mob_info))

# DELETE Request to Delete Mob from Database.
@app.route("/api/mobs/<int:mob_id>", methods=["DELETE"])
def api_delete_mob(mob_id):
    return jsonify(utils.delete_mob(mob_id))

# Error-Handling Routing Function for 404 Resource Not Found.
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Page Not Found!"}), 404)


################################################################################
####################### LAUNCHING SERVER-SIDE APPLICATION ######################
################################################################################


if __name__ == "__main__":
    app.run(port=5000)