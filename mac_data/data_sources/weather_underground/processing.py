"""Weather Underground response processing

Defines functions to transform the deserialized API response into data models
"""
import logging
from toolz import compose, curry, merge
from toolz.curried import get_in, map
from .models import WeatherUndergroundObservation
from .api import api_query_args
from mac_data.support import collect

log = logging.getLogger(__name__)

prefix_query_param = '_query:{}'.format

key_map = [
    ('zipcode', prefix_query_param('zipcode')),
    ('recorded_at', 'date'),
    ('temperature', 'tempi'),
    ('dew_point', 'dewpti'),
    ('humidity', 'hum'),
    ('wind_speed', 'wspdi'),
    ('wind_gust', 'wgusti'),
    ('visibility', 'visi'),
    ('pressure', 'pressurei'),
    ('windchill', 'windchilli'),
    ('heat_index', 'heatindexi'),
    ('precipitation', 'precipi'),
    ('fog', 'fog'),
    ('rain', 'rain'),
    ('snow', 'snow'),
    ('condition', 'icon'),
]


@curry
def rename_keys(key_map, d):
    """Renames the keys of d using (new, old) key pairs in key_map

    :rtype: dict
    :param key_map: dict of (new key, old key) pairs
    :param d: dict
    :return: renamed dictionary
    """
    return {new_key: d[old_key]
            for new_key, old_key in key_map}


@curry
def named_query_params(arg_names, arg_values):
    """Return prefixed argument name value pairs

    :rtype: list
    :param arg_names: list of argument names
    :param arg_values: list of argument values
    :return: name value pairs
    """
    prefixed_names = map(prefix_query_param, arg_names)
    return zip(prefixed_names, arg_values)


@curry
def merge_metadata(metadata, observation):
    """Merge metadata and observation dictionaries

    :rtype: dict
    :param metadata: dict of query metadata
    :param observation: dict of observation data
    :return: data dictionary
    """
    return merge(metadata, observation)


extract_observations = get_in(['history', 'observations'])

create_model = compose(
    WeatherUndergroundObservation.from_dict,    # create model
    rename_keys(key_map)                        # filter and rename data
)

process_response = compose(                     # create a collection of models
    list,
    map(create_model)
)

process_metadata = compose(                 # include query metadata
    merge_metadata,                         # merge with observations
    dict,                                   # create dict from items
    named_query_params(api_query_args),     # query arg name, value pairs
    collect                                 # api query args as a tuple
)
