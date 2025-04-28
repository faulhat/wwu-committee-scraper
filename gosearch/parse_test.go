package main

import (
	"golang.org/x/net/html"
	"net/http"
	"os"
	"reflect"
	"testing"
)

func TestHistogram(t *testing.T) {
	s := "!?a a, b b aa ..b a!?"
	expected := Histogram{
		"a":  3,
		"b":  3,
		"aa": 1,
	}

	plot := make(Histogram)
	AddToHistogram(s, &plot)
	if !reflect.DeepEqual(plot, expected) {
		t.Errorf("Didn't get expected histogram for input string. Got: %v", plot)
	}
}

func TestParseFile(t *testing.T) {
	repetitive_expected := Histogram{
		"title":     3,
		"head":      2,
		"paragraph": 3,
		"text":      3,
		"link":      2,
	}

	file, err := os.Open("testdata/repetitive.html")
	if err != nil {
		t.Fatalf("Couldn't open file: %v", err)
	}
	defer file.Close()

	doc, err := html.Parse(file)
	if err != nil {
		t.Fatalf("Couldn't parse HTML: %v", err)
	}

	plot := GetPageWords(doc)
	if !reflect.DeepEqual(plot, repetitive_expected) {
		t.Errorf("Didn't get expected histogram for repetitive.html. Got: %v", plot)
	}
}

func TestWikipedia(t *testing.T) {
	expected_words := []string{"wikipedia", "encyclopedia", "featured"}

	res, err := http.Get("https://en.wikipedia.org/wiki/Main_Page")
	if err != nil {
		t.Fatalf("Couldn't retrieve page: %v", err)
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		t.Errorf("Couldn't retrieve page. Got code %d.", res.StatusCode)
	}

	doc, err := html.Parse(res.Body)
	if err != nil {
		t.Fatalf("Couldn't parse HTML: %v", err)
	}

	plot := GetPageWords(doc)
	for _, word := range expected_words {
		if plot[word] == 0 {
			t.Errorf("Didn't find expected word: %v", word)
		}
	}
}

func TestLinks(t *testing.T) {
	expected_links := []string{
		"https://en.wikipedia.org/wiki/Greece",
		"https://en.wikipedia.org/wiki/Oceanus",
		"https://www.gutenberg.org/files/1658/1658-h/1658-h.htm",
	}

	file, err := os.Open("testdata/sample.html")
	if err != nil {
		t.Fatalf("Couldn't open file: %v", err)
	}
	defer file.Close()

	doc, err := html.Parse(file)
	if err != nil {
		t.Fatalf("Couldn't parse HTML: %v", err)
	}

	links := GetPageLinks(doc)
	if !reflect.DeepEqual(links, expected_links) {
		t.Errorf("Didn't get expected links. Got: %v", links)
	}
}
