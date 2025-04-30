/* Tom's wwu.edu crawler program (improved)
 *  aka the M2 Crawler
 * Collects different types of data about page contents and stores
 *  findings in a SQLite database.
 */

package main

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"log"
	"os"
)

func main() {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		log.Fatalf("Failed to open in-memory DB: %v", err)
	}

	err = DBSetup(db)
	if err != nil {
		log.Fatalf("Failed to create table: %v", err)
	}

	keywords := []string{"committee", "Logan"}
	black_subdomains := []string{"cedar", "catalog"}
	black_urls := []string{}

	crawl(db, "https://wwu.edu/", keywords, true, 1, black_subdomains, black_urls)

	DBDump(db, os.Stderr)
}
