import requests
from bs4 import BeautifulSoup
from datetime import date
import re

PBO_DAILY_URL = "http://pro.boxoffice.com/statistics/bo_numbers/early_estimate/{}".format(date.today().isoformat())
FML_URL = "http://fantasymovieleague.com/researchvault?section=bux"


def _get_rows(url):
    print("fetching {}".format(url))
    resp = requests.get(url)
    resp.raise_for_status()
    doc = resp.text
    soup = BeautifulSoup(doc, 'html.parser')
    tables = soup.find_all('tbody')
    return [[d.text for d in list(r)] for t in tables for r in t.find_all('tr')]


def _fml2table(lookup):
    for rank, title, cost, *_ in _get_rows(FML_URL):
        title = title.strip().split('FB$')[0].upper()
        lookup[title] = {'cost': int(cost), 'proj': None}


def _pbo2table(lookup):
    # for removing pbo's date stuff
    date_paren_pat = re.compile(r'\s*\(\d+\)$')

    for rank, name, proj, *_ in _get_rows(PBO_DAILY_URL):
        proj = proj.strip('$').replace(',', '')
        name = name.strip().upper()
        name = date_paren_pat.sub('', name)
        if name in lookup:
            lookup[name]['proj'] = int(proj)


def projections_table():
    lookup = {}
    _fml2table(lookup)
    _pbo2table(lookup)

    for k, v in lookup.items():
        if v['proj'] is None:
            print("warning: {} has no projection".format(k))
            lookup[k]['proj'] = 300000

    return lookup
