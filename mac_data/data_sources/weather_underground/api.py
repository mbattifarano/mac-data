"""Weather Underground API functions

Defines functions for calling the API and parsing its response.
"""
import requests
from toolz import compose

from mac_data.exceptions import APIRequestFailed


def request_url(api_key, date, zipcode):
    """Form the base request url for weather underground"""
    template = "http://api.wunderground.com/api/{key}/history_{date}/q/{zipcode}.json"
    return template.format(key=api_key, date=date.strftime("%Y%m%d"), zipcode=zipcode)


def get_json_or_raise(response):
    """Raise an exception when the request failed"""
    if response.status_code != 200:
        raise APIRequestFailed(response.status_code)
    data = response.json()
    error = data.get('response', {}).get('error')
    if error:
        raise APIRequestFailed(error)
    else:
        return data


api_call = compose(
    get_json_or_raise,
    requests.get,
    request_url
)
