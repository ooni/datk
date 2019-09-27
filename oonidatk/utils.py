from urllib.parse import urlencode, quote

import json
import zipfile
import itertools
import urllib.parse
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

class TestLists():
    def __init__(self):
        self.url_set = set()
        self.by_country = {}

    def add_from_csv(self, in_file, country_code):
        if country_code in self.by_country:
            raise Exception("Country already loaded")

        self.by_country[country_code] = []
        # We wrap it in TextIOWrapper so that it's not binary and csv is happy
        csv_reader = csv.DictReader(
                TextIOWrapper(in_file),
                fieldnames=TEST_LIST_HEADER,
                delimiter=',',
                quotechar='"'
        )
        next(csv_reader)
        for row in csv_reader:
            self.url_set.add(row['url'])
            self.by_country[country_code].append(dict(row))

    def get_most_similar_url(self, url):
        if url in self.url_set:
            return url

        p = urllib.parse.urlparse(url)
        permutations = itertools.product(
            ['https://', 'http://'],
            [p.netloc if p.netloc.startswith('www.') else 'www.' + p.netloc,
             p.netloc.replace('www.', '')],
            [p.path.rstrip('/'),
             p.path if p.path.endswith('/') else p.path + '/',
             p.path + '?' + p.query + p.fragment]
        )
        for scheme, host, path in permutations:
            attempt = '{}{}{}'.format(scheme, host, path)
            if attempt in self.url_set:
                return attempt

        return None

    def get_urls(self, country_code, category_codes=[], include_global=True):
        urls = []
        if country_code in self.by_country:
            for url in self.by_country[country_code]:
                if len(category_codes) > 0 and url['category_code'] not in category_codes:
                    continue
                urls.append(url['url'])

        if include_global is True:
            for url in self.by_country['GLOBAL']:
                if len(category_codes) > 0 and url['category_code'] not in category_codes:
                    continue
                urls.append(url['url'])
        return urls

def load_citizenlab_test_lists(zip_path=None):
    tl = TestLists()

    if zip_path is None:
        r = requests.get(TEST_LISTS_URL)
        zip_fh = BytesIO(r.content)
    else:
        zip_fh = open(zip_path, 'rb')

    z = zipfile.ZipFile(zip_fh)
    for name in z.namelist():
        if not name.endswith('.csv'):
            continue

        p = Path(name)
        country_code = p.stem.upper()
        if len(country_code) == 2 or country_code == 'GLOBAL':
            print('loading {}'.format(name))
            with z.open(name) as in_file:
                tl.add_from_csv(in_file, country_code)
    return tl

def ooni_run_websites_link(urls):
    base_url = "https://run.ooni.io/nettest"
    ta = {
        'urls': list(urls)
    }

    query = {
        'tn': 'web_connectivity',
        'mv': '1.2.0',
        'ta': json.dumps(ta)
    }
    return base_url + '?' + urllib.parse.urlencode(query)


