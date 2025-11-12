import re
from queue import Queue


# Result of searching a document
# Contains a map of terms to number of appearances, the start position
#   of the first term, end position, and the total number of keywords
class SearchRes:
    def __init__(self, appearances, first, end, total):
        self.appearances = appearances
        self.first = first
        self.end = end
        self.total = total


# Search with keywords of varying priority
#  Keywords on the first priority tier out of n will count for n points each,
#  those on the second tier count for n-1, and so on.
def tiered_search(text, keyword_list):
    score = 0
    result = search(text, keyword_list[0])
    result.total *= len(keyword_list)
    for i, tier in enumerate(keyword_list[1:]):
        t_res = search(text, tier)
        for term, num in t_res.appearances.items():
            if term in result.appearances:
                result.appearances[term] += num
            else:
                result.appearances[term] = num

        if result.first == -1:
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


class TrieNode:
    def __init__(self, terminal=False, term=None, occurrences=0, node=None):
        self.terminal = terminal
        self.term = term
        self.node = node


class Trie:
    def __init__(self, terms):
        self.terms = terms
        self.root = [TrieNode() for i in range(256)]
        for term in terms:
            self.add_term(term)

    def print_all(self):
        q = Queue()
        q.put(("", self.root))
        while not q.empty():
            s, n = q.get()
        for i, b in enumerate(n):
            t = s + chr(i)
            if b.node is not None:
                q.put((t, b.node))

            if b.terminal:
                print(f"{t}, {b.term}")


    def add_term(self, term):
        for c in term:
            if ord(c) > 255:
                raise Exception("Tries can only use ASCII terms.")

        n = self.root
        for i, c in enumerate(term):
            b = ord(c)
            if i == len(term) - 1:
                n[b].terminal = True
                n[b].term = term
                return n[b]
            else:
                if n[b].node is None:
                    n[b].node = [TrieNode() for i in range(256)]

                n = n[b].node

    def get_node(self, term):
        n = self.root
        for i, c in enumerate(term):
            b = ord(c)
            if b > 255:
                return None
            elif i == len(term) - 1:
                return n[b] if n[b].terminal else None
            elif n[b].node is None:
                return None
            else:
                n = n[b].node

    def has_term(self, term):
        return self.get_node(term) is not None

    def search(self, text):
        appearances = {}
        first = -1
        end = -1
        total = 0

        i = 0
        for i in range(len(text)):
            n = self.root
            for j, c in enumerate(text[i:]):
                b = ord(c)
                if b > 255 or n[b].node is None:
                    break
                elif n[b].terminal:
                    if first < 0:
                        first = i
                        end = i + j

                    appearances[n[b].node.term] = 1 + appearances.get(n[b].node.term, 0)
                    total += 1

                n = n[b].node

        return SearchRes(appearances, first, end, total)
