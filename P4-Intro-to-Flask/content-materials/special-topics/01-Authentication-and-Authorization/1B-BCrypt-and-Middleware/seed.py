from config import db, app
from models import User, Pet
import bcrypt

def create_users():
    def encrypt_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt=salt)
        return hashed_password.decode("utf-8")
    user_1 = User(username="friendly_neighborhood_user", password=encrypt_password("hunter2"))
    user_2 = User(username="into_the_userverse", password=encrypt_password("drowssap"))
    user_3 = User(username="amazing_administrator", password=encrypt_password("abcde12345"), is_admin=True)
    return [user_1, user_2, user_3]

def create_pets():
    pet_1 = Pet(name="Garfield", species="Cat")
    pet_2 = Pet(name="Nermal", species="Cat")
    pet_3 = Pet(name="Odie", species="Dog")
    pet_4 = Pet(name="Benji", species="Dog", is_adoptable=False)
    pet_5 = Pet(name="Bablu", species="Dog", is_adoptable=False)
    return [pet_1, pet_2, pet_3, pet_4, pet_5]

with app.app_context():
    print(">> Seeding data...")

    print("\n\t>> Deleting preexisting table data...")
    User.query.delete()
    Pet.query.delete()
    db.session.commit()
    print("\t>> Data deletion successful.")

    print("\n\t>> Generating sample data for users with cryptographic hashing...")
    sample_users = create_users()
    db.session.add_all(sample_users)
    db.session.commit()
    print("\t>> User data generation successful.")

    print("\n\t>> Generating sample data for pets...")
    sample_pets = create_pets()
    db.session.add_all(sample_pets)
    db.session.commit()
    print("\t>> Pet data generation successful.")

    print("\n>> Data seeding complete.")