#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


# Flask server request-response utilities.
from flask import make_response, request
# Configured application/server instance.
from config import app
# Relative access to user model.
from models import User

# Tools for working with JSON web tokens.
# NOTE: To be used for JWT construction and encoding/decoding.
import jwt

# Additional tools for extending decorator function logic.
from functools import partial, wraps


#######################################################
###### EXPORTABLE MIDDLEWARE UTILITY FUNCTION(S) ######
#######################################################


def authorization_required(func=None, methods=["GET"]):
    # Applied operations to handle optional `methods` argument for decorator.
    if func is None:
        return partial(authorization_required, methods=methods)
    
    # Factory function to tether wrapper to decorator.
    @wraps(func)

    # Inner authorization function.
    def decorated_authorizer(*args, **kwargs):
        # Preset empty authorization token for handling request header errors.
        authorization_token = None

        # Check if JWT is provided in latest request (within headers). (Extract it if provided.)
        if "x-access-token" in request.headers:
            authorization_token = request.headers["x-access-token"]
        if not authorization_token:
            return make_response({"error": "Missing authentication token."}, 401)
        
        try:
            # Decode JWT using application secret key and HMAC/SHA-256 decryption algorithm.
            decoded_payload = jwt.decode(
                jwt=authorization_token, 
                key=app.config["SECRET_KEY"],
                algorithms=["HS256"])
            
            # Query users from database where authorized user exists (has matching ID).
            authorized_user = User.query.filter(User.id == decoded_payload["id"]).first()
            if authorized_user is None:
                return make_response({"error": "Invalid credentials. Try again."}, 401)
            
            # Define methods authorized only for administrative access.
            UNAUTHORIZED_METHODS = ["POST", "PATCH", "DELETE"]
            # Check if any decorator-submitted methods are unauthorized to non-administrative users.
            if any(method in methods for method in UNAUTHORIZED_METHODS):
                # If so, check if currently authorized user is an administrator.
                if not authorized_user.is_administrator():
                    # If not, return an error response due to unauthorized access.
                    return make_response({"error": "Administrative permissions are required to access this part of the application."}, 401)
        except Exception as error:
            return make_response({"error": f"Something went wrong.", "details": str(error)}, 500)

        # Invoke wrapped view function with administrative access as output.
        return func(authorized_user.to_dict(), *args, **kwargs)
    return decorated_authorizer