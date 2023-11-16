# Flask SQLite Web App: _Minecraft Mobs_

This demo mini-project is designed to demonstrate the steps to develop and test a REST API configured with a SQL database.

As such, completion of this mini-project can produce an effective API that students can use for further development of a full-stack application by leveraging their React and JavaScript development capabilities. 

Moreover, relying on a SQL database allows for better scalability and improved performance of the backend server.

## Steps to Set Up SQL for Database Development

1. On Mac OS X, run `brew install sqlite3` in your Terminal.
2. On Windows/Linux, go to [sqlite.org/download.html](http://sqlite.org/download.html) and choose the latest 32-bit DLL (x86) precompiled binary for SQLite. 

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