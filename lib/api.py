import hmac
import os
from hashlib import sha1
from urllib.parse import urlencode
from urllib.request import urlopen
import json

HOSTNAME = 'https://timetableapi.ptv.vic.gov.au'

class Client:
    def __init__(self, dev_id='', api_key=''):
        self.dev_id = dev_id
        self.api_key = api_key

    def credentials(self):
        return {
            'dev_id': self.dev_id,
            'api_key': self.api_key
        }

    def train_routes(self):
        return self.__send_request(URL.generate('/v3/routes', params={'route_types': [0]}, **self.credentials()))

    def route_types(self):
        return self.__send_request(URL.generate('/v3/route_types', **self.credentials()))
    
    def status_check(self):
        return self.__send_request(URL.generate('/v2/healthcheck', **self.credentials()))

    def __send_request(self, url):
        print(f'sending to url {url}')
        with urlopen(url) as f:
            return f.read().decode('UTF-8')



class URL:

    @staticmethod
    def generate(endpoint, params={}, dev_id='', api_key='', hostname=HOSTNAME):
        params = URL.__generate_params(endpoint, dev_id, api_key, params=params)
        print('generated URL params')
        print(json.dumps(params, indent=2))
        return f'{hostname}{endpoint}?{params}'

    @staticmethod
    def __generate_params(endpoint, dev_id, api_key, params={}):
        url_params = {
            'devid':     dev_id,
            'signature': URL.generate_signature(endpoint, dev_id, api_key, params=params)
        }
        params.update(url_params)
        return urlencode(url_params)

    @staticmethod
    def generate_signature(endpoint, dev_id, api_key, params={}):
        base_params = {'devid': dev_id }
        raw = f'{endpoint}?{urlencode(base_params)}'
        print(f'generating signature from: "{raw}"')
        hasher = hmac.new(
            api_key.encode('UTF-8'),
            raw.encode('UTF-8'),
            digestmod=sha1
        )
        return hasher.hexdigest()


