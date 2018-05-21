import logging
import time
import datetime
from toolz import curry

log = logging.getLogger(__name__)


def dict_flatten(d, prefix=None):
    """Flatten a nested dictionary

    nested values are keyed by a tuple of parent keys

    >>> dict_flatten({'a': {'b': {'c': 1}}})
    {('a', 'b', 'c'): 1}

    :rtype: dict
    :param d: dict
    :param prefix: tuple of keys
    :return: dictionary of flattened keys and values
    """
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
    """Collect arguments as a tuple

    :rtype: tuple
    :param args: tuple of arguments
    :return: args
    """
    return args


@curry
def fapply(f, args):
    """Apply a function to an iterable of arguments

    :param f: function
    :param args: tuple of arguments for f
    :return: value
    """
    return f(*args)


@curry
def attribute(name, obj):
    """Attribute access to an object

    :param name: str attribute name
    :param obj: object
    :return: obj.name
    """
    return getattr(obj, name)


@curry
def map_sleep(t, f, arglist):
    # type: (float, function, list) -> iter
    """Map a function over a list of arguments with a sleep timer

    :param t: float seconds to sleep in between invocations
    :param f: function to apply
    :param arglist: list of arguments for f
    :return: list of values
    """
    arg_list = iter(arglist)
    yield f(arg_list.next())
    for arg in arg_list:
        log.debug("Sleeping for {} seconds".format(t))
        time.sleep(t)
        yield f(arg)


ONE_DAY = datetime.timedelta(days=1)


def date_range(start, stop, step=ONE_DAY):
    # type: (datetime.date, datetime.date, datetime.timedelta) -> list
    """

    :rtype: list
    :param start: date
    :param stop: date
    :param step: timedelta
    :return: list of dates
    """
    dt = start
    while dt < stop:
        yield dt
        dt += step


def flatten(l):
    # type: (iter) -> iter
    """Flatten a list
    :param l: list of lists
    :return: list
    """
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
