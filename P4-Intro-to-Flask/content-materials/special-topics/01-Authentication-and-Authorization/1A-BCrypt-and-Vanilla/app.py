#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


# Flask server request-response and session storage utilities.
from flask import request, make_response, session
# Configured application/server and database instances.
from config import app, db
# Relative access to user model.
from models import User

# Cryptographic hashing tools for user authentication.
import bcrypt


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
def api():
    authorization = authorize_user()
    if authorization.status_code == 401:
        return make_response({"error": authorization.get_json()["error"]}, 401)
    else:
        return make_response({"msg": "API access granted.", "user": authorization.get_json()}, 200)


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
            return make_response(
                {
                    "msg": "User successfully logged in.", 
                    "user": matching_user.to_dict(only=("id", "username", "created_at"))
                }, 200)
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
############## USER AUTHORIZATION ROUTING #############
#######################################################


# GET route to grant post-login user authorization(s) across application routes.
@app.route("/authorize")
def authorize_user():
    user_id = session.get("user_id")

    if not user_id:
        return make_response({"error": "User account not authenticated. Please log in or sign up to continue using the application."}, 401)
    else:
        matching_user = User.query.filter(User.id == user_id).first()
        if matching_user is not None:
            return make_response(matching_user.to_dict(only=("id", "username", "created_at")), 200)
        else:
            return make_response({"error": "Invalid username or password. Try again."}, 401)
        

#######################################################
################ GLOBAL ERROR HANDLING ################
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