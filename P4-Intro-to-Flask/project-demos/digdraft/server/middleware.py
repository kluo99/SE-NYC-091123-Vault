from flask import make_response, session

from functools import wraps

from config import app

from models import Player

def authorization_required(func):
    @wraps(func)
    def decorated_authorizer(*args, **kwargs):
        player_id = session.get("player_id")
        if not player_id:
            return make_response({"error": "Player account not authenticated. Please log in or sign up to continue using the application."}, 401)
        try:
            authorized_player = Player.query.filter(Player.id == player_id).first()
            if authorized_player is None:
                return make_response({"error": "Invalid username or password. Try again."}, 401)
        except Exception as error:
            return make_response({"error": f"Something went wrong. EXCEPTION: {str(error)}."}, 500)

        return func(authorized_player.to_dict(), *args, **kwargs)
    return decorated_authorizer