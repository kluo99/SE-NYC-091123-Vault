# Flask SQLite Backend API: _Student Course Picker_

This demo mini-project is designed to demonstrate the steps to develop and test a REST API configured with a SQL database extended with SQLAlchemy in Flask.

As such, completion of this mini-project can produce an effective API that students can use for further development of a full-stack application by leveraging their React and JavaScript development capabilities. 

Moreover, relying on a SQL database allows for better scalability and improved performance of the backend server, while extending the SQL database's functionality with Flask-SQLAlchemy will enable improved security, validation, authentication, and other critical full-stack development paradigms with the server. 

## Setting Up Our SQL Server

Once we've written the boilerplate scaffolding for our SQLite3 server, we want to run the following three commands:
- Running `flask db init` will initialize our Flask-SQL server.
- Running `flask db migrate -m "Initial Migration"` will perform a database migration to ensure the stability of your model schema into your SQL server's setup.
- Running `flask db upgrade` will upgrade your database to the latest version of the updated data's layout and changes.

From here, we need to run `seed.py` with relevant scripting to populate our database.

We can view our SQL database at any time via the SQL Server viewer in VS Code. 

## Updating Database Schemas

At times, it may be necessary to update the database schemas and structures due to significant architectural changes to how the tables are set up. In those cases, the follwoing commands can be run:
- Running `flask db migrate -m "Database Migration"` will perform a database migration to commit new changes to the database schema into your SQL server's setup. 
  - NOTE: It's recommended to change the migration commit message to something more pertinent to the precise nature of the migrational changes. 
- Running `flask db upgrade` will upgrade your database to the latest version of the updated data's layouts and changes.

## Boilerplate CURL Scripts to Test HTTP Requests

### Basic CURL Scripts for Application Setup and API Access.

1. **GET Request to Access Database.**
    ```
    curl -i http://127.0.0.1:<PORT>/
    ```

2. **GET Request to View API Entry Point.**
    ```
    curl -i http://127.0.0.1:<PORT>/api
    ```

3. **General GET Request for 404 Error Handling.**
    ```
    curl -i http://127.0.0.1:<PORT>/whereami
    ```

### Basic CURL Scripts for Student Data Manipulation

4. **GET Request to Access All Students.**
    ```
    curl -i http://127.0.0.1:<PORT>/api/students
    ```

5. **GET Request to Access an Individual Student by ID.**
    ```
    curl -i http://127.0.0.1:<PORT>/api/students/<int:student_id>
    ```

6. **POST Request to Add New Student to Database.**
    ```
    curl -i -H "Content-Type: application/json" -X POST -d '{"fname":"Jimothy", "lname":"Johnson", "grad_year":2023}' http://127.0.0.1:<PORT>/api/students
    ```

7. **PATCH Route to Edit a Student's Information in Database.**
    ```
    curl -i -H "Content-Type: application/json" -X PATCH -d '{"grad_year":2025}' http://127.0.0.1:<PORT>/api/students/<int:student_id>
    ```

8. **DELETE Request to Remove a Student from the Database.**
    ```
    curl -H "Content-Type: application/json" -X DELETE http://127.0.0.1:<PORT>/api/students/<int:student_id>
    ```

### Basic CURL Scripts for Course Data Manipulation

9. **GET Request to Access All Courses.**
    ```
    curl -i http://127.0.0.1:<PORT>/api/courses
    ```

10. **GET Request to Access an Individual Course by ID.**
    ```
    curl -i http://127.0.0.1:<PORT>/api/courses/<int:course_id>
    ```

11. **POST Request to Add New Course to Database.**
    ```
    curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Intro to Python", "instructor":"Kashy", "credits":3}' http://127.0.0.1:<PORT>/api/courses
    ```

12. **PATCH Route to Edit a Course's Information in Database.**
    ```
    curl -i -H "Content-Type: application/json" -X PATCH -d '{"instructor":"Sakib"}' http://127.0.0.1:<PORT>/api/courses/<int:course_id>
    ```

13. **DELETE Request to Remove a Course from the Database.**
    ```
    curl -H "Content-Type: application/json" -X DELETE http://127.0.0.1:<PORT>/api/courses/<int:course_id>
    ```

### Higher-Level CURL Scripts for Associative Data Manipulation

14. **GET Route to View All Enrolled Courses for a Current Student.**
    ```
    curl -i http://127.0.0.1:<PORT>/api/students/<int:student_id>/courses
    ```

15. **POST Route to Add a Course to a Student's Currently Enrolled Courses.**
    ```
    curl -i -H "Content-Type: application/json" -X POST -d '{"student_id":1, "course_id":1, "term":"S2024"}' http://127.0.0.1:<PORT>/api/students/<int:student_id>/enrollments
    ```

16. **GET Route to View All Enrolled Students in a Particular Course.**
    ```
    curl -i http://127.0.0.1:<PORT>/api/courses/<int:course_id>/students
    ```

17. **POST Route to Add a Student to a Course's Currently Enrolled Students.**
    ```
    curl -i -H "Content-Type: application/json" -X POST -d '{"course_id":1, "student_id":1, "term":"S2024"}' http://127.0.0.1:<PORT>/api/courses/<int:course_id>/enrollments
    ```


