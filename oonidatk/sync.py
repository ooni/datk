import tempfile
import logging
import shutil
import os

from multiprocessing.pool import ThreadPool

import requests

from .extractors import extractors, extract_common

OONI_API_BASE_URL = 'https://api.ooni.io/api/v1/'
MEASUREMENTS_PER_PAGE = 100000

class DataCache(object):
    '''
    Will cache downloaded measurements so that they don't have to be
    re-downloaded. It works by downloading them to a temporary directory.
    '''
    def __init__(self):
        self.cache_dir = tempfile.mkdtemp(suffix='oomsmtcache', prefix='tmp')

    def is_cached(self, measurement_id):
        return os.path.exists(os.path.join(self.cache_dir, measurement_id))

    def delete(self):
        shutil.rmtree(self.cache_dir)
        self.cache_dir = None

    def download(self, measurement_id, measurement_url):
        dst_path = os.path.join(self.cache_dir, measurement_id)
        r = requests.get(measurement_url, stream=True)
        if r.status_code == 200:
            with open(dst_path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            return measurement_id
        raise Exception("Failed to download " + measurement_id)

    def download_extract(self, measurement_id, measurement_url):
        dst_path = os.path.join(self.cache_dir, measurement_id)
        r = requests.get(measurement_url)
        with open(dst_path, 'wb') as f:
            f.write(r.content)

        j = r.json()
        test_name = j['test_name']
        if test_name in extractors:
            return extractors[test_name](j)
        return extract_common(j)

def download_measurements(cache, query={}, concurrency=10, extract=False):
    download_func = cache.download
    if extract is True:
        download_func = cache.download_extract

    thread_pool = ThreadPool(concurrency)

    query = dict(query, limit=MEASUREMENTS_PER_PAGE, order_by='test_start_time')
    r = requests.get(
        OONI_API_BASE_URL+'measurements',
        params=query
    )
    j = r.json()
    if j['metadata']['count'] >= MEASUREMENTS_PER_PAGE:
        logging.warning('Your query is very broad. Pagination may be very slow in retrieving this data')

    downloaded_msmts = []
    while True:
        id_url = list(
            filter(
                lambda x: not cache.is_cached(x[0]),
                   map(lambda x: (x['measurement_id'], x['measurement_url']), j['results'])
        ))
        for t in thread_pool.imap_unordered(lambda x: download_func(x[0], x[1]), id_url):
            downloaded_msmts.append(t)

        next_url = j['metadata']['next_url']
        if next_url:
            j = requests.get(next_url).json()
        else:
            break

    return downloaded_msmts
