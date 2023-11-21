#######################################################
############# IMPORTS AND INITIALIZATIONS #############
#######################################################


from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy


#######################################################
########## SETTING UP DATABASE CONFIGURATION ##########
#######################################################


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

# Instantiate database connection using metadata schema.
db = SQLAlchemy(metadata=metadata)


#######################################################
######### SETTING UP DATABASE OBJECT MODELS ###########
#######################################################


"""
There are three major steps to giving life to our association table.
(With an important preliminary step.)

0.  Ensure stability of our previously constructed physical objects.
        0a. Set up the table name and columns of the `Student` database object model.
        0b. Set up the table name and columns of the `Course` database object model.
        0c. Set up the table name and columns of the `Enrollment` associative object model.
1.  Connect an individual physical object to the association table.
        1a. Construct a new relationship from students to enrollments. 
                [`Student` <-> `Enrollment`]
        1b. Close the new relationship from enrollments back to students. 
                [`Enrollment` <-> `Student`]
        1c. Construct a new relationship from courses to enrollments. 
                [`Course` <-> `Enrollment`]
        1d. Close the new relationship from enrollments back to courses. 
                [`Enrollment` <-> `Course`]
2.  Link the associations to the OTHER physical object.
        2a. Construct an association proxy that links the student-enrollment relationship 
            to the course-enrollment relationship. 
                [(`Student` <-> `Enrollment`) <---> (`Course` <-> `Enrollment`)]
        2b. Construct an association proxy that links the course-enrollment relationship 
            to the student-enrollment relationship.
                [(`Course` <-> `Enrollment`) <---> (`Student` <-> `Enrollment`)]
3.  Instruct our program(s) at every chance we get (both in `models` and `app`) 
    to not infinitely recurse/cascade when accessing nested data, using a technique
    called "serialization rules".
        3a. Design serialization rules for the student table to avoid cascading when
            accessing student data via enrollment table traversal.
        3b. Design serialization rules for the course table to avoid cascading when
            accessing course data via enrollment table traversal.
        3c. Design serialization rules for the enrollment table to avoid cascading when
            accessing enrollment data from the student table.
        3d. Design serialization rules for the enrollment table to avoid cascading when
            accessing enrollment data from the course table.
"""

# Setting up database model for a student.
# NOTE: This needs to be subclassed with two superclasses:
#   -> `db.Model` for SQL-like database structuring.
#   -> `SerializerMixin` for data serialization and avoiding infinite referencing.
class Student(db.Model, SerializerMixin):
    # 0a. Set up the name of SQL database table containing student data.
    __tablename__ = "student_table"
    # 0a. Set up physical object columns prior to interdependent association(s).
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    grad_year = db.Column(db.Integer)

    # 1a. Create a relationship that links a student row to an enrollment row.  
    # NOTE: This relationship needs to be closed back to the student-enrollment relationship. 
    enrollments = db.relationship("Enrollment", back_populates="student")

    # 2a. Creates an association proxy from the student-enrollment relationship to the course-enrollment relationship.
    courses = association_proxy("enrollments", "course")

    # 3a. Creates serialization rules to avoid cascading when accessing student data from an enrollment.
    serialize_rules = ("-enrollments.student",)


# Setting up database model for a course.
# NOTE: This needs to be subclassed with two superclasses:
#   -> `db.Model` for SQL-like database structuring.
#   -> `SerializerMixin` for data serialization and avoiding infinite referencing.
class Course(db.Model, SerializerMixin):
    # 0b. Set up the name of SQL database table containing course data.
    __tablename__ = "course_table"
    # 0b. Set up physical object columns prior to interdependent association(s).
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    instructor = db.Column(db.String)
    credits = db.Column(db.Integer)

    # 1c. Create a relationship that links a course row to an enrollment row.
    # NOTE: This relationship needs to be closed back to the course-enrollment relationship.
    enrollments = db.relationship("Enrollment", back_populates="course")
    
    # 2b. Creates an association proxy from the course-enrollment relationship to the student-enrollment relationship.
    students = association_proxy("enrollments", "student")

    # 3b. Creates serialization rules to avoid cascading when accessing course data from an enrollment.
    serialize_rules = ("-enrollments.course",)
    

# Setting up database association model for connecting a student and a course.
# NOTE: This needs to be subclassed with two superclasses:
#   -> `db.Model` for SQL-like database structuring.
#   -> `SerializerMixin` for data serialization and avoiding infinite referencing.
class Enrollment(db.Model, SerializerMixin):
    # 0c. Set up the name of SQL database table containing enrollment data.
    __tablename__ = "enrollment_table"
    # 0c. Set up association object columns prior to interdependent association(s).
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student_table.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course_table.id"))
    term = db.Column(db.String)

    # 1b. Extend the relationship from (1a) to link from an enrollment row back to a student row. 
    # NOTE: This relationship needs to be closed back to the enrollment-student relationship.
    student = db.relationship("Student", back_populates="enrollments")
    # 1d. Extend the relationship from (1c) to link from an enrollment row back to a course row.
    # NOTE: This relationship needs to be closed back to the enrollment-course relationship.
    course = db.relationship("Course", back_populates="enrollments")

    # 3c. Creates serialization rules to avoid cascading when accessing enrollment data from a student.
    # 3d. Creates serialization rules to avoid cascading when accessing enrollment data from a course.
    serialize_rules = ("-student.enrollments", "-course.enrollments")