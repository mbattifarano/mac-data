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


def test_callattr():
    l = []
    support.callattr('append', (1,), l)
    assert l == [1]
    support.callattr('extend', ([2, 3],), l)
    assert l == [1, 2, 3]
    assert support.callattr('pop', None, l) == 3
