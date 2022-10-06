import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    value = os.environ.get('MYAPP_FOO')
    return f"<p>Hello, World!!! Value of MYAPP_FOO: {value}</p>"


@app.route("/ping")
def ping():
    return "pong"
