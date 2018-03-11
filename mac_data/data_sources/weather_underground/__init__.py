"""Weather Underground Data Collection API
"""
from toolz import compose, juxt, map, curry
from toolz.curried import get

from mac_data.support import fapply, map_sleep
from .schema import WeatherUndergroundAPIResponse
from .processing import process_response, extract_observations, process_metadata
from .api import WAIT, query_api

get_observations = compose(                   # query the api and extract observations
    extract_observations,                     # get the list of observations from payload
    get(0),                                   # drop the deserialization errors
    WeatherUndergroundAPIResponse().load,     # deserialize api response
    query_api                                 # query the api
)

collect_data = compose(                       # create observation models from api response
    process_response,                         # create observations models
    fapply(map),                              # merge metadata into each observation
    juxt(process_metadata, get_observations)  # process query params as metadata and api call
)


def collect_many(api_key, on_dates, zipcodes, t=WAIT):
    """Collect data over many dates and zipcodes"""
    collect_one = curry(collect_data)
    process = compose(
        map_sleep(t, fapply(collect_one(api_key))),
        zip
    )
    return process(on_dates, zipcodes)
