import hmac
import os
from hashlib import sha1
from urllib.parse import urlencode
from urllib.request import urlopen
import json
from collections import namedtuple

HOSTNAME = 'http://timetableapi.ptv.vic.gov.au'

class ResultCollection(object):
    def __init__(self, collection):
        self.collection = collection

    def __repr__(self):
        return json.dumps([el._asdict() for el in self.collection], indent=2)

class Collection(object):

    def __init__(self, raw_collection):
        self.obj_collection = Collection.__objectify(
            raw_collection,
            self.key,
            self.namedtuple_class
        )

    @property
    def key(self):
        raise NotImplementedError('Must supply api collection key')

    @property
    def namedtuple_class(self):
        raise NotImplementedError('Must supply the namedtuple class')

    def search(self, search_key, search_value):
        results = []
        for element in self.obj_collection:
            if search_value in getattr(element, search_key):
                results.append(element)
        return ResultCollection(results)

    def __repr__(self):
        return json.dumps([element._asdict() for element in self.obj_collection], indent=2)

    @staticmethod
    def __objectify(collection, collection_key, namedtuple_class):
        results = []
        for element in collection[collection_key]:
            results.append(namedtuple_class(**element))
        return results

class RouteTypes(Collection):

    @property
    def namedtuple_class(self):
        return namedtuple(
            'route_type',
            [
                'route_type_name',
                'route_type'
            ]
        )

    @property
    def key(self):
        return 'route_types'

class Routes(Collection):

    @property
    def namedtuple_class(self):
        return namedtuple(
            'route',
            [
                'route_type',
                'route_id',
                'route_name',
                'route_number',
                'route_gtfs_id'
            ]
        )

    @property
    def key(self):
        return 'routes'

class Stops(Collection):

    @property
    def namedtuple_class(self):
        return namedtuple(
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

    @property
    def key(self):
        return 'stops'

class Departures(Collection):

    @property
    def namedtuple_class(self):
        return namedtuple(
            'departure',
            [
              'stop_id',
              'route_id',
              'run_id',
              'disruption_ids',
              'direction_id',
              'scheduled_departure_utc',
              'estimated_departure_utc',
              'at_platform',
              'platform_number',
              'flags',
              'departure_sequence'
            ]
        )

    @property
    def key(self):
        return 'departures'

class Disruptions(Collection):

    @property
    def namedtuple_class(self):
        return namedtuple(
            'disruption',
            [
              'disruption_id',
              'title',
              'url',
              'description',
              'disruption_status',
              'disruption_type',
              'published_on',
              'last_updated',
              'from_date',
              'to_date',
              'routes',
              'stops',
              'colour',
              'display_on_board',
              'display_status',
            ]
        )

class TrainDisruptions(Disruptions):

    def __init__(self, raw_collection):
        super().__init__(raw_collection['disruptions'])

    @property
    def key(self):
        return 'metro_train'

class Client:
    'Access information from the public PTV API'

    def __init__(self, dev_id='', api_key=''):
        self.dev_id = dev_id
        self.api_key = api_key

    def credentials(self):
        return {
            'dev_id':  self.dev_id,
            'api_key': self.api_key
        }

    def status_check(self):
        return self.__send_request('/v2/healthcheck')

    def route_types(self):
        return RouteTypes(self.__send_request('/v3/route_types'))

    def search_train_routes_by_name(self, substr):
        self.routes = Routes(
            self.__send_request('/v3/routes', params={'route_types': [0]})
        )
        return self.routes.search('route_name', substr)

    def train_stops_by_name(self, substr, route_id=3, route_type=0):
        stops = Stops(
            self.__send_request(f'/v3/stops/route/{route_id}/route_type/{route_type}')
        )
        return stops.search('stop_name', substr)

    def stops(self, route_id=0, route_type=0):
        return Stops(
            self.__send_request(f'/v3/stops/route/{route_id}/route_type/{route_type}')
        )

    def disruptions(self):
        return TrainDisruptions(
            self.__send_request('/v3/disruptions')
        )

    def disruptions_for_stop(self, route_id, stop_id):
        return TrainDisruptions(
            self.__send_request(f'/v3/disruptions/route/{route_id}/stop/{stop_id}')
        )

    def departures(self, route_type=0, stop_id=1071):
        return Departures(
            self.__send_request(f'/v3/departures/route_type/{route_type}/stop/{stop_id}')
        )

    def departures_for_route(self, route_type=0, stop_id=1071, route_id=3):
        return Departures(
            self.__send_request(f'/v3/departures/route_type/{route_type}/stop/{stop_id}/route/{route_id}')
        )

    def __send_request(self, endpoint, params={}, to_json=False):
        url = URL.generate(endpoint, params=params, **self.credentials())
        print(f'sending to url {url}')
        with urlopen(url) as f:
            result = json.loads(f.read().decode('UTF-8'))
            if to_json:
                return json.dumps(result, indent=2)
            else:
                return result


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


