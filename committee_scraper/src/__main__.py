import sqlite3
import sys
from argparse import ArgumentParser
from scraper import Scraper
from sqlite3 import connect

parser = ArgumentParser(prog="committee_scraper",
                        description="Summarize and extract committee information")

parser.add_argument("--model", type=str, default=None, help="LLM Model")
parser.add_argument("--min_score", type=int, default=0, help="Min score of pages to summarize")
args = parser.parse_args()

# DB file path
db_path = "../pages.db"

try:
    db_target = db_path
    db_connection = connect(db_target)
except sqlite3.Error as e:
    print(e.__str__())
    sys.exit(1)

# Initialize the scraper
scraper = Scraper(model=args.model, score_threshold=args.min_score, db_connection=db_connection)

try:
    scraper.fetch_urls()
    scraper.scrape()
except KeyboardInterrupt as e:
    print(f'\nFinished execution on link #{scraper.iteration}: {scraper.URLS[scraper.iteration]}')
    db_connection.close()
    sys.exit(1)
except Exception as e:
    print(e.__str__())
    db_connection.close()
    sys.exit(1)

db_connection.close()
sys.exit(0)
