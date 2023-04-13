from flask import Flask
from main import main

app = Flask(__name__)


@app.route("/status")
def hello_world():
    return "OK"


@app.route("/run")
def run():
    main()
    return "OK"
