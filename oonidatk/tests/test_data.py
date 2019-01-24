import pytest
from oonidatk import download_measurements, DataCache

def test_download_measurements():
    dc = DataCache()
    msmt_ids = download_measurements(dc, query={'test_name': 'facebook_messenger', 'since': '2019-01-20', 'until': '2019-01-25', 'probe_cc': 'ZW'})
    assert len(msmt_ids) > 0
    dc.delete()

def test_download_measurements_extract():
    dc = DataCache()
    msmts = download_measurements(dc, query={'test_name': 'facebook_messenger', 'since': '2019-01-20', 'until': '2019-01-25', 'probe_cc': 'ZW'}, extract=True)
    print(msmts)
    assert len(msmts) > 0
    dc.delete()
