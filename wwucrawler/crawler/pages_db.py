from sqlite3 import Connection, connect
import sys, typing, json
from search import SearchRes


class PagesDB:
    def __init__(self, path):
        self.con = connect(path)

    # Ensure pages table exists
    def setup(self):
        self.con.cursor().execute(
            """
            CREATE TABLE IF NOT EXISTS pages (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                url                 TEXT NOT NULL,
                title               TEXT,
                terms               TEXT NOT NULL,
                score               REAL,
                full_text           TEXT NOT NULL,
                summary_before      TEXT NOT NULL,
                summary_keyword     TEXT NOT NULL,
                summary_after       TEXT NOT NULL,
                retrieved           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.con.commit()

    # Add a page to the database
    #  Generates a temporary summary highlighting the first search term found
    def add_page(self, url, title, terms, score, text):
        summary_before = ""
        summary_keyword = ""
        summary_after = ""

        if terms.total == 0:
            if len(text) > 103:
                summary_before = text[:100] + "..."
            else:
                summary_before = text
        else:
            if terms.first > 13:
                summary_before = "..." + text[terms.first - 10 : terms.first]
            else:
                summary_before = text[terms.first - 13 : terms.first]

            summary_keyword = text[terms.first : terms.end]
            if (
                len(summary_before) + len(summary_keyword) + len(text[terms.end :])
                > 103
            ):
                summary_after = text[terms.end : terms.end + 100] + "..."
            else:
                summary_after = text[terms.end :]

        self.con.cursor().execute(
            "INSERT INTO pages (url, title, terms, score, full_text, summary_before, summary_keyword, summary_after) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                url,
                title,
                json.dumps(terms.appearances),
                score,
                text,
                summary_before,
                summary_keyword,
                summary_after,
            ),
        )
        self.con.commit()

    # Number of stored pages
    def count_pages(self):
        cur = self.con.cursor()
        cur.execute("SELECT COUNT() FROM pages")
        return cur.fetchone()[0]

    # Dump list of pages with at least one keyword to a file
    def dump_results(self, f=sys.stderr):
        cur = self.con.cursor()
        cur.execute(
            "SELECT url, title, terms, score, summary_before, summary_keyword, summary_after, retrieved FROM pages WHERE score > 0"
        )
        rows = cur.fetchall()
        for (
            url,
            title,
            terms,
            score,
            summary_before,
            summary_keyword,
            summary_after,
            retrieved,
        ) in rows:
            print(f'{url} @ {retrieved} "{title}"', file=f)
            print(f"\t{terms}\n\t{score}", file=f)
            if summary_keyword:
                print(
                    f"\t{summary_before}**{summary_keyword}**{summary_after}\n", file=f
                )
            else:
                print(f"\t{summary_before}\n", file=f)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.con.close()
