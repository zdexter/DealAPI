import urllib2

"""
Unit tests for the Tornado application living in api.py

Nose will pick up any function ending with _test
    (or any function or class whose name matches ((?:^|[\\b_\\.-])[Tt]est) )
    Reference:  http://nose.readthedocs.org/en/latest/writing_tests.html
"""

def urlconf_test():
    """
    Make an HTTP GET request to /my_merchant
        Expected return value: List of deals offered by my_merchant.
    """
    base_url = 'http://localhost:8000'
    # TODO:  Test output for a variety of cases
    response = urllib2.urlopen('%s/my_merchant' % base_url)
    if response.read():
        pass