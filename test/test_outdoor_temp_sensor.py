from homeassistant.components.sensor import SensorDeviceClass

from custom_components.ha_ecodan.sensor import EcodanSensor, ENTITY_DESCRIPTIONS


def test_outdoor_temp_sensor_properties(coordinator):

    sensor = EcodanSensor(coordinator(), ENTITY_DESCRIPTIONS[1])

    assert sensor.device_class == SensorDeviceClass.TEMPERATURE
    assert sensor.name == "Outdoor Temperature"


def test_outdoor_temp_sensor_value_from_coordinator(coordinator):
    data = {"OutdoorTemperature": -9.5}

    sensor = EcodanSensor(coordinator(data), ENTITY_DESCRIPTIONS[1])

    assert sensor.native_value == -9.5
