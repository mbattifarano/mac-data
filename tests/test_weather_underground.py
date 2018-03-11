import pytest
import requests_mock

import datetime
import pytz
import simplejson as json
from toolz import get_in, remove, compose
from mac_data.support import dict_flatten
from mac_data.data_sources import weather_underground as w
from mac_data.data_sources.weather_underground.schema import NULL_VALUES


@pytest.fixture
def response():
    with open('tests/fixtures/response_weather_underground_001.json') as fp:
        return fp.read()


def _date_key(key):
    return 'date' in key or 'utcdate' in key


def test_schema_keys(response):
    schema = w.WeatherUndergroundAPIResponse()
    raw_data = json.loads(response)
    data, _ = schema.loads(response)
    assert (set(remove(_date_key, dict_flatten(data).keys())) ==
            set(remove(_date_key, dict_flatten(raw_data).keys())))


def test_schema_values(response):
    schema = w.WeatherUndergroundAPIResponse()
    data, errors = schema.loads(response)
    assert not errors
    raw_data = json.loads(response)
    for k, v in dict_flatten(data).iteritems():
        raw_value = get_in(k, raw_data)
        if _date_key(k):
            tz = pytz.timezone(raw_value['tzname'])
            dt_components = compose(int, raw_value.__getitem__)
            dt = datetime.datetime(*map(dt_components,
                                        ['year', 'mon', 'mday', 'hour', 'min']))
            assert v == tz.localize(dt)
        elif v is None:
            assert raw_value in NULL_VALUES
        else:
            try:
                raw_float = float(raw_value)
            except ValueError:  # not a number, compare raw value
                assert v == raw_value
            else:
                if k in {('response', 'version')}:  # an exception
                    assert v == raw_value
                else:
                    assert v == raw_float


def test_processing_pipeline(response):
    with requests_mock.Mocker() as m:
        m.get("http://api.wunderground.com/api/the_api_key/history_20170309/q/15217.json",
              text=response)
        observations = w.get_data("the_api_key", datetime.date(2017, 3, 9), "15217")
        raw_data = json.loads(response)
        assert len(observations) == len(raw_data['history']['observations'])
