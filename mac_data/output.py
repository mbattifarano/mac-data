import csv
from abc import ABCMeta, abstractmethod
from mac_data.marshmallow_ext import fieldnames


class OutputAdapter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def dump(self, data):
        pass


class CSVAdapter(OutputAdapter):
    """Write model data to csv"""
    def __init__(self, fp, schema):
        self.file = fp
        self.schema = schema

    def dump(self, data):
        """Dump a list of models to a csv

        :param data: list of models
        """
        columns = fieldnames(self.schema)
        rows, _ = self.schema(many=True).dump(data)
        writer = csv.DictWriter(self.file, columns)
        writer.writeheader()
        writer.writerows(rows)
