from json import loads, dump
from flask import abort
from flask_restful import Resource, reqparse, fields, marshal

TASK_FIELDS = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "done": fields.Boolean,
    "uri": fields.Url("task")
}

class TaskAPI(Resource):
    def __init__(self):
        with open("server/data/tasks.json", "r") as fr:
            self.tasks = loads(fr.read())["tasks"]
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("title", type=str, location="json")
        self.reqparse.add_argument("description", type=str, location="json")
        self.reqparse.add_argument("done", type=str, location="json")
        super(TaskAPI, self).__init__()

    def get(self, id):
        task = [task for task in self.tasks if task["id"] == int(id)]
        if len(task) == 0:
            abort(404)
        return {"task": marshal(task[0], TASK_FIELDS)}, 201
    
    def patch(self, id):
        task = [task for task in self.tasks if task["id"] == int(id)]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        with open("server/data/tasks.json", "w") as stream:
            for key, value in args.items():
                if value is not None:
                    if value.lower() == "true":
                        task[key] = True
                    elif value.lower() == "false":
                        task[key] = False
                    else:
                        task[key] = value
            dump({"tasks": self.tasks}, stream, indent=4)
        return {"task": marshal(task, TASK_FIELDS)}, 201
    
    def delete(self, id):
        task = [task for task in self.tasks if task["id"] == int(id)]
        if len(task) == 0:
            abort(404)
        with open("server/data/tasks.json", "w") as stream:
            self.tasks.remove(task[0])
            dump({"tasks": self.tasks}, stream, indent=4)
        return task[0], 201