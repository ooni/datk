from urllib.parse import urlencode, quote

import json
import zipfile
import csv
from io import BytesIO, StringIO, TextIOWrapper
from pathlib import Path

import requests

TEST_LISTS_URL = "https://github.com/citizenlab/test-lists/archive/master.zip"

def print_explorer_url(e):
    query = ''
    if e.get('input', None):
        query = '?input={}'.format(quote(e['input'], safe=''))
    print('https://explorer.ooni.io/measurement/{}{}'.format(e['report_id'], query))

TEST_LIST_HEADER = [
    "url",
    "category_code",
    "category_description",
    "date_added",
    "source",
    "notes"
]

def read_csv(z, name):
    with z.open(name) as in_file:
        # We wrap it in TextIOWrapper so that it's not binary and csv is happy
        csv_reader = csv.DictReader(TextIOWrapper(in_file), fieldnames=TEST_LIST_HEADER, delimiter=',', quotechar='"')
        next(csv_reader)
        return [dict(row) for row in csv_reader]

def load_citizenlab_test_lists():
    test_lists = {}

    r = requests.get(TEST_LISTS_URL)
    z = zipfile.ZipFile(BytesIO(r.content))
    for name in z.namelist():
        if not name.endswith('.csv'):
            continue

        p = Path(name)
        country_code = p.stem.upper()
        if len(country_code) == 2:
            print('loading {}'.format(name))
            test_lists[country_code] = read_csv(z, name)

    return test_lists
