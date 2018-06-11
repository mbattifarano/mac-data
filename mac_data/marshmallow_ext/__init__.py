from fields import Union, Either, NullObject  # NOQA


def fieldnames(schema):
    return schema._declared_fields.keys()
