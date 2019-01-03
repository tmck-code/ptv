from hashlib import sha1
import hmac
import binascii

def getUrl(request):
    devId = 2
    key = '7car2d2b-7527-14e1-8975-06cf1059afe0'
    request = request + ('&' if ('?' in request) else '?')
    raw = request+'devid={0}'.format(devId)
    hashed = hmac.new(key, raw, sha1)
    signature = hashed.hexdigest()
    return 'http://tst.timetableapi.ptv.vic.gov.au'+raw+'&signature={1}'.format(devId, signature)

# This returns 
# 'http://tst.timetableapi.ptv.vic.gov.au/v2/healthcheck?devid=2&signature=7a98b58785754b6af5fa51899666e767085b8ef4'
print getUrl('/v2/healthcheck')

