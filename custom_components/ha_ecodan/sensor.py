from dataclasses import dataclass

from homeassistant.const import UnitOfTemperature
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorDeviceClass, SensorStateClass

from custom_components.ha_ecodan import EcodanDataUpdateCoordinator, DOMAIN
from .pyecodan.device import DeviceStateKeys
from .entity import EcodanEntity


@dataclass(kw_only=True)
class EcodanSensorEntityDescription(SensorEntityDescription):
    """A Sensor Description for Ecodan Sensors."""

    state_key: str


ENTITY_DESCRIPTIONS = (
    EcodanSensorEntityDescription(
        key="ha_ecodan",
        name="Flow Temperature",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        state_key=DeviceStateKeys.FlowTemperature,
    ),
    EcodanSensorEntityDescription(
        key="ha_ecodan",
        name="Outdoor Temperature",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        state_key=DeviceStateKeys.OutdoorTemperature,
    ),
    EcodanSensorEntityDescription(
        key="ha_ecodan",
        name="Hot Water Temperature",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        state_key=DeviceStateKeys.HotWaterTemperature,
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        EcodanSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class EcodanSensor(EcodanEntity, SensorEntity):
    """A Sensor Entity for the Ecodan platform."""

    def __init__(self, coordinator: EcodanDataUpdateCoordinator, entity_description: EcodanSensorEntityDescription):
        """Create an Ecodan sensor."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.device.id}_{entity_description.state_key}".lower()

    @property
    def native_value(self) -> str:
        """Return the value of the sensor."""
        return self.coordinator.data.get(self.entity_description.state_key)
