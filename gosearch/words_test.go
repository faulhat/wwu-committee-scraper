package main

import (
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
