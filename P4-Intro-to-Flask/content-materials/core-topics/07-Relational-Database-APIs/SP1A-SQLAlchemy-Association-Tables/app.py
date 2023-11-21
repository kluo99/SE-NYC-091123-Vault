#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


from flask import make_response, jsonify, request
from flask import Flask
from models import db, Student, Course, Enrollment

from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
migrate = Migrate(app, db)
db.init_app(app)


#######################################################
######## INITIAL SETUP ROUTES FOR APPLICATION #########
#######################################################


# GET route to access database.
@app.route("/")
def app_root():
    return {"msg": "Flask application is active."}

# GET route to access API entry point.
@app.route("/api")
def api_entry():
    return {"msg": "Successful API access."}


#######################################################
########## INITIAL SETUP ROUTES FOR STUDENTS ##########
#######################################################


# GET route to access students.
@app.get("/api/students")
def view_all_students():
    all_students = Student.query.all()
    enrolled_students = [student.to_dict(rules=("-enrollments",)) for student in all_students]
    return make_response(jsonify(enrolled_students), 200)

# GET route to access an individual student by ID.
@app.get("/api/students/<int:student_id>")
def view_student_by_id(student_id: int):
    matching_student = Student.query.filter(Student.id == student_id).first()
    if not matching_student:
        return make_response(jsonify({"error": f"Student ID `{student_id}` not found in database."}), 404)
    return make_response(jsonify(matching_student.to_dict()), 200)

# POST route to add new student to database.
@app.post("/api/students")
def add_student():
    POST_REQUEST = request.get_json()
    new_student = Student(
        fname=POST_REQUEST["fname"], 
        lname=POST_REQUEST["lname"], 
        grad_year=POST_REQUEST["grad_year"]
    )
    db.session.add(new_student)
    db.session.commit()
    return make_response(jsonify(new_student.to_dict()), 201)

# PATCH route to edit a student's information in database.
@app.patch("/api/students/<int:student_id>")
def edit_student(student_id: int):
    matching_student = Student.query.filter(Student.id == student_id).first()
    if not matching_student:
        return make_response(jsonify({"error": f"Student ID `{student_id}` not found in database."}), 404)
    PATCH_REQUEST = request.get_json()
    for attribute in PATCH_REQUEST:
        setattr(matching_student, attribute, PATCH_REQUEST[attribute])
    db.session.add(matching_student)
    db.session.commit()
    return make_response(jsonify(matching_student.to_dict()), 200)

# DELETE route to remove a student from the database.
@app.delete("/api/students/<int:student_id>")
def remove_student(student_id: int):
    matching_student = Student.query.filter(Student.id == student_id).first()
    if not matching_student:
        return make_response(jsonify({"error": f"Student ID `{student_id}` not found in database."}), 404)
    db.session.delete(matching_student)
    db.session.commit()
    return make_response(jsonify(matching_student.to_dict()), 200)


#######################################################
########## INITIAL SETUP ROUTES FOR COURSES ###########
#######################################################


# GET route to access courses.
@app.get("/api/courses")
def view_all_courses():
    all_courses = Course.query.all()
    enrollable_courses = [course.to_dict(rules=("-enrollments",)) for course in all_courses]
    return make_response(jsonify(enrollable_courses), 200)

# GET route to access an individual course by ID.
@app.get("/api/courses/<int:course_id>")
def view_course_by_id(course_id: int):
    matching_course = Course.query.filter(Course.id == course_id).first()
    if not matching_course:
        return make_response(jsonify({"error": f"Course ID `{course_id}` not found in database."}), 404)
    return make_response(jsonify(matching_course.to_dict()), 200)

# POST route to add new course to database.
@app.post("/api/courses")
def add_course():
    POST_REQUEST = request.get_json()
    new_course = Course(
        title=POST_REQUEST["title"], 
        instructor=POST_REQUEST["instructor"], 
        credits=POST_REQUEST["credits"]
    )
    db.session.add(new_course)
    db.session.commit()
    return make_response(jsonify(new_course.to_dict()), 201)

# PATCH route to edit a course's information in database.
@app.patch("/api/courses/<int:course_id>")
def edit_course(course_id: int):
    matching_course = Course.query.filter(Course.id == course_id).first()
    if not matching_course:
        return make_response(jsonify({"error": f"Course ID `{course_id}` not found in database."}), 404)
    PATCH_REQUEST = request.get_json()
    for attribute in PATCH_REQUEST:
        setattr(matching_course, attribute, PATCH_REQUEST[attribute])
    db.session.add(matching_course)
    db.session.commit()
    return make_response(jsonify(matching_course.to_dict()), 200)

# DELETE route to remove a course from the database.
@app.delete("/api/courses/<int:course_id>")
def remove_course(course_id: int):
    matching_course = Course.query.filter(Course.id == course_id).first()
    if not matching_course:
        return make_response(jsonify({"error": f"Course ID `{course_id}` not found in database."}), 404)
    db.session.delete(matching_course)
    db.session.commit()
    return make_response(jsonify(matching_course.to_dict()), 200)


#######################################################
########## ASSOCIATION METHODS FOR STUDENTS ###########
#######################################################


# POST route to add a course to a student's currently enrolled courses (list).
@app.post("/api/students/<int:student_id>/enrollments")
def enroll_in_course(student_id: int):
    # 1. Find the student that matches the given ID from the URL/route.
    matching_student = Student.query.filter(Student.id == student_id).first()
    # 2. Find the course that matches the given ID from the request. 
    # NOTE: My request will be neither a `Student()` nor a `Course()`. 
    #       It will be an `Enrollment()` with IDs for a student and a course.
    POST_REQUEST = request.get_json()
    course_id, enrollment_term = POST_REQUEST["course_id"], POST_REQUEST["term"]
    matching_course = Course.query.filter(Course.id == course_id).first()
    # NOTE: It's helpful to validate our matching objects before attempting to manipulate SQL tables.
    if not matching_student:
        return make_response(jsonify({"error": f"Student ID `{student_id}` not found"}), 404)
    if not matching_course:
        return make_response(jsonify({"error": f"Course ID `{course_id}` not found"}), 404)
    # 3. Link our matching student and course using a third object: `Enrollment`. 
    new_enrollment = Enrollment(student_id=matching_student.id, 
                                course_id=matching_course.id,
                                term=enrollment_term)
    # 4. Stage and commit changes to our database.
    db.session.add(new_enrollment)
    db.session.commit()
    # 5. Return acceptable value to frontend/API.
    return make_response(jsonify(new_enrollment.to_dict(rules=("-student",))), 201)

# GET route to view all enrolled courses for a current student.
@app.get("/api/students/<int:student_id>/courses")
def get_courses_for_student(student_id: int):
    matching_student = Student.query.filter(Student.id == student_id).first()
    if not matching_student:
        return make_response(jsonify({"error": f"Student ID `{student_id}` not found"}), 404)
    all_courses_for_student = [course.to_dict(rules=("-enrollments",)) for course in matching_student.courses]
    return make_response(jsonify(all_courses_for_student), 200)


#######################################################
########## ASSOCIATION METHODS FOR COURSES ############
#######################################################


# POST route to add a student to a course's currently enrolled students (list).
@app.post("/api/courses/<int:course_id>/enrollments")
def enroll_student(course_id: int):
    # 1. Find the course that matches the given ID from the URL/route.
    matching_course = Course.query.filter(Course.id == course_id).first()
    # 2. Find the student that matches the given ID from the request. 
    # NOTE: My request will be neither a `Course()` nor a `Student()`. 
    #       It will be an `Enrollment()` with IDs for a course and a student.
    POST_REQUEST = request.get_json()
    student_id, enrollment_term = POST_REQUEST["student_id"], POST_REQUEST["term"]
    matching_student = Student.query.filter(Student.id == student_id).first()
    # NOTE: It's helpful to validate our matching objects before attempting to manipulate SQL tables.
    if not matching_course:
        return make_response(jsonify({"error": f"Course ID `{course_id}` not found"}), 404)
    if not matching_student:
        return make_response(jsonify({"error": f"Student ID `{student_id}` not found"}), 404)
    # 3. Link our matching course and student using an association table: `Enrollment`. 
    new_enrollment = Enrollment(course_id=matching_course.id,
                                student_id=matching_student.id,
                                term=enrollment_term)
    # 4. Stage and commit changes to our database.
    db.session.add(new_enrollment)
    db.session.commit()
    # 5. Return acceptable value to frontend/API.
    return make_response(jsonify(new_enrollment.to_dict(rules=("-course",))), 201)

# GET route to view all enrolled students for a current course.
@app.get("/api/courses/<int:course_id>/students")
def get_students_for_course(course_id: int):
    matching_course = Course.query.filter(Course.id == course_id).first()
    if not matching_course:
        return make_response(jsonify({"error": f"Course ID `{course_id}` not found"}), 404)
    all_students_for_course = [student.to_dict(rules=("-enrollments",)) for student in matching_course.students]
    return make_response(jsonify(all_students_for_course), 200)


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