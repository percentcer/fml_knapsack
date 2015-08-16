import requests
import uuid

from bs4 import BeautifulSoup
from collections import OrderedDict

FML_URL = "http://fantasymovieleague.com/researchvault?section=box-office"

DOLLAR_MAGNITUDES = {"B": 1e9, "M": 1e6, "K": 1e3}

def _get_rows(url):
    print("fetching {}".format(url))
    resp = requests.get(url)
    resp.raise_for_status()
    doc = resp.text
    soup = BeautifulSoup(doc, 'html.parser')
    tables = soup.find_all('tbody')
    return [[r.find('img')] + [d.text for d in list(r)] for t in tables for r in t.find_all('tr')]


def _fml2table(lookup):
    for img, rank, title, estimate, _, prev, *_ in _get_rows(FML_URL):
        title, cost = title.strip().split('FB$')
        estimate = None if estimate == '-' else float(estimate[1:-1]) * DOLLAR_MAGNITUDES[estimate[-1]]
        prev = None if prev == '-' else float(prev[1:-1]) * DOLLAR_MAGNITUDES[prev[-1]]
        title = title.upper()

        lookup[title] = {
            'cost': int(cost),
            'proj': estimate,
            'prev': prev,
            'poster': img.attrs['src'] if img else None,
            'id': str(uuid.uuid4())[:8]} # todo: title conflicts


def projections_table():
    lookup = OrderedDict()
    _fml2table(lookup)

    for k, v in lookup.items():
        if v['proj'] is None:
            if v['prev'] is None:
                print("warning: {} has no projection".format(k))
            else:
                # reduce previous week's value by 40%
                lookup[k]['proj'] = lookup[k]['prev'] * 0.4

    return lookup
