import hmac

def ptv_url(endpoint, dev_id, key):
    raw = f'{endpoint}?devid={dev_id}'
    signature = hmac.new(key.encode('UTF-8'), raw.encode('UTF-8'), digestmod='sha1').hexdigest()

    return f'http://tst.timetableapi.ptv.vic.gov.au{endpoint}?devid={dev_id}&signature={signature}'

# This returns
# 'http://tst.timetableapi.ptv.vic.gov.au/v2/healthcheck?devid=2&signature=7a98b58785754b6af5fa51899666e767085b8ef4'
print(ptv_url('/v2/healthcheck', dev_id=2, key='7car2d2b-7527-14e1-8975-06cf1059afe0'))

