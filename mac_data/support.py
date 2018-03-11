from toolz import curry


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
