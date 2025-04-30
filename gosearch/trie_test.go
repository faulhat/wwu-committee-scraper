package main

import (
	"reflect"
	"testing"
)

func TestTrieToString(t *testing.T) {
	trie := new(TrieNode)
	trie.Add("hello")
	s := trie.ToString()
	if s != "h - e - l - l - o - $\n" {
		t.Errorf("(1)ToString() didn't produce expected output. Got:\n %v", s)
	}

	trie.Add("hi")
	s = trie.ToString()
	if s != "h - e - l - l - o - $\n  - i - $\n" {
		t.Errorf("(2)ToString() didn't produce expected output. Got:\n %v", s)
	}

	trie.Add("hill")
	s = trie.ToString()
	if s != "h - e - l - l - o - $\n  - i - $\n      - l - l - $\n" {
		t.Errorf("(3)ToString() didn't produce expected output. Got:\n %v", s)
	}

	trie.Add("world")
	s = trie.ToString()
	if s != "h - e - l - l - o - $\n  - i - $\n      - l - l - $\nw - o - r - l - d - $\n" {
		t.Errorf("(3)ToString() didn't produce expected output. Got:\n %v", s)
	}
}

func TestTrieMember(t *testing.T) {
	var words = []string{
		"hello",
		"world",
		"woah",
		"will",
		"hi",
	}

	trie := TrieFromList(words)
	for _, word := range words {
		_, ok := trie.Get(word)
		if !ok {
			t.Errorf("Trie didn't contain expected word %v. Contents: %v", word, trie.ToString())
		}
	}
}

func TestTrieAddSet(t *testing.T) {
	var words = Histogram{
		"hey":   4,
		"hi":    3,
		"hello": 2,
	}

	trie := new(TrieNode)
	for word, n := range words {
		for i := 0; i < n; i++ {
			trie.Add(word)
		}
	}

	for word, n := range words {
		v, ok := trie.Get(word)
		if !ok {
			t.Errorf("Trie didn't contain expected word %v.", word)
		} else if v != n {
			t.Errorf("Trie didn't contain expected value for word %v. Got %v", word, v)
		}
	}

	trie.Set("whatever", 0)
	plot := trie.ToHistogram()
	if !reflect.DeepEqual(*plot, words) {
		t.Errorf("Trie didn't map to expected histogram. Got: %v", plot)
	}

	trie.Set("hey", 2)
	v, ok := trie.Get("hey")
	if !ok {
		t.Errorf("Trie didn't contain expected word after update.")
	} else if v != 2 {
		t.Errorf("Trie didn't contain expected value after update. Got %v", v)
	}
}
