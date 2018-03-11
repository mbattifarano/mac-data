from sqlalchemy.ext.declarative import declarative_base


class ConstructorsMixin(object):
    @classmethod
    def from_dict(cls, data):
        return cls(**data)


Base = declarative_base(cls=ConstructorsMixin)
