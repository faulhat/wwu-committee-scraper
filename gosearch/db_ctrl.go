package main

import (
	"database/sql"
	"errors"
	_ "github.com/mattn/go-sqlite3"
	"golang.org/x/net/html"
	"strings"
	"time"
)

type Page struct {
	Id        int
	Url       string
	Terms     Histogram
	Hist      Histogram
	Text      string
	Retrieved time.Time
}

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

func DBAddPage(db *sql.DB, url string, root *html.Node, terms []string) error {
	return errors.New("Not implemented")
}

func NewPage(url string, root *html.Node, terms []string) *Page {
	page := new(Page)
	page.Url = url
	page.Text = GetPageText(root)
	page.Terms = *Search(terms, strings.ToLower(page.Text)).ToHistogram()
	page.Hist = GetPageWords(root)

	return page
}

func DBGetPage(db *sql.DB, url string) (*Page, error) {
	return nil, errors.New("Not implemented")
}
