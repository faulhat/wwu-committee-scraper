from sqlite3 import Connection, Cursor, connect
import sys, typing, re, json
from search import SearchRes


def db_setup(target: str) -> tuple[Connection, Cursor]:
    con = connect(target)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS pages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            url         TEXT NOT NULL,
            terms       TEXT NOT NULL,
            score       REAL,
            full_text   TEXT NOT NULL,
            summary     TEXT NOT NULL,
            retrieved   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    return con, cur


def db_add_page(cur: Cursor, url: str, terms: SearchRes, score: float, text: str):
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

    cur.execute(
        "INSERT INTO pages (url, terms, score, full_text, summary) VALUES (?, ?, ?, ?, ?)",
        (url, json.dumps(terms.appearances), score, text, summary),
    )


def db_dump_results(cur: Cursor, f: typing.TextIO = sys.stderr):
    cur.execute(
        "SELECT id, url, terms, score, summary, retrieved FROM pages WHERE score > 0 ORDER BY score DESC"
    )
    rows = cur.fetchall()
    for page_id, url, terms, score, summary, retrieved in rows:
        print(f"{page_id}. {url} @ {retrieved}", file=f)
        print(f"\t{terms}\n\t{score}", file=f)
        print(f"\t{summary}\n", file=f)
