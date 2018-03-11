from toolz import compose
from toolz.curried import get_in, map
from mac_data.data_sources.weather_underground.models import WeatherUndergroundObservation


def process_observation(observation):
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
    return {new_key: observation[old_key]
            for new_key, old_key in key_map}


process_response = compose(
    list,
    map(WeatherUndergroundObservation.from_dict),
    map(process_observation),
    get_in(['history', 'observations'])
)
