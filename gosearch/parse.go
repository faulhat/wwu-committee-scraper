package main

import (
	"golang.org/x/net/html"
	"regexp"
	"strings"
)

type Histogram = map[string]int

func GetPageText(root *html.Node) string {
	var b strings.Builder
	ExtractText(root, &b)
	return b.String()
}

func ExtractText(n *html.Node, b *strings.Builder) {
	if n.Type == html.ElementNode && ignoreTags[n.Data] {
		return
	}

	data := strings.TrimSpace(n.Data)
	if n.Type == html.TextNode && data != "" {
		b.WriteString(data + " ")
	}

	for c := n.FirstChild; c != nil; c = c.NextSibling {
		ExtractText(c, b)
	}
}

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

func GetPageWords(root *html.Node) Histogram {
	plot := make(Histogram)
	ExtractToHistogram(root, &plot)
	return plot
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

func GetPageLinks(root *html.Node) []string {
	links := make([]string, 0)
	ExtractLinks(root, &links)
	return links
}

func ExtractLinks(n *html.Node, into *[]string) {
	if n.Type == html.ElementNode && n.Data == "a" {
		for _, attr := range n.Attr {
			if attr.Key == "href" {
				*into = append(*into, attr.Val)
				break
			}
		}
	}

	for c := n.FirstChild; c != nil; c = c.NextSibling {
		ExtractLinks(c, into)
	}
}
