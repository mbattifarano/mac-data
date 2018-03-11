from toolz import compose
from toolz.curried import get

from .schema import WeatherUndergroundAPIResponse
from .processing import process_response
from .api import api_call

get_data = compose(
    process_response,
    get(0),
    WeatherUndergroundAPIResponse().load,
    api_call
)
