"""
Can run using either of the following commands:
    > `python(3) app.py`
    > `flask run`
"""

from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run()