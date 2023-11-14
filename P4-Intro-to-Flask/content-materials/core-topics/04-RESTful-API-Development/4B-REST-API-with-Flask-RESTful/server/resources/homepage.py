from flask_restful import Resource

class HomePageAPI(Resource):
    def get(self):
        return {"message": "Welcome to the TODO List API!"}