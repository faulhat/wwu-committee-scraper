package main

/* Return a trie mapping each term in w to its number of appearances in s */
func Search(w []string, s string) *TrieNode {
	t := TrieFromList(w)
	for i := 0; i < len(s); i++ {
		t.Prefix(s, i)
	}

	return t
}

/* Increment all entries in n which match s starting from position c. */
func (n *TrieNode) Prefix(s string, c int) {
	if n.term {
		n.val++
	}

	if c < len(s) && n.children[s[c]] != nil {
		n.children[s[c]].Prefix(s, c+1)
	}
}
