import json
import os
from flask import Flask, render_template, jsonify, abort, request, redirect, url_for

# Getting the app started
app = Flask(__name__)


def folder_exists(path):
    return os.path.isdir(path)

# Display static HTML.
@app.route('/')
def index():
    return render_template("index.html")

# Search for JSON data.
@app.route('/data/<path:subpath>', methods=["GET", "POST"])
def get_path():
    if not folder_exists('/data'):
        return redirect(url_for('404_error'))
    return True

def load_json_file(filename):
   with open(filename, "r") as f:
       data = json.load(f)
   return data

if (get_path() == True):
    json_data = load_json_file('/data/*.json')

# @app.route('/', methods=["GET", "POST"])
# def get_data():
#     if not folder_exists('/data'):
#         return redirect(url_for('404_error'))
    



if __name__ == "__main__":
    app.run(debug=True)