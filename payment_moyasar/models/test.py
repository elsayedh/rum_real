import json
import requests

def myrequest(http_verb, url, data=None ):
    moyasar_key ='sk_test_GwH7M35mPJW7X5tyiVYDXpZR6ycuhkNafKXUMKyy'

    if moyasar_key is None:
        raise Exception('API key must be provided')

    request = {
        'method': 'GET',
        'url': url,
        'auth': (moyasar_key, ''),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    if data is not None:
        if http_verb.upper() == 'GET':
            request['params'] = data
        else:
            request['data'] = json.dumps(data)

    res = requests.request(**request)
    if 400 <= res.status_code <= 404:
        json_string = res.text
        json_dict = json.loads(json_string)
        json_dict["http_code"] = res.status_code
        raise Exception(f'{json.dumps(json_dict)}')
    if 500 <= res.status_code <= 504:
        raise Exception(f'API Error with status code: {res.status_code}')
    return res

x=myrequest('get','https://api.moyasar.com/v1/payments/',data={'id':'066f8423-474f-45d9-9e28-888adaf6b9c5'})

json_dict = json.loads(x.content)
print(json_dict)
c=json_dict['payments'][0]['description']
print(c)
