import requests
import sys
from bs4 import BeautifulSoup
from sqlite3 import Connection
from ollama import Client
import utils

summarize_prompt = """Summarize the following webpage content in exactly one sentence, between 10 and 25 words.
Do not include any explanations, introductions, or markdown formatting."""

extract_prompt = """Extract a list of STUDENT committee positions from the following university webpage text.
Return ONLY the matching results in Python list format like: [position, position].
Only include entries that:
- Clearly refer to positions on committees that are for Students.
- Follow the format of being listed as 'X at large student positions, x Students at large, etc.' or inside of an html table.
If no clear student positions are found, return [].
DO NOT include explanations or extra text.
"""


class Scraper:
    def __init__(self, model: str, score_threshold: int, db_connection: Connection):
        self.model = None if model == "None" else model
        self.client = Client()
        self.db_connection = db_connection
        self.score_threshold = score_threshold
        self.URLS = []
        self.iteration = 1

    def fetch_urls(self):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT url FROM pages WHERE score > ? AND summary != ''  ORDER BY score desc",
            (0,)
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
                    cursor.execute("UPDATE pages SET summary = (?) WHERE url = (?)",
                                   (current_pd.summary + contact,
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
                self.doc_links = self._set_doc_links()
                self.emails = self._set_emails()
                if self.scraper.model is not None:
                    self.summary = self._set_summary()
                    self.positions = self._set_positions()
                else:
                    self.summary = "<N/A>"
                    self.positions = "<N/A>"
            else:
                print(f"[DEBUG] Failed to load page: {self.url}")
                self.summary = "<N/A>"
                self.positions = "<N/A>"

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
                response = self.scraper.client.generate(model=self.scraper.model,
                                                        prompt=self.soup.text + summarize_prompt)
            except Exception as e:
                return "<N/A>"
            return response.response

        def _set_positions(self) -> [str]:
            try:
                response = self.scraper.client.generate(model=self.scraper.model,
                                                        prompt=self.soup.text + extract_prompt)
            except Exception as e:
                return "<N/A>"
            return response.response

        def _set_emails(self) -> [str]:
            return ([email_obj.text for email_obj in self.soup.find_all("a")
                     if email_obj.text.__contains__("@") and utils.validate_email(email_obj.text)])

        def _set_doc_links(self) -> [str]:
            return [file['href'] for file in self.soup.find_all("a", href=True) if file['href'].__contains__('.pdf')]

        def print_state(self) -> None:
            print(
                f'Summary - URL: {self.url}\n    Summary: {self.summary}\n'
                f'    Positions: {self.positions}\n    Emails: {self.emails}\n    Doc Links: {self.doc_links}')

