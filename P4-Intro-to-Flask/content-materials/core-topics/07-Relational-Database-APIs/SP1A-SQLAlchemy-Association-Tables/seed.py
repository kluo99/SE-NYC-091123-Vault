#######################################################
############# IMPORTS AND INITIALIZATIONS #############
#######################################################


# Tool for generating fake data.
from faker import Faker
# Database instance, both physical models, and the associator.
from models import db, Student, Course, Enrollment
# Random selection utilities.
from random import choice, randint
# Flask application connection.
from app import app


#######################################################
########## SETTING UP DATABASE CONFIGURATION ##########
#######################################################


# Initialize faker data creation tool.
fake = Faker()


#######################################################
########### DEFINING DATA SEEDING FUNCTIONS ###########
#######################################################


# Helper function to generate ten (10) fake students.
def generate_students():
    students = []
    for _ in range(10):
        fname = fake.name().split(" ")[0]
        lname = fake.name().split(" ")[1]
        students.append(
            Student(fname=fname, 
                    lname=lname, 
                    grad_year=randint(2023, 2027))
        )
    return students

# Helper function to generate ten (10) fake courses.
def generate_courses():
    courses = []
    for _ in range(10):
        word = fake.text().split(" ")[0]
        courses.append(
            Course(title=word, 
                   instructor=fake.name(), 
                   credits=choice([1, 3]))
        )
    return courses

# Helper function to generate ten (10) fake enrollments.
# NOTE: This will randomly associate each student and course 
#       uniquely with one another.
def generate_enrollments(students, courses):
    enrollments = []
    for _ in range(10):
        random_student = choice(students)
        random_course = choice(courses)
        random_term = choice(["F", "S"]) + str(randint(2023, 2024))
        enrollments.append(
            Enrollment(
                student_id=random_student.id,
                course_id=random_course.id,
                term=random_term
            )
        )
    return enrollments


#######################################################
## POPULATE TABLE WITHIN APPLICATION CONTEXT MANAGER ##
#######################################################


with app.app_context():
    print(">> Seeding data...")

    print("\n\t>> Deleting preexisting table data...")
    Student.query.delete()
    Course.query.delete()
    Enrollment.query.delete()
    db.session.commit()
    print("\t>> Data deletion successful.")

    print("\n\t>> Generating dummy data for students...")
    students = generate_students()
    db.session.add_all(students)
    db.session.commit()
    print("\t>> Student data generation successful.")

    print("\n\t>> Generating dummy data for courses...")
    courses = generate_courses()
    db.session.add_all(courses)
    db.session.commit()
    print("\t>> Course data generation successful.")

    print("\n\t>> Generating random associations for enrollments...")
    enrollments = generate_enrollments(students, courses)
    db.session.add_all(enrollments)
    db.session.commit()
    print("\t>> Enrollment association generation successful.")
    # import ipdb; ipdb.set_trace()
    print("\n>> Data seeding complete.")