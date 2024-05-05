from unittest.mock import AsyncMock

import pytest

from custom_components.ha_ecodan.select import EcodanSelect, ENTITY_DESCRIPTIONS
from custom_components.ha_ecodan.pyecodan.device import DeviceStateKeys, OperationMode


def test_select_modes(coordinator):
    sensor = EcodanSelect(coordinator(), ENTITY_DESCRIPTIONS[0])
    assert sensor.options == [
        "Room Thermostat",
        "Flow Temperature",
        "Weather Compensation"
    ]


@pytest.mark.parametrize("operation_mode, option", [
    (OperationMode.Room, "Room Thermostat"),
    (OperationMode.Flow, "Flow Temperature"),
    (OperationMode.Curve, "Weather Compensation")
])
def test_current_selection(coordinator, operation_mode, option):
    data = { DeviceStateKeys.OperationModeZone1: operation_mode}
    sensor = EcodanSelect(coordinator(data), ENTITY_DESCRIPTIONS[0])
    assert sensor.current_option == option


@pytest.mark.parametrize("operation_mode, option", [
    (OperationMode.Room, "Room Thermostat"),
    (OperationMode.Flow, "Flow Temperature"),
    (OperationMode.Curve, "Weather Compensation")
])
@pytest.mark.asyncio
async def test_select_option(coordinator, operation_mode, option):
    data = { DeviceStateKeys.OperationModeZone1: operation_mode}
    obj = coordinator(data)
    obj.device.set_operation_mode = AsyncMock()
    sensor = EcodanSelect(obj, ENTITY_DESCRIPTIONS[0])
    await sensor.async_select_option(option)

    obj.device.set_operation_mode.assert_awaited_with(operation_mode)
