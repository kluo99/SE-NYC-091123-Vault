import time, datetime
from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return {"message": "Hello, world!"}

@app.route("/date", methods=["GET"])
def view_current_date():
    return {"date": get_viewable_date()}

def get_viewable_date():
    current_time = time.time()
    return datetime.datetime.fromtimestamp(current_time).strftime("%Y-%m-%d")

if __name__ == "__main__":
    app.run(debug=True)