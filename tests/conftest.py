import pytest
from cStringIO import StringIO


@pytest.fixture
def file_object():
    fp = StringIO()
    yield fp
    fp.close()
