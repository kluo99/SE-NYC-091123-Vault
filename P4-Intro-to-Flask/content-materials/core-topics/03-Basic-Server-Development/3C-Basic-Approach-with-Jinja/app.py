"""
Can run using either of the following commands:
    > `python(3) app.py`
    > `flask run`
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
@app.route("/hello", methods=["GET"])
@app.route("/hello/<username>", methods=["GET"])
def home(username=None):
    username = username or "User"
    return render_template("index.html", username=username)

if __name__ == "__main__":
    app.run()