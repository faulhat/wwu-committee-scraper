import re


# Result of searching a document
# Contains a map of terms to number of appearances, the start position
#   of the first term, end position, and the total number of keywords
class SearchRes:
    def __init__(self, appearances: dict[str, int], first: int, end: int, total: int):
        self.appearances = appearances
        self.first = first
        self.end = end
        self.total = total


# Search a document for given keywords
# TODO:  Make this use a trie
def search(text: str, terms: list[str]) -> SearchRes:
    appearances = {}
    first = -1
    end = -1
    total = 0

    for term in terms:
        pattern = re.compile(f"(?<!\w){term}(?!\w)")
        cur = 0
        while match := pattern.search(text, cur):
            appearances[term] = 1 + appearances.get(term, 0)
            if first < 0 or match.end() < first:
                first = match.start()
                end = match.end()

            cur = match.end()
            total += 1

    return SearchRes(appearances, first, end, total)
