"""Weather Underground Data Collection API
"""
from toolz import compose, juxt, map
from toolz.curried import get

from mac_data.support import fapply
from .schema import WeatherUndergroundAPIResponse
from .processing import process_response, extract_observations, process_metadata
from .api import query_api

get_observations = compose(                   # query the api and extract observations
    extract_observations,                     # get the list of observations from payload
    get(0),                                   # drop the deserialization errors
    WeatherUndergroundAPIResponse().load,     # deserialize api response
    query_api                                 # query the api
)

get_data = compose(                           # create observation models from api response
    process_response,                         # create observations models
    fapply(map),                              # merge metadata into each observation
    juxt(process_metadata, get_observations)  # process query params as metadata and api call
)
