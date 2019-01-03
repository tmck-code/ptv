import hmac
import os
from urllib.parse import urlencode
from urllib.request import urlopen

HOSTNAME = 'http://timetableapi.ptv.vic.gov.au'

def status_check(dev_id='', api_key=''):
    url = URL.generate('/v2/healthcheck', dev_id=dev_id, api_key=api_key)
    with urlopen(url) as f:
        return f.read().decode('UTF-8')

class URL:

    @staticmethod
    def generate(endpoint, dev_id='', api_key='', hostname=HOSTNAME):
        params = URL.__generate_params(endpoint, dev_id, api_key)
        return f'{hostname}{endpoint}?{params}'

    @staticmethod
    def __generate_signature(endpoint, dev_id, api_key):
        raw = f'{endpoint}?devid={dev_id}'
        hasher = hmac.new(
            api_key.encode('UTF-8'),
            raw.encode('UTF-8'),
            digestmod='sha1'
        )
        return hasher.hexdigest()

    @staticmethod
    def __generate_params(endpoint, dev_id, api_key):
        return urlencode({
            'devid':     dev_id,
            'signature': URL.__generate_signature(endpoint, dev_id, api_key)
        })

