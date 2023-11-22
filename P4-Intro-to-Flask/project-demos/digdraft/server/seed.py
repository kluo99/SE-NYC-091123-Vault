#######################################################
############# IMPORTS AND INITIALIZATIONS #############
#######################################################


# Database instance, both physical models, and the associator.
from models import db, Mob, Biome, Spawn
# Flask application connection.
from app import app


#######################################################
########### DEFINING DATA SEEDING FUNCTIONS ###########
#######################################################


# Helper function to curate ten (10) sample mobs.
def create_sample_mobs():
    zombie = Mob(name="Zombie", hit_points=10, damage=1, speed=1, is_hostile=True, can_spawn_during_daytime=False)
    polar_bear = Mob(name="Polar Bear", hit_points=40, damage=4, speed=2, is_hostile=False, can_spawn_during_daytime=True)
    enderman = Mob(name="Enderman", hit_points=25, damage=5, speed=2, is_hostile=False, can_spawn_during_daytime=True)
    silverfish = Mob(name="Silverfish", hit_points=8, damage=1, speed=1, is_hostile=True, can_spawn_during_daytime=True)
    iron_golem = Mob(name="Iron Golem", hit_points=50, damage=7, speed=1, is_hostile=False, can_spawn_during_daytime=True)
    blaze = Mob(name="Blaze", hit_points=12, damage=2, speed=1, is_hostile=True, can_spawn_during_daytime=True)
    chicken = Mob(name="Chicken", hit_points=4, damage=0, speed=1, is_hostile=False, can_spawn_during_daytime=True)
    skeleton_archer = Mob(name="Skeleton Archer", hit_points=15, damage=2, speed=1, is_hostile=True, can_spawn_during_daytime=False)
    warden = Mob(name="Warden", hit_points=200, damage=8, speed=2, is_hostile=True, can_spawn_during_daytime=True)
    ender_dragon = Mob(name="Ender Dragon", hit_points=250, damage=8, speed=5, is_hostile=True, can_spawn_during_daytime=True)
    return [zombie, polar_bear, enderman, silverfish, iron_golem, blaze, chicken, skeleton_archer, warden, ender_dragon]

# Helper function to curate ten (10) sample biomes.
def create_sample_biomes():
    caves = Biome(name="Caves", elevation="base", rarity="common", is_in_overworld=True, is_in_nether=False, is_in_end=False)
    tundra = Biome(name="Tundra", elevation="base", rarity="uncommon", is_in_overworld=True, is_in_nether=False, is_in_end=False)
    mountains = Biome(name="Mountains", elevation="high", rarity="common", is_in_overworld=True, is_in_nether=False, is_in_end=False)
    stronghold = Biome(name="Stronghold", elevation="low", rarity="rare", is_in_overworld=True, is_in_nether=False, is_in_end=False)
    village = Biome(name="Village", elevation="base", rarity="common", is_in_overworld=True, is_in_nether=False, is_in_end=False)
    nether_fortress = Biome(name="Nether Fortress", elevation="low", rarity="rare", is_in_overworld=False, is_in_nether=True, is_in_end=False)
    plains = Biome(name="Plains", elevation="base", rarity="common", is_in_overworld=True, is_in_nether=False, is_in_end=False)
    forest = Biome(name="Forest", elevation="base", rarity="common", is_in_overworld=True, is_in_nether=False, is_in_end=False)
    skulk = Biome(name="Skulk", elevation="low", rarity="rare", is_in_overworld=True, is_in_nether=False, is_in_end=False)
    the_end = Biome(name="The End", elevation="low", rarity="very rare", is_in_overworld=False, is_in_nether=False, is_in_end=True)
    return [caves, tundra, mountains, stronghold, village, nether_fortress, plains, forest, skulk, the_end]

# Helper function to curate ten (10) sample spawns.
# NOTE: This will sequentially associate each mob and biome 
#       uniquely with one another.
def create_sample_spawns(sample_mobs, sample_biomes):
    sample_spawns, spawn_hours = [], [2, 14, 22, 7, 5, 12, 14, 23, 11, 0]
    for position in range(len(sample_mobs)):
        sample_spawns.append(Spawn(
            mob_id=sample_mobs[position].id,
            biome_id=sample_biomes[position].id,
            hour_spawned=spawn_hours[position]
        ))
    return sample_spawns


#######################################################
## POPULATE TABLE WITHIN APPLICATION CONTEXT MANAGER ##
#######################################################


with app.app_context():
    print(">> Seeding data...")

    print("\n\t>> Deleting preexisting table data...")
    Mob.query.delete()
    Biome.query.delete()
    Spawn.query.delete()
    db.session.commit()
    print("\t>> Data deletion successful.")

    print("\n\t>> Generating sample data for mobs...")
    sample_mobs = create_sample_mobs()
    db.session.add_all(sample_mobs)
    db.session.commit()
    print("\t>> Mob data generation successful.")

    print("\n\t>> Generating sample data for biomes...")
    sample_biomes = create_sample_biomes()
    db.session.add_all(sample_biomes)
    db.session.commit()
    print("\t>> Biome data generation successful.")

    print("\n\t>> Generating random associations (spawns) between mobs and biomes...")
    sample_spawns = create_sample_spawns(sample_mobs=sample_mobs, sample_biomes=sample_biomes)
    db.session.add_all(sample_spawns)
    db.session.commit()
    print("\t>> Spawn association generation successful.")

    print("\n>> Data seeding complete.")