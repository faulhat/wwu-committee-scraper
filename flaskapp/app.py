import json
import os
from flask import Flask, send_file, send_from_directory, redirect, url_for

# Getting the app started
app = Flask(__name__)


def folder_exists(path):
    return os.path.isdir(path)


# Display static HTML.
@app.route('/')
def index():
    return send_file("../index.html")

# Search for JSON data.
@app.route('/data/<path:subpath>')
def data(subpath):
    if not folder_exists("data/"):
        return redirect(url_for("not_found"))
    else:
        return send_from_directory("data/", subpath)
    

if __name__ == "__main__":
    app.run(debug=True)