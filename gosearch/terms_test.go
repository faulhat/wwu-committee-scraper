package main

import "testing"

func TestPrefix(t *testing.T) {
	words := map[string]int{
		"hills": 1,
		"hill": 3,
		"hillsborough": 1,
		"hampton": 1,
		"hillyside": 2,
		"hillysides": 1,
	}

	nonsense := "hillsborough hampton hillyside hillysides"
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
