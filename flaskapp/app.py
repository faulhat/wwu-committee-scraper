import os
from flask import Flask, send_file, send_from_directory, redirect, url_for, jsonify
from sqlite3 import connect, Cursor
from typing import Any

# Getting the app started
app = Flask(__name__)


# Display static HTML.
@app.route('/')
def index():
    # return send_file("../demo_frontend/index.html")
    return send_file(os.path.join(os.path.dirname(__file__), '../demo_frontend/index.html'))


# Search for JSON data.
@app.route('/data/<path:subpath>')
def data(subpath):
    if not os.path.isdir("data/"):
        return redirect(url_for("not_found"))
    else:
        return send_from_directory("data/", subpath)
    

def full_pages_table(cur: Cursor) -> list[dict[str, Any]]:
    cur.execute(
        "SELECT url, title, score, summary FROM pages WHERE score > 0 ORDER BY score DESC"
    )
    rows = cur.fetchall()
    
    results = []
    for url, title, score, summary in rows:
        results.append({
            "url": url,
            "title": title if title is not None else url,
            "score": score,
            "summary": summary
        })
    
    return results


@app.route('/pages.json')
def pages_list():
    table = []
    db_path = os.path.join(os.path.dirname(__file__), '../wwucrawler/pages.db')
    if os.path.isfile(db_path):
        with connect(db_path) as db_con:
            table = full_pages_table(db_con.cursor())
    
    return jsonify(table)


if __name__ == "__main__":
    app.run(debug=True)
