import unittest

# import helper
from lib import api

class TestAPI(unittest.TestCase):

    def test_url(self):
        # This is the original return value and input variables used in the
        # Python 2 code example in the official docs
        expected = 'http://tst.timetableapi.ptv.vic.gov.au/v2/healthcheck?devid=2&signature=7a98b58785754b6af5fa51899666e767085b8ef4'
        result = api.generate_url(
            '/v2/healthcheck',
            dev_id=2,
            api_key='7car2d2b-7527-14e1-8975-06cf1059afe0',
            hostname='http://tst.timetableapi.ptv.vic.gov.au'
        )
        self.assertEqual(expected, result)

