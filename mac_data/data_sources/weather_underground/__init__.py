"""Weather Underground Data Collection API
"""
import logging
import itertools as it

from toolz import compose, juxt, map, curry
from toolz.curried import get, do

from mac_data.support import fapply, map_sleep, flatten, date_range
from mac_data.output import CSVAdapter
from .api import WAIT, query_api
from .schema import WeatherUndergroundAPIResponse
from .processing import process_response, extract_observations, process_metadata
from .models import WeatherUndergroundObservation, WeatherUndergroundObservationSchema

log = logging.getLogger(__name__)

get_observations = compose(                   # query the api and extract observations
    extract_observations,                     # get the list of observations from payload
    get(0),                                   # drop the deserialization errors
    WeatherUndergroundAPIResponse().load,     # deserialize api response
    query_api                                 # query the api
)

collect_data = compose(                       # create observation models from api response
    do(compose(log.info,
               "Created {} observations".format,
               len)),
    process_response,                         # create observations models
    fapply(map),                              # merge metadata into each observation
    juxt(process_metadata, get_observations)  # process query params as metadata and api call
)


def collect_many(api_key, on_dates, zipcodes, t):
    """Collect data over many dates and zipcodes

    :param api_key: str weather underground api key
    :param on_dates: list of dates
    :param zipcodes: list of zipcodes
    :param t: float delay between api calls
    :return: list of observations
    """
    collect_one = curry(collect_data)
    process = compose(
        flatten,
        map_sleep(t, fapply(collect_one(api_key))),
        zip
    )
    return process(on_dates, zipcodes)
