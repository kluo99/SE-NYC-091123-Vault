from config import db, app
from models import User
import bcrypt

def create_users():
    def encrypt_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt=salt)
        return hashed_password.decode("utf-8")
    user_1 = User(username="friendly_neighborhood_user", password=encrypt_password("hunter2"))
    user_2 = User(username="into_the_userverse", password=encrypt_password("drowssap"))
    user_3 = User(username="amazing_administrator", password=encrypt_password("abc123"))
    return [user_1, user_2, user_3]

with app.app_context():
    print(">> Seeding data...")

    print("\n\t>> Deleting preexisting table data...")
    User.query.delete()
    db.session.commit()
    print("\t>> Data deletion successful.")

    print("\n\t>> Generating sample data for users with cryptographic hashing...")
    sample_users = create_users()
    db.session.add_all(sample_users)
    db.session.commit()
    print("\t>> User data generation successful.")

    print("\n>> Data seeding complete.")