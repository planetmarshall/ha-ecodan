import pytest

from unittest.mock import Mock, AsyncMock

from data.melcloud import MelCloudData


@pytest.fixture
def coordinator():
    def _coordinator(_data: dict=None):
        if _data is None:
            _data = {}

        mock = Mock()
        mock.data = _data
        mock.async_request_refresh = AsyncMock()
        return mock

    return _coordinator


@pytest.fixture
def melcloud():
    return MelCloudData()
