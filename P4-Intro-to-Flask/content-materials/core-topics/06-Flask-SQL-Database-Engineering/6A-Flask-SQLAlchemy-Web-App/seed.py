"""
FILENAME:       `seed.py`
TITLE:          Flask REST API integrated with SQLite3 and SQLAlchemy.
AUTHOR:         Aakash 'Kash' Sudhakar
DESCRIPTION:    A tutorial mini-project on setting up backend servers
                that handle RESTful API calls via HTTP requests and store,
                modify, and query data via tabular SQLite3 databases extended
                with SQL-Alchemy for additional functionalities, validations,
                security, and authentication. 
USAGE:          Run with `python(3) seed.py` to reset and populate 
                SQLAlchemy database with dummy data.
"""


################################################################################
### IMPORTATIONS AND INITIALIZATIONS FOR DEVELOPING FLASK-SQLALCHEMY SERVERS ###
################################################################################


from app import app
from models import db, Mob


################################################################################
################# DATABASE SEEDING AND REGENERATIVE POPULATION #################
################################################################################


print(">> Seeding... starting...")

with app.app_context():
    print(">> Deleting data...")

    Mob.query.delete()

    print(">> Creating new mobs...")

    ZombieMob = Mob(name="Zombie", hit_points=20, damage=2, speed=1, is_hostile=True)
    VillagerMob = Mob(name="Villager", hit_points=30, damage=1, speed=1, is_hostile=False)
    EndermanMob = Mob(name="Enderman", hit_points=40, damage=4, speed=2, is_hostile=False)
    CaveSpiderMob = Mob(name="Cave Spider", hit_points=12, damage=2, speed=2, is_hostile=True)
    BlazeMob = Mob(name="Blaze", hit_points=8, damage=3, speed=1, is_hostile=True)
    IronGolemMob = Mob(name="Iron Golem", hit_points=50, damage=6, speed=1, is_hostile=False)

    mobs = [ZombieMob, VillagerMob, EndermanMob, CaveSpiderMob, BlazeMob, IronGolemMob]

    print(">> Adding mobs to database...")

    db.session.add_all(mobs)

    db.session.commit()

    print(">> Seeding... done.")