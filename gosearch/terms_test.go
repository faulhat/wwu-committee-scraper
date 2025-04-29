package main

import "testing"

var words = map[string]int{
	"hills":        1,
	"hill":         3,
	"hillsborough": 1,
	"hampton":      1,
	"hillyside":    2,
	"hillysides":   1,
}

var nonsense = "hillsborough hampton hillyside hillysides"

func TestPrefix(t *testing.T) {
	trie := new(TrieNode)
	for word := range words {
		trie.Set(word, 0)
	}

	trie.Prefix(nonsense, 0)
	trie.Prefix(nonsense, 13)
	trie.Prefix(nonsense, 21)
	trie.Prefix(nonsense, 31)

	for word, n := range words {
		v, ok := trie.Get(word)
		if !ok {
			t.Errorf("Trie didn't contain expected word %v.", word)
		} else if v != n {
			t.Errorf("Trie didn't contain expected value for word %v. Got %v", word, v)
		}
	}
}

func TestSearch(t *testing.T) {
	terms := make([]string, 0, len(words))
	for k := range words {
		terms = append(terms, k)
	}

	trie := Search(terms, nonsense)
	for word, n := range words {
		v, ok := trie.Get(word)
		if !ok {
			t.Errorf("Trie didn't contain expected word %v.", word)
		} else if v != n {
			t.Errorf("Trie didn't contain expected value for word %v. Got %v", word, v)
		}
	}
}
