import pytest
import requests_mock
from cStringIO import StringIO

import datetime
import pytz
import simplejson as json
from marshmallow import Schema, fields
from toolz import get_in, remove, compose
from mac_data.support import dict_flatten
from mac_data.data_sources import weather_underground as w
from mac_data.data_sources.weather_underground.schema import NULL_VALUES
from mac_data.data_sources.weather_underground.processing import rename_keys
from mac_data.data_sources.weather_underground.output import CSVAdapter


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
    def read_float(v):
        if v == "":
            return None
        else:
            value = float(v)
            if value < 0:
                return None
            else:
                return value
    with requests_mock.Mocker() as m:
        m.get("http://api.wunderground.com/api/the_api_key/history_20170309/q/15217.json",
              text=response)
        observations = w.collect_data("the_api_key", datetime.date(2017, 3, 9), "15217")
        raw_data = json.loads(response)
        raw_observations = raw_data['history']['observations']
        assert len(observations) == len(raw_observations)
        for ob, raw_ob in zip(observations, raw_observations):
            assert ob.zipcode == "15217"
            # The api call is mocked to return a canned response from 2016-09-01
            assert ob.recorded_at.date() == datetime.date(2016, 9, 1)
            assert ob.temperature == read_float(raw_ob['tempi'])
            assert ob.dew_point == read_float(raw_ob['dewpti'])
            assert ob.humidity == read_float(raw_ob['hum'])
            assert ob.wind_speed == read_float(raw_ob['wspdi'])
            assert ob.wind_gust == read_float(raw_ob['wgusti'])
            assert ob.visibility == read_float(raw_ob['visi'])
            assert ob.pressure == read_float(raw_ob['pressurei'])
            assert ob.windchill == read_float(raw_ob['windchilli'])
            assert ob.heat_index == read_float(raw_ob['heatindexi'])
            assert ob.precipitation == read_float(raw_ob['precipi'])
            assert ob.fog == read_float(raw_ob['fog'])
            assert ob.rain == read_float(raw_ob['rain'])
            assert ob.snow == read_float(raw_ob['snow'])
            assert ob.condition == raw_ob['icon']


def test_rename_keys():
    d = {'a': 1, 'b': "hello", 'c': {'a': 2}}
    key_map = [
        (0, 'a'),
        ('foo', 'b'),
        ('bar', 'c')
    ]
    expected = {0: 1, 'foo': "hello", 'bar': {'a': 2}}
    assert rename_keys(key_map, d) == expected


def test_process_metadata():
    values = ['the_key', 'the_date', 'the_zipcode']
    f = w.process_metadata(*values)
    expected = {
        '_query:api_key': 'the_key',
        '_query:on_date': 'the_date',
        '_query:zipcode': 'the_zipcode'
    }
    assert f({}) == expected


def test_collect_many(response):
    def read_float(v):
        if v == "":
            return None
        else:
            value = float(v)
            if value < 0:
                return None
            else:
                return value
    on_dates = [datetime.date(2017, 3, 9), datetime.date(2017, 3, 10)]
    zipcodes = ["15217", "15216"]
    t = 0  # don't sleep during tests
    with requests_mock.Mocker() as m:
        m.get("http://api.wunderground.com/api/the_api_key/history_20170309/q/15217.json",
              text=response)
        m.get("http://api.wunderground.com/api/the_api_key/history_20170310/q/15216.json",
              text=response)
        raw_data = json.loads(response)
        raw_observations = raw_data['history']['observations']
        obs_iter = w.collect_many("the_api_key", on_dates, zipcodes, t)
        for observations, zipcode in zip(obs_iter, zipcodes):
            assert len(observations) == len(raw_observations)
            for ob, raw_ob in zip(observations, raw_observations):
                assert ob.zipcode == zipcode
                # The api call is mocked to return a canned response from 2016-09-01
                assert ob.recorded_at.date() == datetime.date(2016, 9, 1)
                assert ob.temperature == read_float(raw_ob['tempi'])
                assert ob.dew_point == read_float(raw_ob['dewpti'])
                assert ob.humidity == read_float(raw_ob['hum'])
                assert ob.wind_speed == read_float(raw_ob['wspdi'])
                assert ob.wind_gust == read_float(raw_ob['wgusti'])
                assert ob.visibility == read_float(raw_ob['visi'])
                assert ob.pressure == read_float(raw_ob['pressurei'])
                assert ob.windchill == read_float(raw_ob['windchilli'])
                assert ob.heat_index == read_float(raw_ob['heatindexi'])
                assert ob.precipitation == read_float(raw_ob['precipi'])
                assert ob.fog == read_float(raw_ob['fog'])
                assert ob.rain == read_float(raw_ob['rain'])
                assert ob.snow == read_float(raw_ob['snow'])
                assert ob.condition == raw_ob['icon']


def test_csv_adapter(file_object):
    class TestSchema(Schema):
        key = fields.Integer()
        value = fields.String()
    data = [
        dict(key=1, value='derp'),
        dict(key=0, value='foo')
    ]
    expected = (
        "key,value\r\n"
        "1,derp\r\n"
        "0,foo\r\n"
    )
    adapter = CSVAdapter(file_object, TestSchema)
    adapter.dump(data)
    file_object.seek(0)
    assert file_object.read() == expected
