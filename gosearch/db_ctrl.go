package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
	"golang.org/x/net/html"
	"io"
	"log"
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
		retrieved TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);`)

	return err
}

func DBAddPage(db *sql.DB, page *Page) error {
	terms_js, err := json.Marshal(page.Terms)
	if err != nil {
		return err
	}

	hist_js, err := json.Marshal(page.Hist)
	if err != nil {
		return err
	}

	_, err = db.Exec(`INSERT INTO pages (url, terms, hist, full_text) VALUES (?, ?, ?, ?)`, page.Url, terms_js, hist_js, page.Text)
	if err != nil {
		return err
	}

	return nil
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
	page := new(Page)
	page.Url = url

	var terms_js, hist_js string
	row := db.QueryRow(`SELECT terms, hist, full_text FROM pages where url = ?`, url)
	err := row.Scan(&terms_js, &hist_js, &page.Text)
	if err == sql.ErrNoRows {
		return nil, nil
	} else if err != nil {
		return nil, err
	}

	err = json.Unmarshal([]byte(terms_js), &page.Terms)
	if err != nil {
		return nil, err
	}

	err = json.Unmarshal([]byte(hist_js), &page.Hist)
	if err != nil {
		return nil, err
	}

	return page, nil
}

func DBDump(db *sql.DB, dst io.Writer) {
	rows, err := db.Query(`SELECT url, terms, hist, full_text FROM pages`)
	if err != nil {
		log.Fatalf("Failed to dump DB contents: %v", err)
	}
	defer rows.Close()

	for rows.Next() {
		var url string
		var terms string
		var hist string
		var text string

		err := rows.Scan(&url, &terms, &hist, &text)
		if err != nil {
			log.Fatalf("Couldn't can row: %v", err)
		}

		io.WriteString(dst, fmt.Sprintf("%v\n", url))
		io.WriteString(dst, fmt.Sprintf("\t%v\n", terms))
		io.WriteString(dst, fmt.Sprintf("\t%v\n", hist))
		if len(text) > 23 {
			io.WriteString(dst, fmt.Sprintf("\t%v...\n\n", text[:20]))
		} else {
			io.WriteString(dst, fmt.Sprintf("\t%v\n\n", text))
		}
	}
}
