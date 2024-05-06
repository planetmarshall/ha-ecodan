from unittest.mock import AsyncMock

import pytest
from homeassistant.components.sensor import SensorDeviceClass

from custom_components.ha_ecodan.sensor import EcodanSensor, ENTITY_DESCRIPTIONS as SENSOR_ENTITY_DESCRIPTIONS
from custom_components.ha_ecodan.switch import EcodanSwitch, ENTITY_DESCRIPTIONS as SWITCH_ENTITY_DESCRIPTIONS


def test_hot_water_sensor_properties(coordinator):

    sensor = EcodanSensor(coordinator(), SENSOR_ENTITY_DESCRIPTIONS[2])

    assert sensor.device_class == SensorDeviceClass.TEMPERATURE
    assert sensor.name == "Hot Water Temperature"


def test_hot_water_sensor_value_from_coordinator(coordinator):
    data = {"TankWaterTemperature": 47}

    sensor = EcodanSensor(coordinator(data), SENSOR_ENTITY_DESCRIPTIONS[2])

    assert sensor.native_value == 47


@pytest.mark.asyncio
async def test_force_hot_water_switch_on(coordinator):
    data = {"ForcedHotWaterMode": False}
    obj = coordinator(data)
    obj.device.force_hot_water = AsyncMock()

    switch = EcodanSwitch(obj, SWITCH_ENTITY_DESCRIPTIONS[1])
    await switch.async_turn_on()

    obj.device.force_hot_water.assert_awaited_with(True)

@pytest.mark.asyncio
async def test_force_hot_water_switch_off(coordinator):
    data = {"ForcedHotWaterMode": True}
    obj = coordinator(data)
    obj.device.force_hot_water = AsyncMock()

    switch = EcodanSwitch(obj, SWITCH_ENTITY_DESCRIPTIONS[1])
    await switch.async_turn_off()

    obj.device.force_hot_water.assert_awaited_with(False)
