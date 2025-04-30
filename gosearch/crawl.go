package main

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"golang.org/x/net/html"
	"log"
	"net/http"
)

func crawl(target *sql.DB, root string, keywords []string, bounded bool, maxDepth int, black_subdomains []string, black_urls []string) {
	seen := make(map[string]bool)
	counter := 1

	queue := NewQueue()
	queue.Enqueue(root, 0)
	for queue.Size() > 0 {
		url, depth := queue.Dequeue()
		log.Printf("%v\t%v\t%v\n", counter, depth, url)

		res, err := http.Get(root)
		if err != nil {
			log.Printf("[ERROR] Couldn't retrieve page: %v\n", err)
		} else {
			if res.StatusCode != http.StatusOK {
				log.Printf("[ERROR] Couldn't retrieve page (got code %v)\n", res.StatusCode)
			} else {
				doc, err := html.Parse(res.Body)
				if err != nil {
					log.Printf("[ERROR] Couldn't parse HTML: %v\n", err)
				} else {
					page := NewPage(url, doc, keywords)
					if len(page.Terms) > 0 {
						err = DBAddPage(target, page)
						if err != nil {
							log.Fatalf("Couldn't add page to database. Quitting...")
						}
					}

					if !bounded || depth < maxDepth {
						links := GetPageLinks(doc)
						for _, link := range links {
							link = CompleteLink(link, url)
							if link != "" && !seen[link] {
								row, err := DBGetPage(target, link)
								if err != nil {
									log.Fatalf("Couldn't query database. Quitting...")
								}

								if row == nil {
									queue.Enqueue(link, depth+1)
								}

								seen[link] = true
							}
						}
					}
				}
			}

			res.Body.Close()
		}
	}
}
