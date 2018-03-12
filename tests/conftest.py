import pytest
from cStringIO import StringIO
from tempfile import NamedTemporaryFile


@pytest.fixture
def file_object():
    fp = StringIO()
    yield fp
    fp.close()


@pytest.fixture
def tmpfile():
    with NamedTemporaryFile(delete=False) as fp:
        yield fp
