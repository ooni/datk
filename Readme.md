# OONI DATK

The OONI Data Analysis ToolKit is a set of python tools that will make your
life easier when analyzing OONI data.

**WARNING** This is still under heavy development and the API may (and WILL) change unexpectedly without any prior notice.

Do not depend on this in your own software, just yet!

If you do have feedback, even about the API, do not hesitate to open an issue!

```
pip install oonidatk
```


## Downloading Data

```
dc = DataCache()
msmt_ids = download_measurements(dc,
  query={
    'test_name': 'web_connectivity',
    'probe_cc': 'ZW',
    'since': '2019-01-20'
  }
)
```
