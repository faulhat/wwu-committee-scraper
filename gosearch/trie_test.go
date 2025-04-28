package main

import "testing"

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
