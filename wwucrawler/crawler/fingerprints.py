import re, requests
from bs4 import BeautifulSoup
import numpy as np


def get_words(text):
    return re.findall(r"\w+", text)


def calc_comparison_fingerprint(text, word2pos):
    fingerprint = np.zeros((len(word2pos),))
    words = re.findall(r"\w+", text)
    for word in words:
        word = word.lower()
        if word in word2pos:
            fingerprint[word2pos[word]] += 1

    fingerprint /= len(words)
    return fingerprint


def gen_canonical_fingerprints(canon_texts):
    common_words = set(get_words(canon_texts[0]))
    for text in canon_texts[1:]:
        common_words = common_words.union(set(get_words(text)))

    w2p = {}
    for word in common_words:
        w2p[word] = len(w2p)

    return [calc_comparison_fingerprint(text, w2p) for text in canon_texts], w2p


def min_set_distance(text, canon_fps, w2p):
    mindist = np.inf
    text_fp = calc_comparison_fingerprint(text, w2p)
    for fp in canon_fps:
        distance = np.sum(np.abs(text_fp - fp))
        mindist = min(mindist, distance)

    return mindist


def texts_from_urls(urls):
    texts = []
    for url in urls:
        print(f"Retrieving canonical sample {url}")
        res = None
        try:
            res = requests.get(url, timeout=(3, 10))
            res.raise_for_status()
        except TimeoutError:
            print("Timed out")
        except requests.exceptions.RequestException as e:
            print(f"Couldn't retrieve page: {e.__str__()}")

        if res is not None and res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            texts.append(soup.text)

    return texts
