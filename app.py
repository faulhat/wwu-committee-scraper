import json
import os
from flask import Flask, render_template, jsonify, abort, request

# Getting the app started
app = Flask(__name__)


def folder_exists(path):
    return os.path.isdir(path)

# Display static HTML.
# @app.route('/')
# def index():
#     return render_template("index.html")

# Search for JSON data.
@app.route('/data/<path:subpath>')
def load_json_file(filename):
    if not folder_exists('/data'):
        abort(404)
    with open(filename, "r") as f:
        data = json.load(f)
    return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True)