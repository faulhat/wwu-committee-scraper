package main

import "strings"

type TrieNode struct {
	term bool
	children [256]*TrieNode
	val int
}

func TrieFromList(init []string) *TrieNode {
	return new(TrieNode)
}

func (n *TrieNode) ToString() string {
	var b strings.Builder
	n.intoString(&b, 0)
	return b.String()
}

func (n *TrieNode) intoString(b *strings.Builder, depth int) {
	indent := false
	if n.term {
		b.WriteString(" - $\n")
		indent = true
	}

	for i, c := range n.children {
		if c != nil {
			if depth > 0 {
				if indent {
					b.WriteString(strings.Repeat(" ", 2 + 4 * (depth - 1)))
				} else {
					b.WriteString(" ")
				}
				indent = true

				b.WriteString("- ")
			}

			b.WriteByte(byte(i))
			c.intoString(b, depth + 1)
		}
	}
}

func (n *TrieNode) Add(s string) {
	n.put(s, 0)
}

func (n *TrieNode) put(s string, c int) {
	if c == len(s) {
		n.term = true
	} else {
		if n.children[s[c]] == nil {
			n.children[s[c]] = new(TrieNode)
		}

		n.children[s[c]].put(s, c + 1)
	}
}

func (n *TrieNode) Contains(s string) bool {
	return false
}


