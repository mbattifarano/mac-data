"""Waether Underground response processing

Defines functions to transform the deserialized API response into data models
"""
from toolz import compose, curry
from toolz.curried import get_in, map
from mac_data.data_sources.weather_underground.models import WeatherUndergroundObservation

key_map = [
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
    """Renames the keys of d using (new, old) key pairs in key_map"""
    return {new_key: d[old_key]
            for new_key, old_key in key_map}


process_response = compose(
    list,
    map(WeatherUndergroundObservation.from_dict),
    map(rename_keys(key_map)),
    get_in(['history', 'observations'])
)
