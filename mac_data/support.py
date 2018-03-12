import logging
import time
import datetime
from toolz import curry

log = logging.getLogger(__name__)


def dict_flatten(d, prefix=None):
    """Flatten a dictionary"""
    items = []
    prefix = prefix or tuple()
    for k, v in _iteritems(d):
        key = prefix + (k,)
        try:
            items.extend(dict_flatten(v, key).items())
        except TypeError:
            items.append((key, v))
    return dict(items)


def collect(*args):
    """Collect arguments as a tuple"""
    return args


@curry
def fapply(f, args):
    """Apply a function to an iterable of arguments"""
    return f(*args)


@curry
def attribute(name, obj):
    return getattr(obj, name)


@curry
def map_sleep(t, f, arglist):
    """Map a function over a list of arguments with a sleep timer"""
    arg_list = iter(arglist)
    yield f(arg_list.next())
    for arg in arg_list:
        log.debug("Sleeping for {} seconds".format(t))
        time.sleep(t)
        yield f(arg)


ONE_DAY = datetime.timedelta(days=1)


def date_iter(start, stop, step=ONE_DAY):
    dt = start
    while dt < stop:
        yield dt
        dt += step


def flatten(l):
    for it in l:
        for el in it:
            yield el


def _iteritems(d_l):
    if isinstance(d_l, str) or isinstance(d_l, unicode):
        raise TypeError
    try:
        return d_l.iteritems()
    except AttributeError:
        pass
    try:
        return enumerate(d_l)
    except TypeError:
        raise TypeError
