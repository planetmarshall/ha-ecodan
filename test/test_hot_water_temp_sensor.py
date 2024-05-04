from homeassistant.components.sensor import SensorDeviceClass

from custom_components.ha_ecodan.sensor import EcodanSensor, ENTITY_DESCRIPTIONS


def test_hot_water_sensor_properties(coordinator):

    sensor = EcodanSensor(coordinator(), ENTITY_DESCRIPTIONS[2])

    assert sensor.device_class == SensorDeviceClass.TEMPERATURE
    assert sensor.name == "Hot Water Temperature"


def test_hot_water_sensor_value_from_coordinator(coordinator):
    data = {"TankWaterTemperature": 47}

    sensor = EcodanSensor(coordinator(data), ENTITY_DESCRIPTIONS[2])

    assert sensor.native_value == 47
