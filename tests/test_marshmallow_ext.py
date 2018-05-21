import pytest

from mac_data.marshmallow_ext import Either, NullObject
from marshmallow import fields, ValidationError


def test_either_field():
    f = Either(fields.Integer(), fields.List(fields.Integer()))
    assert f.deserialize("1") == 1
    assert f.deserialize(["1", "2", "3"]) == [1, 2, 3]

    assert f.serialize('a', {'a': 1}) == 1
    assert f.serialize('a', {'a': [1, 2, 3]}) == [1, 2, 3]

    with pytest.raises(ValidationError):
        f.deserialize("a string")

    with pytest.raises(ValidationError):
        print f.serialize("a", {'a': "a string"})


def test_null_object_field():
    f = NullObject("")
    assert f.deserialize("") is None
    with pytest.raises(ValidationError):
        f.deserialize("hello")

    assert f.serialize('a', {'a': None}) == ""
    with pytest.raises(ValidationError):
        f.serialize('a', {'a': "hello"})
