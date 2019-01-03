import unittest
import os

# import helper
from lib import api

class TestAPI(unittest.TestCase):

    def test_signature(self):
        expected = 'a73c9a5b12daad6b0d591604caec1ba7a9679bb7'
        endpoint = 'https://timetableapi.ptv.vic.gov.au/v2/healthcheck'
        devid = '3000972'
        api_key = os.getenv('PTV_API_KEY')
        result = api.URL.generate_signature(endpoint, devid, api_key)
        self.assertEqual(expected, result)
        

    # def test_url(self):
    #     # This is the original return value and input variables used in the
    #     # Python 2 code example in the official docs
    #     expected = 'http://tst.timetableapi.ptv.vic.gov.au/v2/healthcheck?devid=2&signature=7a98b58785754b6af5fa51899666e767085b8ef4'
    #     result = api.URL.generate(
    #         '/v2/healthcheck',
    #         dev_id=2,
    #         api_key='7car2d2b-7527-14e1-8975-06cf1059afe0',
    #         hostname='http://tst.timetableapi.ptv.vic.gov.au'
    #     )
    #     self.assertEqual(expected, result)

