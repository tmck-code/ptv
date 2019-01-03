import hmac
import os

HOSTNAME = 'http://timetableapi.ptv.vic.gov.au'

def generate_url(endpoint, dev_id='', api_key='', hostname=HOSTNAME):
    print(endpoint, dev_id, api_key)
    raw = f'{endpoint}?devid={dev_id}'
    signature = hmac.new(api_key.encode('UTF-8'), raw.encode('UTF-8'), digestmod='sha1').hexdigest()

    return f'{hostname}{endpoint}?devid={dev_id}&signature={signature}'

