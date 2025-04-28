package main

import (
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

	result := make(Histogram)
	AddToHistogram(s, &result)
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("Didn't get expected histogram for input string. Got: %v", result)
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

	result, err := GetPageWords(file)
	if err != nil {
		t.Fatalf("Couldn't extract words: %v", err)
	}

	if !reflect.DeepEqual(result, repetitive_expected) {
		t.Errorf("Didn't get expected histogram for repetitive.html. Got: %v", result)
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

	plot, err := GetPageWords(res.Body)
	if err != nil {
		t.Fatalf("Couldn't generate histogram: %v", err)
	}

	for _, word := range expected_words {
		if plot[word] == 0 {
			t.Errorf("Didn't find expected word: %v", word)
		}
	}
}
