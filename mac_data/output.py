import csv
from mac_data.marshmallow_ext import fieldnames


class OutputAdapter(object):
    def dump(self, data):
        pass


class CSVAdapter(OutputAdapter):
    def __init__(self, fp, schema):
        self.file = fp
        self.schema = schema

    def dump(self, data):
        columns = fieldnames(self.schema)
        rows, _ = self.schema(many=True).dump(data)
        writer = csv.DictWriter(self.file, columns)
        writer.writeheader()
        writer.writerows(rows)
