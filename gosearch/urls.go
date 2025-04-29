package main

import "strings"

func GetDomain(url string) string {
	seg := strings.SplitN(url, "/", 4)
	if len(seg) < 3 {
		return ""
	} else {
		return seg[2]
	}
}

func GetDomainSubdomain(url string) (string, string) {
	full_domain := GetDomain(url)
	if full_domain == "" {
		return "", ""
	} else {
		seg := strings.Split(full_domain, ".")
		domain := strings.Join(seg[len(seg)-2:], ".")
		subdomain := ""
		if len(seg) > 2 {
			subdomain = seg[len(seg)-3]
		}

		return domain, subdomain
	}
}
