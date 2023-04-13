from flask import Flask

from main import main

app = Flask(__name__)


@app.route("/")
def root():
    return "OK"


@app.route("/status")
def status():
    return "OK"


@app.route("/run")
def run():
    main()
    return "OK"
