package main

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
)

func DBSetup(db *sql.DB) error {
	_, err := db.Exec(`CREATE TABLE IF NOT EXISTS pages (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		url TEXT NOT NULL,
		terms TEXT NOT NULL,
		hist TEXT NOT NULL,
		full_text TEXT NOT NULL,
		retrieved TIMESTAMP
	);`)

	return err
}
