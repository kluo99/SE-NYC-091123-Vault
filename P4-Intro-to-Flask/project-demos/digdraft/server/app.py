#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


from flask import make_response, jsonify, request, render_template
from flask import Flask
from models import db, Mob, Biome, Spawn

from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///digdraft.db"
migrate = Migrate(app, db)
db.init_app(app)


#######################################################
######## INITIAL SETUP ROUTES FOR APPLICATION #########
#######################################################


# GET route to access database.
@app.route("/")
def app_root():
    return {"msg": "Welcome to Digdraft!"}
    return render_template("index.html")

# GET route to access API entry point.
@app.route("/api")
def api_entry():
    return {"msg": "Successful API access."}


#######################################################
############ INITIAL SETUP ROUTES FOR MOBS ############
#######################################################


# GET route to access all mobs.
@app.get("/api/mobs")
def view_all_mobs():
    all_mobs = Mob.query.all()
    spawnable_mobs = [mob.to_dict(rules=("-spawns",)) for mob in all_mobs]
    return render_template("mobs.html", spawnable_mobs=spawnable_mobs)

# GET route to access an individual mob by ID.
@app.get("/api/mobs/<int:mob_id>")
def view_mob_by_id(mob_id: int):
    matching_mob = Mob.query.filter(Mob.id == mob_id).first()
    if not matching_mob:
        return make_response(jsonify({"error": f"Mob ID `{mob_id}` not found in database."}), 404)
    return make_response(jsonify(matching_mob.to_dict()), 200)

# POST route to add new mob to database.
@app.post("/api/mobs")
def add_mob():
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
def edit_mob(mob_id: int):
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
def remove_mob(mob_id: int):
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
def view_all_biomes():
    all_biomes = Biome.query.all()
    spawnable_biomes = [biome.to_dict(rules=("-spawns",)) for biome in all_biomes]
    return make_response(jsonify(spawnable_biomes), 200)

# GET route to access an individual biome by ID.
@app.get("/api/biomes/<int:biome_id>")
def view_biome_by_id(biome_id: int):
    matching_biome = Biome.query.filter(Biome.id == biome_id).first()
    if not matching_biome:
        return make_response(jsonify({"error": f"Biome ID `{biome_id}` not found in database."}), 404)
    return make_response(jsonify(matching_biome.to_dict()), 200)

# POST route to add new biome to database.
@app.post("/api/biomes")
def add_biome():
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
def edit_biome(biome_id: int):
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
def remove_biome(biome_id: int):
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
def spawn_mob_in_biome(mob_id: int):
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
def view_spawned_biomes_for_mob(mob_id: int):
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
def spawn_mob_from_biome(biome_id: int):
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
def view_spawned_mobs_for_biome(biome_id: int):
    matching_biome = Biome.query.filter(Biome.id == biome_id).first()
    if not matching_biome:
        return make_response(jsonify({"error": f"Biome ID `{biome_id}` not found in database."}), 404)
    spawned_mobs_for_biome = [mob.to_dict(rules=("-spawns",)) for mob in matching_biome.mobs]
    return make_response(jsonify(spawned_mobs_for_biome), 200)


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