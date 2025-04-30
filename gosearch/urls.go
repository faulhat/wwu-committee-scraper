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

func StripQuery(url string) string {
	return strings.SplitN(url, "?", 2)[0]
}

func CompleteLink(link string, parent string) string {
	if !(startswith(link, "/") || startswith(link, "http://") || startswith(link, "https://")) {
		return ""
	}

	if !endswith(link, "/") {
		link += "/"
	}

	if startswith(link, "/") {
		link = "https://" + GetDomain(parent) + link
	} else {
		d, _ := GetDomainSubdomain(link)
		p_d, _ := GetDomainSubdomain(parent)
		if d != p_d {
			return ""
		}
	}

	return link
}

func startswith(s string, p string) bool {
	return len(s) >= len(p) && s[:len(p)] == p
}

func endswith(s string, p string) bool {
	return len(s) >= len(p) && s[len(s)-len(p):] == p
}
