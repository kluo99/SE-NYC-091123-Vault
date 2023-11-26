from flask import request, make_response, session
import bcrypt

from config import app, db

from models import User

@app.route("/")
def root():
    return make_response({"msg": "Application loaded successfully."}, 200)

@app.route("/api")
def api():
    authorization = authorize_user()
    if authorization.status_code == 401:
        return make_response({"error": authorization.get_json()["error"]}, 401)
    else:
        return make_response({"msg": "API access granted.", "user": authorization.get_json()}, 200)

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
    
@app.route("/logout", methods=["DELETE"])
def user_logout():
    if request.method == "DELETE":
        session["user_id"] = None
        # return make_response({"msg": "User successfully logged out."}, 200)
        return make_response({"msg": "User successfully logged out."}, 204)
    else:
        return make_response({"error": f"Invalid request type. (Expected DELETE; received {request.method}.)"}, 400)
    
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
        
if __name__ == "__main__":
    app.run(debug=True, port=5555)