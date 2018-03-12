from sqlalchemy.ext.declarative import declarative_base


class ConstructorsMixin(object):
    @classmethod
    def from_dict(cls, data):
        """Construct a model from a dictionary of key, value pairs

        :rtype: cls
        :param data: dict of model key, value pairs
        :return: model
        """
        return cls(**data)


Base = declarative_base(cls=ConstructorsMixin)
