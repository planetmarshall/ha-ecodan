from homeassistant.components.sensor import SensorDeviceClass

from custom_components.ha_ecodan.sensor import EcodanSensor, ENTITY_DESCRIPTIONS


def test_flowtemp_sensor_properties(coordinator):

    sensor = EcodanSensor(coordinator(), ENTITY_DESCRIPTIONS[0])

    assert sensor.device_class == SensorDeviceClass.TEMPERATURE
    assert sensor.name == "Flow Temperature"


def test_flowtemp_sensor_value_from_coordinator(coordinator):
    data = {"FlowTemperature": 26}

    sensor = EcodanSensor(coordinator(data), ENTITY_DESCRIPTIONS[0])

    assert sensor.native_value == 26
