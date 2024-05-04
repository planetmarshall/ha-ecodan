import pytest

from unittest.mock import Mock


@pytest.fixture
def coordinator():
    def _coordinator(_data: dict=None):
        if _data is None:
            _data = {}

        mock = Mock()
        mock.data = _data
        return mock

    return _coordinator
