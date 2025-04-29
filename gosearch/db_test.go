package main

import (
	"database/sql"
	"testing"

	_ "github.com/mattn/go-sqlite3"
)

func setupTestDB(t *testing.T) *sql.DB {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		t.Fatalf("Failed to open in-memory DB: %v", err)
	}
	defer db.Close()

	err = DBSetup(db)
	if err != nil {
		t.Fatalf("Failed to create table: %v", err)
	}

	return db
}

func TestDBSetup(t *testing.T) {
	setupTestDB(t)
}
