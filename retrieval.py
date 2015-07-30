import requests
import re
import uuid

from bs4 import BeautifulSoup
from datetime import date, timedelta
from collections import OrderedDict

yesterday = date.today() - timedelta(1)

PBO_DAILY_URL = "http://pro.boxoffice.com/statistics/long_term_predictions?w=1"
FML_URL = "http://fantasymovieleague.com/researchvault?section=bux"

def _get_rows(url):
    print("fetching {}".format(url))
    resp = requests.get(url)
    resp.raise_for_status()
    doc = resp.text
    soup = BeautifulSoup(doc, 'html.parser')
    tables = soup.find_all('tbody')
    return [[r.find('img')] + [d.text for d in list(r)] for t in tables for r in t.find_all('tr')]


def _fml2table(lookup):
    for img, rank, title, cost, *_ in _get_rows(FML_URL):
        title = title.strip().split('FB$')[0].upper()
        lookup[title] = {
            'cost': int(cost),
            'proj': None,
            'poster': img.attrs['src'] if img else None,
            'id': str(uuid.uuid4())[:8]} # todo: title conflicts


def _pbo2table(lookup):
    # for removing pbo's date stuff
    date_paren_pat = re.compile(r'\s*\(\d+\)$')

    for _, name, proj, *_ in _get_rows(PBO_DAILY_URL):
        proj = proj.strip('$').replace(',', '')
        name = name.strip().upper()
        name = date_paren_pat.sub('', name)
        if name in lookup:
            lookup[name]['proj'] = int(proj)


def projections_table():
    lookup = OrderedDict()
    _fml2table(lookup)
    _pbo2table(lookup)

    for k, v in lookup.items():
        if v['proj'] is None:
            print("warning: {} has no projection".format(k))
            lookup[k]['proj'] = 100000

    return lookup
