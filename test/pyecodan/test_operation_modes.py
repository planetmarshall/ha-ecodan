import pytest

from custom_components.ha_ecodan.pyecodan import Device
from custom_components.ha_ecodan.pyecodan.device import OperationMode

from unittest.mock import AsyncMock, Mock


@pytest.mark.parametrize("operation_mode_index, operation_mode", [
    (0, OperationMode.Room),
    (1, OperationMode.Flow),
    (2, OperationMode.Curve),
])
def test_operation_mode_from_device_state(melcloud, operation_mode_index, operation_mode):
    client = Mock()
    device = Device(client, melcloud.device_state_with(OperationModeZone1=operation_mode_index))

    assert device.operation_mode == operation_mode


@pytest.mark.parametrize("operation_mode_index, operation_mode", [
    (0, OperationMode.Room),
    (1, OperationMode.Flow),
    (2, OperationMode.Curve),
])
@pytest.mark.asyncio
async def test_set_operation_mode(melcloud, operation_mode_index, operation_mode):
    client = Mock()
    client.device_request = AsyncMock(return_value=melcloud.response)
    device = Device(client, melcloud.device_state)

    await device.set_operation_mode(operation_mode)

    client.device_request.assert_called_with(
        "SetAtw",
        melcloud.request_with(EffectiveFlags=281475043819560, OperationModeZone1=operation_mode_index))
