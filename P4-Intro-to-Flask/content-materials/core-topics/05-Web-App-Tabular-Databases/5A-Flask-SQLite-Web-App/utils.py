"""
FILENAME:       `utils.py`
TITLE:          Flask REST API integrated with SQLite3.
AUTHOR:         Aakash 'Kash' Sudhakar
DESCRIPTION:    A tutorial mini-project on setting up backend servers
                that handle RESTful API calls via HTTP requests and store,
                modify, and query data via tabular SQLite3 databases. 
USAGE:          Imports automatically into `app.py`. 
"""


################################################################################
#### IMPORTATIONS AND INITIALIZATIONS FOR SERVER DEVELOPMENT IN FLASK & SQL ####
################################################################################


import sqlite3

MOB_FEATURES = ["mob_id", "name", "hit_points", "damage", "speed", "is_hostile"]


################################################################################
############### DEFINE DATABASE CONNECTION AND LOADING FUNCTIONS ###############
################################################################################


def connect_to_database():
    # Connect to database.
    connection = sqlite3.connect("mobs.db")
    return connection

def create_data_table():
    try:
        # Connect to database.
        connection = connect_to_database()

        # Create database query in SQL for deleting preexisting data.
        print(">> Dropping mob data...")
        TABLE_DELETION_QUERY = """DROP TABLE IF EXISTS mobs"""

        # Execute database deletion query using SQL connection.
        connection.execute(TABLE_DELETION_QUERY)
        print(">> Mobs dataset dropped.")

        # Create database query in SQL for manually creating new data.
        print(">> Creating new mobs table...")
        TABLE_CREATION_QUERY = """
            CREATE TABLE mobs (
                mob_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name TEXT NOT NULL,
                hit_points INTEGER NOT NULL,
                damage INTEGER NOT NULL,
                speed TEXT NOT NULL,
                is_hostile BOOLEAN NOT NULL
            );
        """

        # Execute database population query using SQL connection.
        connection.execute(TABLE_CREATION_QUERY)

        # Commit all executed queries to SQL database for migration.
        connection.commit()
        print(">> Mobs table created successfully.")
    except:
        print(">> Failed to create mobs table.")
    finally:
        # Close connection to SQL database.
        connection.close()


################################################################################
################### DATABASE PROCESSING FUNCTION DEFINITIONS ###################
################################################################################


def get_mobs():
    all_mobs = []
    try:
        connection = connect_to_database()
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        FULL_SELECTION_QUERY = """SELECT * FROM mobs"""
        cursor.execute(FULL_SELECTION_QUERY)
        rows = cursor.fetchall()

        for row in rows:
            mob = {}
            for key in MOB_FEATURES:
                mob[key] = row[key]
            all_mobs.append(mob)
    except:
        all_mobs = []
    return all_mobs

def get_mob_by_id(mob_id: int):
    identified_mob = {}
    try:
        connection = connect_to_database()
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        SELECTION_BY_ID_QUERY = """SELECT * FROM mobs WHERE mob_id = ?"""
        SELECTION_BY_ID_DATA = (mob_id,)
        cursor.execute(SELECTION_BY_ID_QUERY, SELECTION_BY_ID_DATA)
        row = cursor.fetchone()

        for key in MOB_FEATURES:
            identified_mob[key] = row[key]
    except:
        identified_mob = {}
    return identified_mob

def create_mob(mob: dict):
    created_mob = {}
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        CREATION_QUERY = """
            INSERT INTO mobs (name, hit_points, damage, speed, is_hostile) 
            VALUES (?, ?, ?, ?, ?)
        """
        CREATION_DATA = tuple(mob[key] for key in MOB_FEATURES if key != "mob_id")
        cursor.execute(CREATION_QUERY, CREATION_DATA)

        connection.commit()
        created_mob = get_mob_by_id(cursor.lastrowid)
    except:
        connection().rollback()
    finally:
        connection.close()
    return created_mob

def update_mob(mob_id: int, new_mob_info: dict):
    updated_mob, original_mob = {}, get_mob_by_id(mob_id)
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        UPDATE_QUERY = """
            UPDATE mobs SET name = ?, hit_points = ?, damage = ?, speed = ?, is_hostile = ? 
            WHERE mob_id = ?
        """


        UPDATE_DATA = []

        for key in MOB_FEATURES:
            if key != "mob_id":
                if key in new_mob_info:
                    UPDATE_DATA.append(new_mob_info[key])
                else:
                    UPDATE_DATA.append(original_mob[key])

        UPDATE_DATA = tuple(UPDATE_DATA) + (mob_id,)


        cursor.execute(UPDATE_QUERY, UPDATE_DATA)

        connection.commit()
        updated_mob = get_mob_by_id(mob_id)
    except:
        connection.rollback()
        updated_mob = {}
    return updated_mob

def delete_mob(mob_id: int):
    deleted_mob = {}
    try:
        connection = connect_to_database()
        
        DELETION_QUERY = """DELETE from mobs WHERE mob_id = ?"""
        DELETION_DATA = (mob_id,)
        deleted_mob = get_mob_by_id(mob_id)
        connection.execute(DELETION_QUERY, DELETION_DATA)
        connection.commit()
    except:
        connection.rollback()
        deleted_mob = {}
    finally:
        connection.close()
    return deleted_mob