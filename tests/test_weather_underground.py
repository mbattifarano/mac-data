import pytest

import simplejson as json
from toolz import get_in
from mac_data.support import dict_flatten
from mac_data.data_sources import weather_underground as w
from mac_data.data_sources.weather_underground.schema import NULL_VALUES


@pytest.fixture
def response():
    with open('tests/fixtures/response_weather_underground_001.json') as fp:
        return fp.read()


def test_schema_keys(response):
    schema = w.WeatherUndergroundAPIResponse()
    raw_data = json.loads(response)
    data, _ = schema.loads(response)
    assert set(dict_flatten(data).keys()) == set(dict_flatten(raw_data).keys())


def test_schema_values(response):
    schema = w.WeatherUndergroundAPIResponse()
    data, errors = schema.loads(response)
    raw_data = json.loads(response)
    for k, v in dict_flatten(raw_data).iteritems():
        if v in NULL_VALUES:
            assert get_in(k, data) is None
        else:
            try:
                value = float(v)
            except ValueError:  # not a number, compare raw value
                assert get_in(k, data) == v
            else:
                if k in {('response', 'version')}:  # a few exceptions
                    assert get_in(k, data) == v
                else:
                    assert get_in(k, data) == value
