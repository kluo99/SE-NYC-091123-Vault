#######################################################
############# IMPORTS AND INITIALIZATIONS #############
#######################################################


from config import db

from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy


#######################################################
######### SETTING UP DATABASE OBJECT MODELS ###########
#######################################################


"""
There are three major steps to giving life to our association table.
(With an important preliminary step.)

0.  Ensure stability of our previously constructed physical objects.
        0a. Set up the table name and columns of the `Mob` database object model.
        0b. Set up the table name and columns of the `Biome` database object model.
        0c. Set up the table name and columns of the `Spawn` associative object model.
1.  Connect an individual physical object to the association table.
        1a. Construct a new relationship from mobs to spawns. 
                [`Mob` <-> `Spawn`]
        1b. Close the new relationship from spawns back to mobs. 
                [`Spawn` <-> `Mob`]
        1c. Construct a new relationship from biomes to spawns. 
                [`Biome` <-> `Spawn`]
        1d. Close the new relationship from spawns back to biomes. 
                [`Spawn` <-> `Biome`]
2.  Link the associations to the OTHER physical object.
        2a. Construct an association proxy that links the mob-spawn relationship 
            to the biome-spawn relationship. 
                [(`Mob` <-> `Spawn`) <---> (`Biome` <-> `Spawn`)]
        2b. Construct an association proxy that links the biome-spawn relationship 
            to the mob-spawn relationship.
                [(`Biome` <-> `Spawn`) <---> (`Mob` <-> `Spawn`)]
3.  Instruct our program(s) at every chance we get (both in `models` and `app`) 
    to not infinitely recurse/cascade when accessing nested data, using a technique
    called "serialization rules".
        3a. Design serialization rules for the mob table to avoid cascading when
            accessing mob data via spawn table traversal.
        3b. Design serialization rules for the biome table to avoid cascading when
            accessing biome data via spawn table traversal.
        3c. Design serialization rules for the spawn table to avoid cascading when
            accessing spawn data from the mob table.
        3d. Design serialization rules for the spawn table to avoid cascading when
            accessing spawn data from the biome table.
"""

# Setting up database model for a mob.
# NOTE: This needs to be subclassed with two superclasses:
#   -> `db.Model` for SQL-like database structuring.
#   -> `SerializerMixin` for data serialization and avoiding infinite referencing.
class Mob(db.Model, SerializerMixin):
    # 0a. Set up the name of SQL database table containing mob data.
    __tablename__ = "mob_table"
    # 0a. Set up physical object columns prior to interdependent association(s).
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    hit_points = db.Column(db.Integer)
    damage = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    is_hostile = db.Column(db.Boolean)
    can_spawn_during_daytime = db.Column(db.Boolean)

    # 1a. Create a relationship that links a mob row to a spawn row.  
    # NOTE: This relationship needs to be closed back to the mob-spawn relationship. 
    spawns = db.relationship("Spawn", back_populates="mob")

    # 2a. Creates an association proxy from the mob-spawn relationship to the biome-spawn relationship.
    biomes = association_proxy("spawns", "biome")

    # 3a. Creates serialization rules to avoid cascading when accessing mob data from a spawn.
    serialize_rules = ("-spawns.mob",)


# Setting up database model for a biome.
# NOTE: This needs to be subclassed with two superclasses:
#   -> `db.Model` for SQL-like database structuring.
#   -> `SerializerMixin` for data serialization and avoiding infinite referencing.
class Biome(db.Model, SerializerMixin):
    # 0b. Set up the name of SQL database table containing biome data.
    __tablename__ = "biome_table"
    # 0b. Set up physical object columns prior to interdependent association(s).
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    elevation = db.Column(db.String(20))
    rarity = db.Column(db.String(20))
    is_in_overworld = db.Column(db.Boolean)
    is_in_nether = db.Column(db.Boolean)
    is_in_end = db.Column(db.Boolean)

    # 1c. Create a relationship that links a biome row to a spawn row.
    # NOTE: This relationship needs to be closed back to the biome-spawn relationship.
    spawns = db.relationship("Spawn", back_populates="biome")
    
    # 2b. Creates an association proxy from the biome-spawn relationship to the mob-spawn relationship.
    mobs = association_proxy("spawns", "mob")

    # 3b. Creates serialization rules to avoid cascading when accessing biome data from a spawn.
    serialize_rules = ("-spawns.biome",)
    

# Setting up database association model for connecting a mob and a biome.
# NOTE: This needs to be subclassed with two superclasses:
#   -> `db.Model` for SQL-like database structuring.
#   -> `SerializerMixin` for data serialization and avoiding infinite referencing.
class Spawn(db.Model, SerializerMixin):
    # 0c. Set up the name of SQL database table containing spawn data.
    __tablename__ = "spawn_table"
    # 0c. Set up association object columns prior to interdependent association(s).
    id = db.Column(db.Integer, primary_key=True)
    mob_id = db.Column(db.Integer, db.ForeignKey("mob_table.id"))
    biome_id = db.Column(db.Integer, db.ForeignKey("biome_table.id"))
    hour_spawned = db.Column(db.Integer)

    # 1b. Extend the relationship from (1a) to link from a spawn row back to a mob row. 
    # NOTE: This relationship needs to be closed back to the spawn-mob relationship.
    mob = db.relationship("Mob", back_populates="spawns")
    # 1d. Extend the relationship from (1c) to link from a spawn row back to a biome row.
    # NOTE: This relationship needs to be closed back to the spawn-biome relationship.
    biome = db.relationship("Biome", back_populates="spawns")

    # 3c. Creates serialization rules to avoid cascading when accessing spawn data from a mob.
    # 3d. Creates serialization rules to avoid cascading when accessing spawn data from a biome.
    serialize_rules = ("-mob.spawns", "-biome.spawns")


class Player(db.Model, SerializerMixin):
    __tablename__ = "player_table"

    id = db.Column(db.Integer, primary_key=True)
    kills = db.Column(db.Integer, default=0, nullable=False)
    deaths = db.Column(db.Integer, default=0, nullable=False)
    experience = db.Column(db.Integer, default=1, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())