# Flask SQLite Web App: _Minecraft Mobs_

This demo mini-project is designed to demonstrate the steps to develop and test a REST API configured with a SQL database extended with SQLAlchemy in Flask.

As such, completion of this mini-project can produce an effective API that students can use for further development of a full-stack application by leveraging their React and JavaScript development capabilities. 

Moreover, relying on a SQL database allows for better scalability and improved performance of the backend server, while extending the SQL database's functionality with Flask-SQLAlchemy will enable improved security, validation, authentication, and other critical full-stack development paradigms with the server. 

## Setting Up Our SQL Server

1. Once we've written the boilerplate scaffolding for our SQLite3 server, we want to run the following three commands:
    - Running `flask db init` will initialize our Flask-SQL server.
    - Running `flask db migrate -m "Initial Migration"` will perform a database migration to ensure the stability of your model schema into your SQL server's setup.
    - Running `flask db upgrade` will upgrade your database to the latest version of the updated data's layout and changes.
2. From here, we need to run `seed.py` with relevant scripting to populate our database.
3. We can view our SQL database at any time via the SQL Server viewer in VS Code. 

## Boilerplate CURL Scripts to Test HTTP Requests

1. **Script to Test Home GET Request.**
    ```
    curl -i http://127.0.0.1:<PORT>/
    ```
2. **Script to Test API GET Request.**
    ```
    curl -i http://127.0.0.1:<PORT>/api
    ```
3. **Script to Test GET Request on All Mob Data.**
    ```
    curl -i http://127.0.0.1:<PORT>/api/mobs
    ```
4. **Script to Test GET Request on Single Mob Datum.**
    ```
    curl -i http://127.0.0.1:<PORT>/api/mobs/<int:mob_id>
    ```
5. **Script to Test POST Request on Mobs.**
    ```
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Ender Dragon","hit_points":100,"damage":8,"speed":5,"is_hostile":true}' http://127.0.0.1:<PORT>/api/mobs
    ```
6. **Script to Test PATCH Request on Single Mob.**
    ```
    curl -i -H "Content-Type: application/json" -X PATCH -d '{"is_hostile":true}' http://127.0.0.1:<PORT>/api/mobs/<int:mob_id>
    ```
7. **Script to Test DELETE Request on Single Mob.**
    ```
    curl -H "Content-Type: application/json" -X DELETE http://127.0.0.1:<PORT>/api/mobs/<int:mob_id>
    ```
8. **Script to Test GET Request on Any Error-Handled Page.**
    ```
    curl -i http://127.0.0.1:<PORT>/whereami
    ```