package main

import (
	"database/sql"
	"golang.org/x/net/html"
	"os"
	"reflect"
	"testing"

	_ "github.com/mattn/go-sqlite3"
)

func setupTestDB(t *testing.T) *sql.DB {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		t.Fatalf("Failed to open in-memory DB: %v", err)
	}

	err = DBSetup(db)
	if err != nil {
		t.Fatalf("Failed to create table: %v", err)
	}

	return db
}

func TestDBAddPage1(t *testing.T) {
	search_terms := []string{"hill", "hilly", "hills", "and hill"}

	e_terms := Histogram{
		"hill":     5,
		"hilly":    1,
		"hills":    3,
		"and hill": 1,
	}

	e_text := "Hilly hills and hillsides on Hillsborough made our way to The Hill country"

	path := "testdata/hillcountry.html"
	file, err := os.Open(path)
	if err != nil {
		t.Fatalf("Couldn't open file: %v", err)
	}
	defer file.Close()

	doc, err := html.Parse(file)
	if err != nil {
		t.Fatalf("Couldn't parse HTML: %v", err)
	}

	db := setupTestDB(t)
	defer db.Close()

	err = DBAddPage(path, doc, search_terms)
	if err != nil {
		t.Fatalf("Couldn't add page to DB: %v", err)
	}

	page, err := DBGetPage(path)
	if err != nil {
		t.Fatalf("Couldn't retrieve page from DB: %v", err)
	}

	if page.Text != e_text {
		t.Errorf("Didn't get expected text from DB. Got: %v", page.Text)
	}

	if !reflect.DeepEqual(page.Terms, e_terms) {
		t.Errorf("Didn't get expected terms table from DB. Got: %v", page.Terms)
	}
}

func TestDBAddPage2(t *testing.T) {
	e_hist := Histogram{
		"title":     3,
		"head":      2,
		"paragraph": 3,
		"text":      3,
		"link":      2,
	}

	e_text := "Head title, title head title paragraph text Paragraph text paragraph! link. link.. Text "

	path := "testdata/repetitive.html"
	file, err := os.Open(path)
	if err != nil {
		t.Fatalf("Couldn't open file: %v", err)
	}
	defer file.Close()

	doc, err := html.Parse(file)
	if err != nil {
		t.Fatalf("Couldn't parse HTML: %v", err)
	}

	db := setupTestDB(t)
	defer db.Close()

	err = DBAddPage(path, doc, nil)
	if err != nil {
		t.Fatalf("Couldn't add page to DB: %v", err)
	}

	page, err := DBGetPage(path)
	if err != nil {
		t.Fatalf("Couldn't retrieve page from DB: %v", err)
	}

	if page.Text != e_text {
		t.Errorf("Didn't get expected text from DB. Got: %v", page.Text)
	}

	if !reflect.DeepEqual(page.Hist, e_hist) {
		t.Errorf("Didn't get expected terms table from DB. Got: %v", page.Terms)
	}
}
