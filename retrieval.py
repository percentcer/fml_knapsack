import requests
from bs4 import BeautifulSoup
from datetime import date
import re

# PBO_URL = "http://pro.boxoffice.com/statistics/long_term_predictions?w=1"
PBO_DAILY = "http://pro.boxoffice.com/statistics/bo_numbers/early_estimate/{}".format(date.today().isoformat())
FML_URL = "http://fantasymovieleague.com/researchvault?section=bux"

def pbo2table(lookup):
    doc = requests.get(PBO_DAILY).text
    soup = BeautifulSoup(doc, 'html.parser')
    tables = soup.find_all('tbody')
    rows = [[d.text for d in list(r)] for t in tables for r in t.find_all('tr')]

    date_paren_pat = re.compile(r'\s*\(\d+\)$')

    for rank, name, proj, *_ in rows:
        proj = proj.strip('$').replace(',', '')
        name = name.strip().upper()
        name = date_paren_pat.sub('', name) #remove pbo's date stuff
        if name in lookup:
            lookup[name]['proj'] = int(proj)

def fml2table(lookup):
    doc = requests.get(FML_URL).text
    soup = BeautifulSoup(doc, 'html.parser')
    table = soup.find('tbody')
    rows = [[d.text for d in list(r)] for r in table.find_all('tr')]
    for rank, title, cost, *_ in rows:
        title = title.strip().split('FB$')[0].upper()
        lookup[title] = {'cost': int(cost), 'proj': None}

def projections_table():
    lookup = {}
    fml2table(lookup)
    pbo2table(lookup)

    for k,v in lookup.items():
        if v['proj'] is None:
            print("warning: {} has no projection".format(k))
            lookup[k]['proj'] = 1000000

    return lookup
