from hashlib import sha1 import hmac
import binascii
import os

def get_url(request):
    dev_id = os.getenv('PTV_API_USER_ID')
    key = os.getenv('PTV_API_KEY')
    request = request + ('&' if ('?' in request) else '?')
    raw = request+'devid={0}'.format(dev_id)
    hashed = hmac.new(key, raw, sha1)
    signature = hashed.hexdigest()
    return 'http://tst.timetableapi.ptv.vic.gov.au'+raw+'&signature={1}'.format(dev_id, signature)

print(get_url('/v2/healthcheck'))

