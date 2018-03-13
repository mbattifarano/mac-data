"""Weather Underground API functions

Defines functions for calling the API and parsing its response.
"""
import logging
from inspect import getargspec
import requests
from toolz import compose
from toolz.curried import do

from mac_data.exceptions import APIRequestFailed
from mac_data.support import attribute

log = logging.getLogger(__name__)

# number of seconds to wait between API calls
# free API limit is 10 per minute / 500 per day
WAIT = 7


def request_url(api_key, on_date, zipcode):
    """Form the base request url for weather underground

    :param api_key: str weather underground API key
    :param on_date: datetime.date date to query
    :param zipcode: str zip code to query
    :return: str query url
    """
    template = "http://api.wunderground.com/api/{key}/history_{date}/q/{zipcode}.json"
    return template.format(key=api_key, date=on_date.strftime("%Y%m%d"), zipcode=zipcode)


api_query_args = getargspec(request_url).args


def get_json_or_raise(response):
    """Recover the json payload or raise an exception

    :rtype: dict
    :param response: request.Response
    :return: json payload
    """
    if response.status_code != 200:
        raise APIRequestFailed(response.status_code)
    data = response.json()
    error = data.get('response', {}).get('error')
    if error:
        raise APIRequestFailed(error)
    else:
        return data


query_api = compose(
    get_json_or_raise,
    do(compose(log.info,
               "Received response with status {}".format,
               attribute('status_code'))),
    requests.get,
    do(compose(log.info, "Sending request to {}".format)),
    request_url
)
