package main

import (
	"os"
	"reflect"
	"testing"
)

const repetitive_expected map[string]int = map[string]int{
	"title":     7,
	"head":      2,
	"paragraph": 3,
	"text":      3,
	"link":      2,
}

func TestParser(t *testing.T) {
	file, err = os.Open("testdata/repetitive.html")
	if err != nil {
		t.Fatalf("Couldn't open file: %v", err)
	}

	defer file.Close()

	result := getAllWords(file)
	if !reflect.DeepEqual(result, repetitive_expected) {
		t.Errorf("Didn't get expected word counts for repetitive.html. Got: %v", result)
	}
}
