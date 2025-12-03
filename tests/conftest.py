import uuid
import pytest


@pytest.fixture
def random_uuid():
    return lambda: uuid.uuid4().hex

