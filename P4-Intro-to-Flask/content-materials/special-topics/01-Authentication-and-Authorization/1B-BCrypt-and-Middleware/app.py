#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


# Flask server request-response and session storage utilities.
from flask import request, make_response, session

# Cryptographic hashing tools for user authentication.
import bcrypt

# Configured application/server and database instances.
from config import app, db

# Relative access to user and pet models.
from models import User, Pet

# Custom authorization decorator middleware.
from middleware import authorization_required


#######################################################
######## INITIAL SETUP ROUTES FOR APPLICATION #########
#######################################################


# GET route to access homepage.
# NOTE: No authentication required.
@app.route("/")
def root():
    return make_response({"msg": "Application loaded successfully.", "notice": "To enter the API, please log in or create an account."}, 200)

# GET route to access API entrypoint.
# NOTE: Requires user privileges.
@app.route("/api")
@authorization_required
def api(current_user):
    return make_response({"user_id": current_user["id"], "msg": "API access granted."}, 200)


#######################################################
############ INITIAL SETUP ROUTES FOR PETS ############
#######################################################


# GET route to view all pets.
# NOTE: Requires user privileges.
@app.route("/api/pets")
@authorization_required
def view_all_pets(current_user):
    all_pets = Pet.query.all()
    adoptable_pets = [pet.to_dict(only=("id", "name", "species")) for pet in all_pets if pet.is_adoptable is True]
    return make_response(adoptable_pets, 200)

# GET route to view individual pet by ID.
# NOTE: Requires user privileges.
@app.route("/api/pets/<int:pet_id>")
@authorization_required
def view_pet_by_id(current_user, pet_id: int):
    matching_pet = Pet.query.filter(Pet.id == pet_id).first()
    if not matching_pet:
        return make_response({"error": f"Pet ID `{pet_id}` not found in database."}, 404)
    return make_response(matching_pet.to_dict(only=("id", "name", "species")), 200)


#######################################################
######### ADMINISTRATOR-ONLY ROUTES FOR PETS ##########
#######################################################


# POST route to add new pet to database.
# NOTE: Requires administrative privileges.
@app.route("/api/pets", methods=["POST"])
@authorization_required(methods=["POST"])
def add_pet(current_user):
    POST_REQUEST = request.get_json()
    new_pet = Pet(
        name=POST_REQUEST["name"], 
        species=POST_REQUEST["species"],
        is_adoptable=True
    )
    db.session.add(new_pet)
    db.session.commit()
    return make_response(new_pet.to_dict(only=("id", "name", "species")), 201)

# PATCH route to edit pet's information in database.
# NOTE: Requires administrative privileges.
@app.route("/api/pets/<int:pet_id>", methods=["PATCH"])
@authorization_required(methods=["PATCH"])
def update_pet(current_user, pet_id: int):
    matching_pet = Pet.query.filter(Pet.id == pet_id).first()
    if not matching_pet:
        return make_response({"error": f"Pet ID `{pet_id}` not found in database."}, 404)
    PATCH_REQUEST = request.get_json()
    for attribute in PATCH_REQUEST:
        setattr(matching_pet, attribute, PATCH_REQUEST[attribute])
    db.session.add(matching_pet)
    db.session.commit()
    return make_response(matching_pet.to_dict(only=("id", "name", "species")), 200)

# DELETE route to remove pet from database.
# NOTE: Requires administrative privileges.
@app.route("/api/pets/<int:pet_id>", methods=["DELETE"])
@authorization_required(methods=["DELETE"])
def remove_pet(current_user, pet_id: int):
    matching_pet = Pet.query.filter(Pet.id == pet_id).first()
    if not matching_pet:
        return make_response({"error": f"Pet ID `{pet_id}` not found in database."}, 404)
    db.session.delete(matching_pet)
    db.session.commit()
    return make_response(matching_pet.to_dict(only=("id", "name", "species")), 204)


#######################################################
############# USER AUTHENTICATION ROUTING #############
#######################################################


# POST route to add new user to database.
@app.route("/signup", methods=["POST"])
def add_user():
    if request.method == "POST":
        payload = request.get_json()

        username = payload["username"]
        password = payload["password"]

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt=salt)

        new_user = User(
            username=username,
            password=hashed_password.decode("utf-8")
        )

        if new_user is not None:
            db.session.add(new_user)
            db.session.commit()
            session["user_id"] = new_user.id
            return make_response(new_user.to_dict(only=("id", "username", "created_at")), 201)
        else:
            return make_response({"error": "Invalid username or password. Try again."}, 401)
    else:
        return make_response({"error": f"Invalid request type. (Expected POST; received {request.method}.)"}, 400)
    
# POST route to authenticate user in database using session-stored credentials.
@app.route("/login", methods=["POST"])
def user_login():
    if request.method == "POST":
        payload = request.get_json()

        # matching_user = User.query.filter(User.username == payload["username"]).first()
        matching_user = User.query.filter(User.username.like(f"%{payload['username']}%")).first()

        AUTHENTICATION_IS_SUCCESSFUL = bcrypt.checkpw(
            password=payload["password"].encode("utf-8"),
            hashed_password=matching_user.password.encode("utf-8")
        )

        if matching_user is not None and AUTHENTICATION_IS_SUCCESSFUL:
            session["user_id"] = matching_user.id
            return make_response(matching_user.to_dict(only=("id", "username", "created_at")), 200)
        else:
            return make_response({"error": "Invalid username or password. Try again."}, 401)
    else:
        return make_response({"error": f"Invalid request type. (Expected POST; received {request.method}.)"}, 400)
    
# DELETE route to remove session-stored credentials for logged user.
@app.route("/logout", methods=["DELETE"])
def user_logout():
    if request.method == "DELETE":
        session["user_id"] = None
        # return make_response({"msg": "User successfully logged out."}, 200)
        return make_response({"msg": "User successfully logged out."}, 204)
    else:
        return make_response({"error": f"Invalid request type. (Expected DELETE; received {request.method}.)"}, 400)
        

#######################################################
############## ADDITIONAL ERROR HANDLING ##############
#######################################################


# General GET route for 404 error handling.
@app.errorhandler(404)
def page_not_found(error):
    return make_response({"error": "Page not found."}, 404)


#######################################################
######### FLASK BOILERPLATE FOR EXECUTION #############
#######################################################


if __name__ == "__main__":
    app.run(debug=True, port=5555)