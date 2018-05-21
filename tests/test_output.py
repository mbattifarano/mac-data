from marshmallow import Schema, fields
from mac_data import output


def test_csv_adapter(file_object):
    class TestSchema(Schema):
        class Meta:
            ordered = True
        key = fields.Integer()
        value = fields.String()
    data = [
        dict(key=1, value='derp'),
        dict(key=0, value='foo')
    ]
    expected = (
        "key,value\r\n"
        "1,derp\r\n"
        "0,foo\r\n"
    )
    adapter = output.CSVAdapter(file_object, TestSchema)
    adapter.dump(data)
    file_object.seek(0)
    actual = file_object.read()
    assert actual == expected
