import time
import datetime
from mac_data import support


def test_dict_flatten():
    d = {
        'a': {'b': 1},
        'c': [2, 3],
        'd': [{'e': 2}, {'e': "hello"}, {'f': 4}],
        'e': 3
    }
    expected = {
        ('a', 'b'): 1,
        ('c', 0): 2,
        ('c', 1): 3,
        ('d', 0, 'e'): 2,
        ('d', 1, 'e'): "hello",
        ('d', 2, 'f'): 4,
        ('e',): 3
    }
    assert support.dict_flatten(d) == expected


def test_collect():
    assert support.collect(1, 2, 3) == (1, 2, 3)


def test_fapply():
    def add3(a, b, c):
        return a + b + c
    assert support.fapply(add3)([1, 2, 3]) == 6


def test_map_sleep():
    def inc(a): return a + 1
    f = support.map_sleep(0.1, inc)
    t0 = time.time()
    assert list(f(range(4))) == [1, 2, 3, 4]
    t1 = time.time()
    assert t1-t0 >= 0.3


def test_date_iter():
    start = datetime.date(2017, 3, 2)
    stop = datetime.date(2017, 3, 10)
    step = datetime.timedelta(days=2)
    expected = [
        datetime.date(2017, 3, 2),
        datetime.date(2017, 3, 4),
        datetime.date(2017, 3, 6),
        datetime.date(2017, 3, 8),
    ]
    assert list(support.date_range(start, stop, step)) == expected
