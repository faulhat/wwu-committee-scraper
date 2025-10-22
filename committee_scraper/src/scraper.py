from typing import Any

import requests
import time
import sys
from bs4 import BeautifulSoup
from sqlite3 import Connection
from google import genai

import utils

summarize_prompt = """
Summarize the main content of the following webpage HTML in exactly one sentence (between 10 and 25 words).
Ignore HTML tags, navigation bars, headers, footers, and boilerplate content.
Do not include explanations, introductions, or any formatting.
Return only the summary sentence, and one additional line following stating whether the website directly references a committee or not.
"""

extract_prompt = """
Extract student committee positions from the following university webpage text.

Return ONLY a comma seperated list of each committee title that is available on the website.

Only include positions explicitly labeled or clearly implied to be STUDENT roles on committees.

If no student committee positions are clearly mentioned, or if the page does not reference any committees, return the following: None

Do not include explanations, introductions, or any formatting.
"""


class Scraper:
    def __init__(self, model: str, score_threshold: int, db_connection: Connection):

        self.model = "gemini-2.5-flash"
        self.client = genai.Client(api_key="AIzaSyBAjgK61OxLfKpkgX9yzIq67GKWA3klEnc")

        self.db_connection = db_connection
        self.score_threshold = score_threshold / 100
        self.URLS = []
        self.iteration = 1

    def fetch_urls(self):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT url FROM pages WHERE score > ? ORDER BY score desc",
            (self.score_threshold,)
        )
        rows = cursor.fetchall()
        self.URLS = [row[0] for row in rows]
        cursor.close()

    def scrape(self):
        cursor = self.db_connection.cursor() if self.db_connection is not None else None
        for URL in self.URLS:
            current_pd = self.PageData(URL, self)
            current_pd.run()
            current_pd.print_state()
            if cursor is not None:
                try:
                    contact = "\nContact: " + utils.extract_emails(current_pd.emails) if len(current_pd.emails) > 0 else ""
                    cursor.execute("UPDATE pages SET summary_before = (?), summary_keyword = ?, summary_after = ? "
                                   "WHERE url = (?)",
                                   (current_pd.summary,
                                    contact,
                                    current_pd.positions,
                                    current_pd.url))
                    self.db_connection.commit()
                except ConnectionError as e:
                    print(f'\nURL: {URL} : {e.__str__()}')
            self.iteration += 1
        cursor.close()

    class PageData:
        def __init__(self, url: str, scraper):
            self.scraper = scraper
            self.url = url
            self.page = None
            self.soup = None
            self.summary = None
            self.positions = None
            self.doc_links = []
            self.emails = []

        def run(self) -> None:
            self.page = self._set_page()
            if self.page is not None:
                self.soup = BeautifulSoup(self.page, 'html.parser')
                self.soup = self.extract_page_contents()
                self.doc_links = self._set_doc_links()
                self.emails = self._set_emails()
                if self.scraper.model is not None:
                    self.summary = self._set_summary()
                    self.positions = self._set_positions()
                    time.sleep(30)
                else:
                    self.summary = "<N/A>"
                    self.positions = "<N/A>"
            else:
                print(f"Failed to load page: {self.url}")
                self.summary = "<N/A>"
                self.positions = "<N/A>"

        # Extract only a portion of a full pages content.
        def extract_page_contents(self):
            # class=main-content
            content_div = self.soup.find(class_='main-content')
            # class=modular-content
            if not content_div:
                content_div = self.soup.find(class_='modular-content')
            # <main> tag
            if not content_div:
                content_div = self.soup.find('main')
            # HTML body
            if not content_div:
                content_div = self.soup.body or self.soup
            return content_div

        def _set_page(self) -> str | None:
            try:
                req = requests.get(self.url)
                if req.status_code == 200:
                    return req.text
                else:
                    return None
            except Exception as e:
                print(e.__str__, file=sys.stderr)
                return None

        def _set_summary(self) -> str:
            try:
                response = self.scraper.client.models.generate_content(model=self.scraper.model,
                                                        contents=self.soup.get_text(strip=True, separator='\n')
                                                        + summarize_prompt)
            except Exception as e:
                print(e.__str__(), file=sys.stderr)
                return "<N/A>"
            return response.text

        def _set_positions(self) -> str:
            try:
                response = self.scraper.client.models.generate_content(model=self.scraper.model,
                                                        contents=self.soup.get_text(strip=True, separator='\n')
                                                        + extract_prompt)
            except Exception as e:
                print(e.__str__(), file=sys.stderr)
                return "<N/A>"
            return response.text

        def _set_emails(self) -> list[Any]:
            return ([email_obj.text for email_obj in self.soup.find_all("a")
                     if email_obj.text.__contains__("@") and utils.validate_email(email_obj.text)])

        def _set_doc_links(self) -> list[Any]:
            return [file['href'] for file in self.soup.find_all("a", href=True) if file['href'].__contains__('.pdf')]

        def print_state(self) -> None:
            print(
                f'Summary - URL: {self.url}\n    Summary: {self.summary}\n'
                f'    Positions: {self.positions}\n    Emails: {self.emails}\n    Doc Links: {self.doc_links}')
