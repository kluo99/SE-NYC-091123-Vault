#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


# Flask server request-response and session storage utilities.
from flask import make_response, session
# Configured application/server instance.
from config import app
# Relative access to user model.
from models import User

# Additional tools for extending decorator function logic.
from functools import partial, wraps


#######################################################
###### EXPORTABLE MIDDLEWARE UTILITY FUNCTION(S) ######
#######################################################


def authorization_required(func=None, methods=["GET"]):
    if func is None:
        return partial(authorization_required, methods=methods)
    @wraps(func)
    def decorated_authorizer(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return make_response({"error": "User account not authenticated. Please log in or sign up to continue using the application."}, 401)
        try:
            authorized_user = User.query.filter(User.id == user_id).first()
            if authorized_user is None:
                return make_response({"error": "Invalid username or password. Try again."}, 401)
            
            UNAUTHORIZED_METHODS = ["POST", "PATCH", "DELETE"]
            if any(method in methods for method in UNAUTHORIZED_METHODS):
                if not authorized_user.is_administrator():
                    return make_response({"error": "Administrative permissions are required to access this part of the application."}, 401)
        except Exception as error:
            return make_response({"error": f"Something went wrong.", "details": str(error)}, 500)

        return func(authorized_user.to_dict(), *args, **kwargs)
    return decorated_authorizer