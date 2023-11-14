"""
Can run using the following command:
    > `python(3) app.py`
"""

from flask import Flask

class FlaskWrapper(object):
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.__register_endpoints()

    def __call__(self, *args, **kwargs):
        return self.app.run(*args, **kwargs)

    @property
    def app(self) -> Flask:
        return self._app
    
    @app.setter
    def app(self, app: Flask):
        IS_INSTANCE_OF_FLASK = isinstance(app, Flask)
        if IS_INSTANCE_OF_FLASK:
            self._app = app
        else:
            raise Exception("Did not recognize Flask application instance.")

    def __register_endpoints(self):
        self.app.add_url_rule(rule="/",
                              endpoint="hello",
                              view_func=self.hello,
                              methods=["GET"])
        
    def hello(self):
        return "Hello, World!"