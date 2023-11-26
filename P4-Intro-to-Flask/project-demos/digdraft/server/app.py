#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


from flask import make_response, jsonify, request, session
# from flask import render_template
import bcrypt

from config import app, db

from models import Player, Mob, Biome, Spawn

from middleware import authorization_required


#######################################################
######## INITIAL SETUP ROUTES FOR APPLICATION #########
#######################################################


# GET route to access database.
@app.route("/")
def app_root():
    return {"msg": "Welcome to Digdraft!", "notice": "Please log in or create an account to continue."}

# GET route to access API entry point.
@app.route("/api")
@authorization_required
def api_entry(current_player):
    return make_response({"player_id": current_player["id"], "msg": "Successful API access."}, 200)


#######################################################
############ INITIAL SETUP ROUTES FOR MOBS ############
#######################################################


# GET route to access all mobs.
@app.get("/api/mobs")
@authorization_required
def view_all_mobs(current_player):
    all_mobs = Mob.query.all()
    spawnable_mobs = [mob.to_dict(rules=("-spawns",)) for mob in all_mobs]
    return make_response(spawnable_mobs, 200)
    # return render_template("mobs.html", spawnable_mobs=spawnable_mobs)

# GET route to access an individual mob by ID.
@app.get("/api/mobs/<int:mob_id>")
@authorization_required
def view_mob_by_id(current_player, mob_id: int):
    matching_mob = Mob.query.filter(Mob.id == mob_id).first()
    if not matching_mob:
        return make_response(jsonify({"error": f"Mob ID `{mob_id}` not found in database."}), 404)
    return make_response(jsonify(matching_mob.to_dict()), 200)

# POST route to add new mob to database.
@app.post("/api/mobs")
@authorization_required
def add_mob(current_player):
    POST_REQUEST = request.get_json()
    new_mob = Mob(
        name=POST_REQUEST["name"], 
        hit_points=POST_REQUEST["hit_points"], 
        damage=POST_REQUEST["damage"],
        speed=POST_REQUEST["speed"],
        is_hostile=POST_REQUEST["is_hostile"],
        can_spawn_during_daytime=POST_REQUEST["can_spawn_during_daytime"]
    )
    db.session.add(new_mob)
    db.session.commit()
    return make_response(jsonify(new_mob.to_dict()), 201)

# PATCH route to edit a mob's information in database.
@app.patch("/api/mobs/<int:mob_id>")
@authorization_required
def edit_mob(current_player, mob_id: int):
    matching_mob = Mob.query.filter(Mob.id == mob_id).first()
    if not matching_mob:
        return make_response(jsonify({"error": f"Mob ID `{mob_id}` not found in database."}), 404)
    PATCH_REQUEST = request.get_json()
    for attribute in PATCH_REQUEST:
        setattr(matching_mob, attribute, PATCH_REQUEST[attribute])
    db.session.add(matching_mob)
    db.session.commit()
    return make_response(jsonify(matching_mob.to_dict()), 200)

# DELETE route to remove a mob from the database.
@app.delete("/api/mobs/<int:mob_id>")
@authorization_required
def remove_mob(current_player, mob_id: int):
    matching_mob = Mob.query.filter(Mob.id == mob_id).first()
    if not matching_mob:
        return make_response(jsonify({"error": f"Mob ID `{mob_id}` not found in database."}), 404)
    db.session.delete(matching_mob)
    db.session.commit()
    return make_response(jsonify(matching_mob.to_dict()), 200)


#######################################################
########### INITIAL SETUP ROUTES FOR BIOMES ###########
#######################################################


# GET route to access biomes.
@app.get("/api/biomes")
@authorization_required
def view_all_biomes(current_player):
    all_biomes = Biome.query.all()
    spawnable_biomes = [biome.to_dict(rules=("-spawns",)) for biome in all_biomes]
    return make_response(jsonify(spawnable_biomes), 200)

# GET route to access an individual biome by ID.
@app.get("/api/biomes/<int:biome_id>")
@authorization_required
def view_biome_by_id(current_player, biome_id: int):
    matching_biome = Biome.query.filter(Biome.id == biome_id).first()
    if not matching_biome:
        return make_response(jsonify({"error": f"Biome ID `{biome_id}` not found in database."}), 404)
    return make_response(jsonify(matching_biome.to_dict()), 200)

# POST route to add new biome to database.
@app.post("/api/biomes")
@authorization_required
def add_biome(current_player):
    POST_REQUEST = request.get_json()
    new_biome = Biome(
        name=POST_REQUEST["name"], 
        elevation=POST_REQUEST["elevation"], 
        rarity=POST_REQUEST["rarity"],
        is_in_overworld=POST_REQUEST["is_in_overworld"],
        is_in_nether=POST_REQUEST["is_in_nether"],
        is_in_end=POST_REQUEST["is_in_end"]
    )
    db.session.add(new_biome)
    db.session.commit()
    return make_response(jsonify(new_biome.to_dict()), 201)

# PATCH route to edit a biome's information in database.
@app.patch("/api/biomes/<int:biome_id>")
@authorization_required
def edit_biome(current_player, biome_id: int):
    matching_biome = Biome.query.filter(Biome.id == biome_id).first()
    if not matching_biome:
        return make_response(jsonify({"error": f"Biome ID `{biome_id}` not found in database."}), 404)
    PATCH_REQUEST = request.get_json()
    for attribute in PATCH_REQUEST:
        setattr(matching_biome, attribute, PATCH_REQUEST[attribute])
    db.session.add(matching_biome)
    db.session.commit()
    return make_response(jsonify(matching_biome.to_dict()), 200)

# DELETE route to remove a biome from the database.
@app.delete("/api/biomes/<int:biome_id>")
@authorization_required
def remove_biome(current_player, biome_id: int):
    matching_biome = Biome.query.filter(Biome.id == biome_id).first()
    if not matching_biome:
        return make_response(jsonify({"error": f"Biome ID `{biome_id}` not found in database."}), 404)
    db.session.delete(matching_biome)
    db.session.commit()
    return make_response(jsonify(matching_biome.to_dict()), 200)


#######################################################
############ ASSOCIATION METHODS FOR MOBS #############
#######################################################


# POST route to add a biome to a mob's currently spawned biomes (list).
@app.post("/api/mobs/<int:mob_id>/spawns")
@authorization_required
def spawn_mob_in_biome(current_player, mob_id: int):
    # 1. Find the mob that matches the given ID from the URL/route.
    matching_mob = Mob.query.filter(Mob.id == mob_id).first()
    # 2. Find the biome that matches the given ID from the request. 
    # NOTE: The request will be neither a `Mob()` nor a `Biome()`. 
    #       It will be a `Spawn()` with IDs for a mob and a biome.
    POST_REQUEST = request.get_json()
    biome_id, hour_spawned = POST_REQUEST["biome_id"], POST_REQUEST["hour_spawned"]
    matching_biome = Biome.query.filter(Biome.id == biome_id).first()
    # NOTE: It's helpful to validate our matching objects before attempting to manipulate SQL tables.
    if not matching_mob:
        return make_response(jsonify({"error": f"Mob ID `{mob_id}` not found in database."}), 404)
    if not matching_biome:
        return make_response(jsonify({"error": f"Biome ID `{biome_id}` not found in database."}), 404)
    # 3. Link our matching mob and biome using a third object: `Spawn`. 
    new_spawn = Spawn(mob_id=matching_mob.id, 
                      biome_id=matching_biome.id,
                      hour_spawned=hour_spawned)
    # 4. Stage and commit changes to our database.
    db.session.add(new_spawn)
    db.session.commit()
    # 5. Return acceptable value to frontend/API.
    # NOTE: Must give additional serialization rules to stop cascading 
    #       after showing a mob's spawned biomes.
    return make_response(jsonify(new_spawn.to_dict(rules=("-mob",))), 201)

# GET route to view all spawned biomes for a current mob.
@app.get("/api/mobs/<int:mob_id>/biomes")
@authorization_required
def view_spawned_biomes_for_mob(current_player, mob_id: int):
    matching_mob = Mob.query.filter(Mob.id == mob_id).first()
    if not matching_mob:
        return make_response(jsonify({"error": f"Mob ID `{mob_id}` not found in database."}), 404)
    spawned_biomes_for_mob = [biome.to_dict(rules=("-spawns",)) for biome in matching_mob.biomes]
    return make_response(jsonify(spawned_biomes_for_mob), 200)


#######################################################
########### ASSOCIATION METHODS FOR BIOMES ############
#######################################################


# POST route to add a mob to a biome's currently spawned mobs (list).
@app.post("/api/biomes/<int:biome_id>/spawns")
@authorization_required
def spawn_mob_from_biome(current_player, biome_id: int):
    # 1. Find the biome that matches the given ID from the URL/route.
    matching_biome = Biome.query.filter(Biome.id == biome_id).first()
    # 2. Find the mob that matches the given ID from the request. 
    # NOTE: My request will be neither a `Biome()` nor a `Mob()`. 
    #       It will be a `Spawn()` with IDs for a biome and a mob.
    POST_REQUEST = request.get_json()
    mob_id, hour_spawned = POST_REQUEST["mob_id"], POST_REQUEST["hours_spawned"]
    matching_mob = Mob.query.filter(Mob.id == mob_id).first()
    # NOTE: It's helpful to validate our matching objects before attempting to manipulate SQL tables.
    if not matching_biome:
        return make_response(jsonify({"error": f"Biome ID `{biome_id}` not found in database."}), 404)
    if not matching_mob:
        return make_response(jsonify({"error": f"Mob ID `{mob_id}` not found in database."}), 404)
    # 3. Link our matching biome and mob using an association table: `Spawn`. 
    new_spawn = Spawn(biome_id=matching_biome.id,
                      mob_id=matching_mob.id, 
                      hour_spawned=hour_spawned)
    # 4. Stage and commit changes to our database.
    db.session.add(new_spawn)
    db.session.commit()
    # 5. Return acceptable value to frontend/API.
    # NOTE: Must give additional serialization rules to stop cascading 
    #       after showing a biome's spawned mobs.
    return make_response(jsonify(new_spawn.to_dict(rules=("-biome",))), 201)

# GET route to view all spawned mobs for a current biome.
@app.get("/api/biomes/<int:biome_id>/mobs")
@authorization_required
def view_spawned_mobs_for_biome(current_player, biome_id: int):
    matching_biome = Biome.query.filter(Biome.id == biome_id).first()
    if not matching_biome:
        return make_response(jsonify({"error": f"Biome ID `{biome_id}` not found in database."}), 404)
    spawned_mobs_for_biome = [mob.to_dict(rules=("-spawns",)) for mob in matching_biome.mobs]
    return make_response(jsonify(spawned_mobs_for_biome), 200)


#######################################################
############ PLAYER AUTHENTICATION ROUTING ############
#######################################################


# POST route to create new user/player within database.
@app.route("/players", methods=["POST"])
def add_player():
    if request.method == "POST":
        payload = request.get_json()

        username = payload["username"]
        password = payload["password"]

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt=salt)

        new_player = Player(
            username=username,
            password=hashed_password.decode("utf-8")
        )

        if new_player is not None:
            db.session.add(new_player)
            db.session.commit()
            session["player_id"] = new_player.id
            return make_response(
                new_player.to_dict(only=("id", "kills", "deaths", "experience", "username", "created_at")), 
                201
            )
        else:
            return make_response({"error": "Invalid username or password. Try again."}, 401)
    else:
        return make_response({"error": f"Invalid request type. (Expected POST; received {request.method}.)"}, 400)
    
# POST route to authenticate player credentials.
@app.route("/players/login", methods=["POST"])
def player_login():
    if request.method == "POST":
        payload = request.get_json()

        matching_player = Player.query.filter(Player.username.like(f"%{payload['username']}%")).first()

        AUTHENTICATION_IS_SUCCESSFUL = bcrypt.checkpw(
            password=payload["password"].encode("utf-8"),
            hashed_password=matching_player.password.encode("utf-8")
        )

        if matching_player is not None and AUTHENTICATION_IS_SUCCESSFUL:
            session["player_id"] = matching_player.id
            return make_response(
                matching_player.to_dict(only=("id", "kills", "deaths", "experience", "username", "created_at")), 
                200
            )
        else:
            return make_response({"error": "Invalid username or password. Try again."}, 401)
    else:
        return make_response({"error": f"Invalid request type. (Expected POST; received {request.method}.)"}, 400)
    
# DELETE route to clear player credentials from server session.
@app.route("/players/logout", methods=["DELETE"])
def player_logout():
    if request.method == "DELETE":
        session["player_id"] = None
        return make_response({"msg": "Player successfully logged out."}, 204)
    else:
        return make_response({"error": f"Invalid request type. (Expected DELETE; received {request.method}.)"}, 400)


#######################################################
############# PLAYER AUTHORIZATION ROUTING ############
#######################################################

# GET route to authorize another view with existing player credentials.
@app.route("/authorize", methods=["GET"])
def authorize_player():
    player_id = session.get("player_id")

    if not player_id:
        return make_response({"error": "Player account not authenticated. Please log in or sign up to continue using the application."}, 401)
    else:
        matching_player = Player.query.filter(Player.id == player_id).first()
        if matching_player is not None:
            return make_response(
                matching_player.to_dict(only=("id", "username", "created_at")), 
                200
            )
        else:
            return make_response({"error": "Invalid username or password. Try again."}, 401)
        

#######################################################
############## ADDITIONAL ERROR HANDLING ##############
#######################################################


# General GET route for 404 error handling.
@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({"error": "Page not found."}), 404)


#######################################################
######### FLASK BOILERPLATE FOR EXECUTION #############
#######################################################


if __name__ == "__main__":
    app.run(port=5555, debug=True)