import datetime
import pytz
from marshmallow import Schema, fields, post_load

from mac_data.marshmallow_ext import Union, Either, NullObject

NULL_VALUES = ("", "-999", "-9999", "-9999.0", "-9999.00")

Null = Union(map(NullObject, NULL_VALUES))
Integer = Either(Null, fields.Integer())
Float = Either(Null, fields.Float())
String = Either(Null, fields.String())


class Date(Schema):
    hour = Integer
    mday = Integer
    min = Integer
    mon = Integer
    pretty = String
    tzname = String
    year = Integer

    @post_load
    def to_datetime(self, data):
        """After loading the dict, convert to tz-aware datetime"""
        tz = pytz.timezone(data['tzname'])
        dt = datetime.datetime(data['year'], data['mon'], data['mday'],
                               data['hour'], data['min'], 0)
        return tz.localize(dt)


class DailySummary(Schema):
    coolingdegreedays = Integer
    coolingdegreedaysnormal = Float
    date = fields.Nested(Date)
    fog = Float
    gdegreedays = Integer
    hail = Float
    heatingdegreedays = Integer
    heatingdegreedaysnormal = Float
    humidity = Float

    maxdewpti = Float
    maxdewptm = Float
    maxhumidity = Float
    maxpressurei = Float
    maxpressurem = Float
    maxtempi = Float
    maxtempm = Float
    maxvisi = Float
    maxvism = Float
    maxwspdi = Float
    maxwspdm = Float

    meandewpti = Float
    meandewptm = Float
    meanpressurei = Float
    meanpressurem = Float
    meantempi = Float
    meantempm = Float
    meanvisi = Float
    meanvism = Float
    meanwdird = Float
    meanwdire = Float
    meanwindspdi = Float
    meanwindspdm = Float

    mindewpti = Float
    mindewptm = Float
    minhumidity = Float
    minpressurei = Float
    minpressurem = Float
    mintempi = Float
    mintempm = Float
    minvisi = Float
    minvism = Float
    minwspdi = Float
    minwspdm = Float

    monthtodatecoolingdegreedays = Integer
    monthtodatecoolingdegreedaysnormal = Integer
    monthtodateheatingdegreedays = Integer
    monthtodateheatingdegreedaysnormal = Integer
    monthtodatesnowfalli = Integer
    monthtodatesnowfallm = Integer

    precipi = Float
    precipm = Float
    precipsource = String
    rain = Float

    since1jancoolingdegreedays = Integer
    since1jancoolingdegreedaysnormal = Integer
    since1julheatingdegreedays = Integer
    since1julheatingdegreedaysnormal = Integer
    since1julsnowfalli = Integer
    since1julsnowfallm = Integer
    since1sepcoolingdegreedays = Integer
    since1sepcoolingdegreedaysnormal = Integer
    since1sepheatingdegreedays = Integer
    since1sepheatingdegreedaysnormal = Integer

    snow = Float
    snowdepthi = Float
    snowdepthm = Float
    snowfalli = Float
    snowfallm = Float
    thunder = Float
    tornado = Float


class Observation(Schema):
    conds = String
    date = fields.Nested(Date)
    dewpti = Float
    dewptm = Float
    fog = Float
    hail = Float
    heatindexi = Float
    heatindexm = Float
    hum = Float
    icon = String
    metar = String
    precipi = Float
    precipm = Float
    pressurei = Float
    pressurem = Float
    rain = Float
    snow = Float
    tempi = Float
    tempm = Float
    thunder = Float
    tornado = Float
    utcdate = fields.Nested(Date)
    visi = Float
    vism = Float
    wdird = Float
    wdire = String
    wgusti = Float
    wgustm = Float
    windchilli = Float
    windchillm = Float
    wspdi = Float
    wspdm = Float


class History(Schema):
    dailysummary = fields.Nested(DailySummary, many=True)
    date = fields.Nested(Date)
    observations = fields.Nested(Observation, many=True)
    utcdate = fields.Nested(Date)


class Response(Schema):
    termsofService = String
    version = String
    features = fields.Dict()


class WeatherUndergroundAPIResponse(Schema):
    history = fields.Nested(History, required=True)
    response = fields.Nested(Response)
