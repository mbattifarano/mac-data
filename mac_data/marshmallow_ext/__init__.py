from fields import Union, Either, NullObject


def fieldnames(schema):
    return schema._declared_fields.keys()
