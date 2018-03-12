# -*- coding: utf-8 -*-

"""Console script for mac_data."""
import sys
import click
import itertools as it
import logging
import mac_data
from mac_data.support import date_iter
from mac_data.api_keys import get_api_key
from mac_data import output
from mac_data.data_sources import weather_underground as wu
from marshmallow.fields import Date

log = logging.getLogger(__name__)

date_t = Date().deserialize


def _log_level_from_verbosity(v):
    return {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG
    }.get(v, logging.DEBUG)


@click.group()
@click.pass_context
@click.version_option(mac_data.__version__)
@click.option('--key-file', default='api_keys.ini', type=click.File(),
              help="Path to api key ini file")
@click.option('-v', '--verbose', count=True)
def main(ctx, key_file, verbose):
    """Command line tool for data collection from web APIs"""
    ctx.obj = {
        'key_file': key_file
    }
    logging.basicConfig(
        level=_log_level_from_verbosity(verbose),
        format="%(asctime)s %(levelname)s %(name)s -- %(message)s",
        datefmt="%xT%X"
    )
    return 0


@main.command()
@click.pass_context
@click.argument('start-date', type=date_t)
@click.argument('end-date', type=date_t)
@click.argument('zip-codes', nargs=-1)
@click.option('--csv-out', type=click.File('w'),
              help="output csv filename (optional)")
def weather_underground(ctx, start_date, end_date, zip_codes, csv_out):
    """Collect data from the Weather Underground API
    """
    api_key = get_api_key(ctx.obj['key_file'], 'weather_underground')
    if not zip_codes:
        return []
    on_dates, zipcodes = map(list, zip(*it.product(date_iter(start_date, end_date), zip_codes)))
    observations = list(wu.collect_many(api_key, on_dates, zipcodes, wu.WAIT))
    if csv_out is not None:
        log.info("Writing data to {}".format(csv_out.name))
        adapter = output.CSVAdapter(csv_out, wu.WeatherUndergroundObservationSchema)
        adapter.dump(observations)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
