import sys
from traceback import print_exc
from argparse import ArgumentParser, REMAINDER

from crawler import Crawler
from database import db_setup, db_dump_results


parser = ArgumentParser(prog="crawler")
parser.add_argument("-o", "--ofile", nargs="?", help="output file")
parser.add_argument("-d", "--depth", default=4, type=int, help="max search depth")
parser.add_argument(
    "-u", "--unbounded", action="store_true", help="disable max search depth"
)
parser.add_argument("keywords", nargs=REMAINDER, help="words to search for")
args = parser.parse_args()

ofile = sys.stdout
if args.ofile is not None:
    try:
        ofile = open(args.ofile, "w")
    except:
        print("Could not open output file. Defaulting to stdout.")

print(f"Searching WWU domain for keywords: {args.keywords}")
print(f"Max depth: {'INF' if args.unbounded else args.depth}")

db_con = db_setup("../pages.db")
try:
    crawler = Crawler(db_con, set(args.keywords), black_subdomains=["cedar", "catalog"])
    urls = crawler.crawl(
        "https://wwu.edu/", bounded=(not args.unbounded), depth=args.depth
    )

    db_dump_results(db_con, f=ofile)
except:
    print_exc()
finally:
    if ofile != sys.stdout:
        ofile.close()

    db_con.close()
