import os
from bottle import route, run

@route("/")
def hello_world():
        return "Hello World! TESTING push"

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
