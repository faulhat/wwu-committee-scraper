package main

/* Increment all entries in n which match s starting from position c. */
func (n *TrieNode) Prefix(s string, c int) {
	if n.term {
		n.val++
	}

	if c < len(s) && n.children[s[c]] != nil {
		n.children[s[c]].Prefix(s, c + 1)
	}
}
