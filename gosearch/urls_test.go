package main

import "testing"

func TestGetDomain(t *testing.T) {
	url := "https://en.wikipedia.org/wiki/Greece"
	d := GetDomain(url)
	if d != "en.wikipedia.org" {
		t.Errorf("Didn't get expected domain. Got: %v", d)
	}

	url = "https://google.com"
	d = GetDomain(url)
	if d != "google.com" {
		t.Errorf("Didn't get expected domain. Got: %v", d)
	}

	bad := "asdjfjadf/"
	d = GetDomain(bad)
	if d != "" {
		t.Errorf("Didn't get expected error value. Got: %v", d)
	}
}

func TestGetDomainSubdomain(t *testing.T) {
	url := "https://en.wikipedia.org/wiki/Greece"
	d, s := GetDomainSubdomain(url)
	if d != "wikipedia.org" || s != "en" {
		t.Errorf("(1)Didn't get expected domain and subdomain. Got: %v, %v", d, s)
	}

	url = "https://google.com"
	d, s = GetDomainSubdomain(url)
	if d != "google.com" || s != "" {
		t.Errorf("(2)Didn't get expected domain and subdomain. Got: %v, %v", d, s)
	}

	bad := "asdjfjadf/"
	d, s = GetDomainSubdomain(bad)
	if d != "" || s != "" {
		t.Errorf("Didn't get expected error values. Got: %v, %v", d, s)
	}
}

func TestCompleteLink(t *testing.T) {
	link := "https://en.wikipedia.org/wiki/Greece"
	comp := CompleteLink(link, "https://wikipedia.org")
	if comp != "https://en.wikipedia.org/wiki/Greece/" {
		t.Errorf("(1)Didn't get expected completed link. Got %v", comp)
	}

	link = "https://google.com/"
	comp = CompleteLink(link, "https://google.com")
	if comp != "https://google.com/" {
		t.Errorf("(2)Didn't get expected completed link. Got %v", comp)
	}

	link = "/hello"
	comp = CompleteLink(link, "https://google.com")
	if comp != "https://google.com/hello/" {
		t.Errorf("(3)Didn't get expected completed link. Got %v", comp)
	}

	link = "nowhere"
	comp = CompleteLink(link, "https://google.com")
	if comp != "" {
		t.Errorf("(1)Didn't get expected error value. Got %v", comp)
	}

	link = "https://nowhere.com"
	comp = CompleteLink(link, "https://google.com")
	if comp != "" {
		t.Errorf("(2)Didn't get expected error value. Got %v", comp)
	}
}
