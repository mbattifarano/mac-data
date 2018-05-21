from marshmallow.fields import Field
from marshmallow import ValidationError


class Union(Field):
    """Represents a field that is one of the listed types"""
    def __init__(self, fields, **kwargs):
        super(Union, self).__init__(**kwargs)
        self._fields = fields

    def _deserialize(self, value, attr, data):
        for type_ in self._fields[:-1]:
            try:
                return type_.deserialize(value)
            except ValidationError:
                pass
        return self._fields[-1].deserialize(value)

    def _serialize(self, value, attr, obj):
        for type_ in self._fields[:-1]:
            try:
                return type_.serialize(attr, obj)
            except ValidationError:
                pass
        return self._fields[-1].serialize(attr, obj)


class Either(Union):
    """Represents a field that is either one type or another"""
    def __init__(self, instance_a, instance_b, **kwargs):
        super(Either, self).__init__([instance_a, instance_b], **kwargs)


class NullObject(Field):
    """Represents a null object literal"""
    def __init__(self, value, null_object=None, **kwargs):
        super(NullObject, self).__init__(**kwargs)
        self._value = value
        self._null_object = null_object

    def _deserialize(self, value, attr, data):
        if value == self._value:
            return self._null_object
        else:
            raise ValidationError("Not a valid NullObject")

    def _serialize(self, value, attr, obj):
        if value == self._null_object:
            return self._value
        else:
            raise ValidationError("Not a valid NullObject")
