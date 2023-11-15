from json import loads, dump
from flask_restful import Resource, reqparse, fields, marshal

# NOTE: Relative path to data may influence how Python can handle this script.
#       Ensure that Flask/Python is executed from an appropriate location.
PATH_TO_DATASET = "data/tasks.json"

TASK_FIELDS = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "done": fields.Boolean,
    "uri": fields.Url("task")
}

class TaskListAPI(Resource):
    def __init__(self):
        with open(PATH_TO_DATASET, "r") as fr:
            self.tasks = loads(fr.read())["tasks"]
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("title",
                                   type=str,
                                   required=True,
                                   help="No task title provided.",
                                   location="json")
        self.reqparse.add_argument("description",
                                   type=str,
                                   default="No description provided.",
                                   location="json")
        super(TaskListAPI, self).__init__()

    def get(self):
        return {"tasks": [marshal(task, TASK_FIELDS) for task in self.tasks]}, 201
    
    def post(self):
        args = self.reqparse.parse_args()
        with open(PATH_TO_DATASET, "w") as stream:
            task = {
                "id": self.tasks[-1]["id"] + 1 if len(self.tasks) > 0 else 1,
                "title": args["title"],
                "description": args["description"],
                "done": False
            }
            self.tasks.append(task)
            dump({"tasks": self.tasks}, stream, indent=4)
        return {"task": marshal(task, TASK_FIELDS)}, 201