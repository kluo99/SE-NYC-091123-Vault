from flask import Flask
from flask_restful import Api
from resources.homepage import HomePageAPI
from resources.tasklist import TaskListAPI
from resources.task import TaskAPI

app = Flask(__name__)
api = Api(app)
    
api.add_resource(HomePageAPI, "/")
api.add_resource(TaskListAPI, "/todo/api/tasks", endpoint="tasks")
api.add_resource(TaskAPI, "/todo/api/tasks/<int:id>", endpoint="task")

if __name__ == "__main__":
    app.run(port=5000, debug=True)