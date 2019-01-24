from urllib.parse import urlencode, quote

def print_explorer_url(e):
    query = ''
    if 'input' in e.keys() and e['input']:
        query = '?input={}'.format(quote(e['input'], safe=''))
    print('https://explorer.ooni.io/measurement/{}{}'.format(e['report_id'], query))
