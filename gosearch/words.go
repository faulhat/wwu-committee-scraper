package main

import (
	"golang.org/x/net/html"
	"io"
	"regexp"
	"strings"
)

type Histogram = map[string]int

func AddToHistogram(s string, into *Histogram) {
	nonASCII := regexp.MustCompile(`[^-A-Za-z]+`)
	words := nonASCII.Split(s, -1)

	for _, word := range words {
		if word != "" {
			lower := strings.ToLower(word)
			(*into)[lower] += 1
		}
	}
}

func GetPageWords(r io.Reader) (Histogram, error) {
	doc, err := html.Parse(r)
	if err != nil {
		return nil, err
	}

	plot := make(Histogram)
	ExtractToHistogram(doc, &plot)
	return plot, nil
}

var ignoreTags = map[string]bool{
	"script": true,
	"style":  true,
	"head":   true,
}

func ExtractToHistogram(n *html.Node, into *Histogram) {
	if n.Type == html.ElementNode && ignoreTags[n.Data] {
		return
	}

	if n.Type == html.TextNode {
		AddToHistogram(n.Data, into)
	}

	for c := n.FirstChild; c != nil; c = c.NextSibling {
		ExtractToHistogram(c, into)
	}
}
