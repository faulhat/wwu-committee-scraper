import re


# Result of searching a document
# Contains a map of terms to number of appearances, the start position
#   of the first term, end position, and the total number of keywords
class SearchRes:
    def __init__(self, appearances, first, end, total):
        self.appearances = appearances
        self.first = first
        self.end = end
        self.total = total


def tiered_search(text, keyword_list):
    score = 0
    result = search(text, keyword_list[0])
    result.total *= len(keyword_list)
    for i, tier in enumerate(keyword_list[1:]):
        t_res = search(text, tier)
        result.appearances |= t_res.appearances
        if result.first == -1 or t_res.first < result.first:
            result.first = t_res.first
            result.end = t_res.end
        
        result.total += (len(keyword_list) - i - 1) * t_res.total
    
    return result


# Search a document for given keywords
# TODO:  Make this use a trie
def search(text, terms):
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
