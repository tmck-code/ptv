import hmac
import os
from hashlib import sha1
from urllib.parse import urlencode
from urllib.request import urlopen
import json
from collections import namedtuple

HOSTNAME = 'https://timetableapi.ptv.vic.gov.au'

RouteType = namedtuple(
    'route_type',
    [
        'route_type_name',
        'route_type'
    ]
)

Route = namedtuple(
    'route',
    [
        'route_type',
        'route_id',
        'route_name',
        'route_number',
        'route_gtfs_id'
    ]
)

Stop = namedtuple(
    'stop',
    [
      'disruption_ids',
      'stop_suburb',
      'stop_name',
      'stop_id',
      'route_type',
      'stop_latitude',
      'stop_longitude',
      'stop_sequence'
    ]
)

class Client:
    def __init__(self, dev_id='', api_key=''):
        self.dev_id = dev_id
        self.api_key = api_key

    def credentials(self):
        return {
            'dev_id': self.dev_id,
            'api_key': self.api_key
        }
    
    def status_check(self):
        return self.__send_request('/v2/healthcheck')

    def route_types(self):
        return Client.__objectify(
            self.__send_request('/v3/route_types'),
            'route_types',
            RouteType
        )

    def stops(self, route_id, route_type):
        return Client.__objectify(
            self.__send_request(f'/v3/stops/route/{route_id}/route_type/{route_type}'),
            'stops',
            Stop
        )

    def route(self):
        result = self.__send_request('/v3/routes/4755')
        return Route(**result['route'])

    def routes_by_type(self):
        return Client.__objectify(
            self.__send_request('/v3/routes', params={'route_types': [0]}),
            'routes',
            Route
        )

    def train_routes_by_name(self, substr):
        routes = self.routes_by_type()
        results = Client.__search_collection(routes, 'route_name', substr)
        return results

    def train_stops_by_name(self, substr):
        stops = self.stops(3, 0)
        results = Client.__search_collection(stops, 'stop_name', substr)
        return results

    def __send_request(self, endpoint, params={}, to_json=False):
        url = URL.generate(endpoint, params=params, **self.credentials())
        print(f'sending to url {url}')
        with urlopen(url) as f:
            result = json.loads(f.read().decode('UTF-8'))
            if to_json:
                return json.dumps(result, indent=2)
            else:
                return result

    @staticmethod
    def __objectify(collection, collection_key, namedtuple_class):
        results = []
        for element in collection[collection_key]:
            results.append(namedtuple_class(**element))
        return results

    @staticmethod
    def __search_collection(collection, search_key, search_value):
        results = []
        for element in collection:
            if search_value in getattr(element, search_key):
                results.append(element)
        return results



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


