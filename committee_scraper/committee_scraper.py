import json
import re
import requests
import threading
from bs4 import BeautifulSoup

# Return a list of all links in a webpage.
# Currently used for scraping as.wwu/committees/ for committee websites.
def scrape_suburls(root):
    urls = []
    try:
        root_contents = requests.get(root)
        soup = BeautifulSoup(root_contents.text, "html.parser")
        links = soup.find_all("div", class_="modular-link")
        for link in links:
            a_tag = link.find_all("a")
            for url in a_tag:
                href = url.get("href")
                if href:
                    urls.append(root+href.strip())
    except:
        print('Error fetching root url or scraping root url.')
    return urls


# Returns a list of entries in a text file.
def fetch_list(filename):
    res = []
    try:
        with open(filename, "r", encoding='utf-8') as file:
            for line in file:
                res.append(line.strip().lower())
    except:
        print("invalid filename")
    return res


# Email address validation.
def validate_email(email):
    accepted_special_characters = "!#$%&'*+-/=?^_`{|}~"
    if not str(email).__contains__("@"):
        return False
    decomposed_email = str(email).split("@")
    local = decomposed_email[0]
    domain = decomposed_email[1]
    for char in local:
        ascii_val = ord(char)
        if char in accepted_special_characters or (48 > ascii_val > 57) and (63 > ascii_val > 90) and (97 > ascii_val > 122) and (ascii_val != 126):
            return False
    for char in domain:
        ascii_val = ord(char)
        if (48 > ascii_val > 57) and (63 > ascii_val > 90) and (97 > ascii_val > 122) and (ascii_val != 126):
            return False
    return True


# Used for committee position count. Returns a value based on the string format of scraped element.
def match_format(strform, element_contents):
    count = 0
    res = []
    line_contents = str(element_contents).split(" ")
    format_contents = str(strform).split(" ")
    if len(line_contents) != len(format_contents):
        return [-3]
    try:
        for i in range(len(line_contents)):
            if format_contents[i] == "?":
                res.append(int(line_contents[i]))
            elif format_contents[i].lower() != line_contents[i].lower():
                return [-1]
            count+=1
        if len(res) == 0:
            res.append(count)
        return res
    except:
        return [-2]


def scrape(url, result_dataset, thread_count):

    formats = [
        "? at-large student positions",
        "? at-large student position",
        "? graduate students at-large",
        "? undergraduate students at-large",
        "student at-large",
        "? students at-large",
        "? student at-large",
        "as student senator",
        "student from the centers",
        "as vice president",
        "as president",
        "as senate president"
    ]

    subpage = requests.get(url)
    subsoup = BeautifulSoup(subpage.text, "html.parser")

    positions = subsoup.find_all(string=re.compile("student|Student|students|Students"))
    title = subsoup.find("div", attrs={'class':'modular-container'}).find("h1").text

    position_count = 0
    for position in positions:
        for format in formats:
            current_sum = sum(match_format(format, position.text))
            if current_sum > 0:
                position_count += current_sum

    email_objs = subsoup.find_all("a")
    emails = []
    for email_obj in email_objs:
        if (email_obj.text.__contains__("@")):
            if validate_email(email_obj.text):
                emails.append(email_obj.text)

    result_dataset[thread_count] = [("Committee_url", url), ("Committee_name", title), ("position_count", position_count), ("Emails", emails)]


if __name__=="__main__":

    threads = []
    attr_count = 4
    url_count = 0

    with open("links.txt", "w") as file:
        for line in scrape_suburls('https://as.wwu.edu/committees/'):
            url_count += 1
            file.write(line + '\n')

    urls = fetch_list("links.txt")
    result_dataset = [[0] * attr_count] * url_count

    for i in range(url_count):
        thread = threading.Thread(target=scrape, args=(urls[i], result_dataset, i))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    for i in range(url_count):
        scrape(urls[i], result_dataset, i)

    transformed_data = {
        "committees": [
            {
                "id": count + 1,
                "name": item[1][1],
                "data": {
                    "url": item[0][1],
                    "position_count": item[2][1],
                    "emails": item[3][1]
                }
            }
            for count, item in enumerate(result_dataset)
        ]
    }

    with open("data.json", "w", encoding='utf-8') as file:
        json.dump(transformed_data, file, indent=4)