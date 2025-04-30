from sqlite3 import Connection, Cursor, connect
import sys, typing, json
from search import SearchRes


def db_setup(target: str) -> Connection:
    con = connect(target)
    con.cursor().execute(
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
    con.commit()

    return con


def db_add_page(
    con: Connection, url: str, title: str, terms: SearchRes, score: float, text: str
):
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

    con.cursor().execute(
        "INSERT INTO pages (url, title, terms, score, full_text, summary) VALUES (?, ?, ?, ?, ?, ?)",
        (url, title, json.dumps(terms.appearances), score, text, summary),
    )
    con.commit()


def db_dump_results(con: Connection, f: typing.TextIO = sys.stderr):
    cur = con.cursor()
    cur.execute(
        "SELECT url, title, terms, score, summary, retrieved FROM pages WHERE score > 0"
    )
    rows = cur.fetchall()
    for url, title, terms, score, summary, retrieved in rows:
        print(f'{url} @ {retrieved} "{title}"', file=f)
        print(f"\t{terms}\n\t{score}", file=f)
        print(f"\t{summary}\n", file=f)
