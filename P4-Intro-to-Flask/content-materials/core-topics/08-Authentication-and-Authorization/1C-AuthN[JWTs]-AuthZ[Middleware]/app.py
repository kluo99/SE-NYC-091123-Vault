#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


# Flask server request-response utilities.
from flask import request, make_response, jsonify
# Configured application/server and database instances.
from config import app, db
# Relative access to user and pet models.
from models import User, Pet
# Custom authorization decorator middleware.
from middleware import authorization_required

# JSON web tokens and cryptographic hashing tools.
# NOTE: To be used for JWT token construction and encoding/decoding. 
import jwt, bcrypt

# Datetime-parsing utilities.
# NOTE: To be used for JWT expiration configuration.
from datetime import datetime, timedelta


#######################################################
######## INITIAL SETUP ROUTES FOR APPLICATION #########
#######################################################


# GET route to access homepage.
# NOTE: No authentication required.
@app.route("/")
def root():
    return make_response({"msg": "Application loaded successfully.", 
                          "notice": "To enter the API, please log in or create an account."}, 200)

# GET route to access API entrypoint.
# NOTE: Requires user privileges. (Can use decorator middleware.)
@app.route("/api")
@authorization_required
def api(current_user):
    return make_response({"user_id": current_user["id"], 
                          "msg": "API access granted."}, 200)


#######################################################
############ INITIAL SETUP ROUTES FOR PETS ############
#######################################################


# GET route to view all pets.
# NOTE: Requires user privileges. (Can use decorator middleware.)
@app.route("/api/pets")
@authorization_required
def view_all_pets(current_user):
    # Query all pet rows from database.
    all_pets = Pet.query.all()

    # Convert all adoptable pets to JSON-friendly object array as server output.
    adoptable_pets = [pet.to_dict(only=("id", "name", "species")) for pet in all_pets if pet.is_adoptable is True]
    return make_response(adoptable_pets, 200)

# GET route to view individual pet by ID.
# NOTE: Requires user privileges. (Can use decorator middleware.)
@app.route("/api/pets/<int:pet_id>")
@authorization_required
def view_pet_by_id(current_user, pet_id: int):
    # Query and return pet from database that matches given ID.
    matching_pet = Pet.query.filter(Pet.id == pet_id).first()
    if not matching_pet:
        return make_response({"error": f"Pet ID `{pet_id}` not found in database."}, 404)
    return make_response(matching_pet.to_dict(only=("id", "name", "species")), 200)


#######################################################
######### ADMINISTRATOR-ONLY ROUTES FOR PETS ##########
#######################################################


# POST route to add new pet to database.
# NOTE: Requires administrative privileges. (Can use decorator middleware.)
@app.route("/api/pets", methods=["POST"])
@authorization_required(methods=["POST"])
def add_pet(current_user):
    # Extract JSONified payload from request.
    payload = request.get_json()

    # Unpack payload attributes to new pet object.
    new_pet = Pet(
        name=payload["name"], 
        species=payload["species"],
        is_adoptable=True
    )

    # Add and commit new pet to database.
    db.session.add(new_pet)
    db.session.commit()
    return make_response(new_pet.to_dict(only=("id", "name", "species")), 201)

# PATCH route to edit pet's information in database.
# NOTE: Requires administrative privileges. (Can use decorator middleware.)
@app.route("/api/pets/<int:pet_id>", methods=["PATCH"])
@authorization_required(methods=["PATCH"])
def update_pet(current_user, pet_id: int):
    # Query pet from database that matches given ID.
    matching_pet = Pet.query.filter(Pet.id == pet_id).first()
    if not matching_pet:
        return make_response({"error": f"Pet ID `{pet_id}` not found in database."}, 404)
    
    # Extract JSONified payload from request.
    payload = request.get_json()

    # Iteratively update relevant pet attributes using payload data.
    for attribute in payload:
        setattr(matching_pet, attribute, payload[attribute])

    # Add and commit updated pet to database.
    db.session.add(matching_pet)
    db.session.commit()
    return make_response(matching_pet.to_dict(only=("id", "name", "species")), 200)

# DELETE route to remove pet from database.
# NOTE: Requires administrative privileges. (Can use decorator middleware.)
@app.route("/api/pets/<int:pet_id>", methods=["DELETE"])
@authorization_required(methods=["DELETE"])
def remove_pet(current_user, pet_id: int):
    # Query pet from database that matches given ID.
    matching_pet = Pet.query.filter(Pet.id == pet_id).first()
    if not matching_pet:
        return make_response({"error": f"Pet ID `{pet_id}` not found in database."}, 404)
    
    # Remove and commit pet from database.
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
        # Retrieve POST request as JSONified payload.
        payload = request.get_json()

        # Extract email, username, and password from payload.
        email = payload["email"]
        username = payload["username"]
        password = payload["password"]

        # Check if user with email already exists in database. (They shouldn't!)
        preexisting_user = User.query.filter(User.email == email).first()
        if not preexisting_user:
            # Generate salt for strenghening password encryption.
            # NOTE: Salts add additional random bits to passwords prior to encryption.
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt=salt)

            # Create new user instance using email, username, and hashed password.
            new_user = User(
                email=email,
                username=username,
                password=hashed_password.decode("utf-8")
            )

            if new_user is not None:
                # Add and commit newly created user to database.
                db.session.add(new_user)
                db.session.commit()

                return make_response(new_user.to_dict(only=("id", "username", "created_at")), 201)
            else:
                return make_response({"error": "Invalid user credentials. Try again."}, 401)
        else:
            return make_response({"error": "User already exists in database."}, 401)
    else:
        return make_response({"error": f"Invalid request type. (Expected POST; received {request.method}.)"}, 400)
    
# POST route to authenticate user in database using JWT credentials.
@app.route("/login", methods=["POST"])
def user_login():
    if request.method == "POST":
        # Retrieve POST request as JSONified payload.
        payload = request.get_json()

        # Filter database by unique email to find matching user to potentially login.
        matching_user = User.query.filter(User.email == payload["email"]).first()

        # Check submitted password against hashed password in database for authentication.
        AUTHENTICATION_IS_SUCCESSFUL = bcrypt.checkpw(
            password=payload["password"].encode("utf-8"),
            hashed_password=matching_user.password.encode("utf-8")
        )

        if matching_user is not None and AUTHENTICATION_IS_SUCCESSFUL:
            # Generate expiration time as 30-minute window from current timewise execution.
            pending_expiration = datetime.utcnow() + timedelta(minutes=30)

            # Create JSON web token using user ID, expiration, and application secret key with HMAC/SHA-256 encryption algorithm.
            authorization_token = jwt.encode(
                payload={"id": matching_user.id, "exp": pending_expiration}, 
                key=app.config["SECRET_KEY"],
                algorithm="HS256")

            # Return requested data with pending JWT as response.
            return make_response(
                jsonify({
                    "user": matching_user.to_dict(only=("id", "username", "email", "created_at")),
                    "token": authorization_token
                }), 201)
        else:
            return make_response({"error": "Invalid user credentials. Try again."}, 401)
    else:
        return make_response({"error": f"Invalid request type. (Expected POST; received {request.method}.)"}, 400)
    
# DELETE route to remove JWT-authorized credentials for logged user.
# NOTE: Logouts are not viable with JWT-authorized credentials due to the expiration-dependent nature of JWTs.
@app.route("/logout", methods=["DELETE"])
def user_logout():
    return make_response({"warning": "Logout is not allowed for JWT authentication protocols. You must wait for the JWT to expire or blacklist it from the server."}, 200)
        

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