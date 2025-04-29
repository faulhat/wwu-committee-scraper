package main

import (
	"strings"
	"fmt"
)

type TrieNode struct {
	term     bool
	children [256]*TrieNode
	val      int
}

func TrieFromList(terms []string) *TrieNode {
	n := new(TrieNode)
	for _, term := range terms {
		n.Set(term, 0)
	}

	return n
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
					b.WriteString(strings.Repeat(" ", 2+4*(depth-1)))
				} else {
					b.WriteString(" ")
				}
				indent = true

				b.WriteString("- ")
			}

			b.WriteByte(byte(i))
			c.intoString(b, depth+1)
		}
	}
}

func (n *TrieNode) ToHistogram() *Histogram {
	plot := Histogram{}
	n.intoHistogram(&plot, "")
	return &plot
}

func (n *TrieNode) intoHistogram(plot *Histogram, acc string) {
	if n.term {
		(*plot)[acc] = n.val
	}

	for i, c := range n.children {
		if c != nil {
			c.intoHistogram(plot, fmt.Sprintf("%s%c", acc, i))
		}
	}
}

func (n *TrieNode) Add(s string) {
	t := n.ensureNode(s, 0)
	t.val++
}

func (n *TrieNode) Set(s string, val int) {
	t := n.ensureNode(s, 0)
	t.val = val
}

func (n *TrieNode) ensureNode(s string, c int) *TrieNode {
	if c == len(s) {
		n.term = true
		return n
	} else {
		if n.children[s[c]] == nil {
			n.children[s[c]] = new(TrieNode)
		}

		return n.children[s[c]].ensureNode(s, c+1)
	}
}

func (n *TrieNode) Get(s string) (int, bool) {
	return n.find(s, 0)
}

func (n *TrieNode) find(s string, c int) (int, bool) {
	if c == len(s) {
		return n.val, n.term
	}

	if n.children[s[c]] == nil {
		return 0, false
	}

	return n.children[s[c]].find(s, c+1)
}
