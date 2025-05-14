from sqlite3 import Connection, connect
import sys, typing, json
from search import SearchRes


class PagesDB:
    def __init__(self, path):
        self.con = connect(path)

    def setup(self):
        self.con.cursor().execute(
            """
            CREATE TABLE IF NOT EXISTS pages (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                url         TEXT NOT NULL,
                title       TEXT,
                terms       TEXT NOT NULL,
                score       REAL,
                full_text   TEXT NOT NULL,
                summary     TEXT NOT NULL,
                retrieved   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.con.commit()

        return self.con

    def add_page(self, url, title, terms, score, text):
        summary = ""
        if terms.total == 0:
            if len(text) > 103:
                summary = text[:100] + "..."
            else:
                summary = text
        else:
            if terms.first > 13:
                summary = "..." + text[terms.first - 10 : terms.first]
            else:
                summary = text[terms.first - 13 : terms.first]

            summary += "<b>" + text[terms.first : terms.end] + "</b>"
            if len(summary) + len(text[terms.end :]) > 103:
                summary += text[terms.end : terms.end + 100] + "..."
            else:
                summary += text[terms.end :]

        self.con.cursor().execute(
            "INSERT INTO pages (url, title, terms, score, full_text, summary) VALUES (?, ?, ?, ?, ?, ?)",
            (url, title, json.dumps(terms.appearances), score, text, summary),
        )
        self.con.commit()

    def count_pages(self):
        cur = self.con.cursor()
        cur.execute("SELECT COUNT() FROM pages")
        return cur.fetchone()[0]

    def dump_results(self, f=sys.stderr):
        cur = self.con.cursor()
        cur.execute(
            "SELECT url, title, terms, score, summary, retrieved FROM pages WHERE score > 0"
        )
        rows = cur.fetchall()
        for url, title, terms, score, summary, retrieved in rows:
            print(f'{url} @ {retrieved} "{title}"', file=f)
            print(f"\t{terms}\n\t{score}", file=f)
            print(f"\t{summary}\n", file=f)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.con.close()
