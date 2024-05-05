from homeassistant.components.select import SelectEntityDescription, SelectEntity

from custom_components.ha_ecodan import EcodanDataUpdateCoordinator, DOMAIN
from .pyecodan.device import DeviceStateKeys, OperationMode
from .entity import EcodanEntity


ENTITY_DESCRIPTIONS = (SelectEntityDescription(key="ha_ecodan", name="Operation Mode", icon="mdi:cog"),)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        EcodanSelect(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class EcodanSelect(EcodanEntity, SelectEntity):
    """A Select Entity for the Ecodan platform."""

    _options = {
        "Room Thermostat": OperationMode.Room,
        "Flow Temperature": OperationMode.Flow,
        "Weather Compensation": OperationMode.Curve,
    }

    def __init__(self, coordinator: EcodanDataUpdateCoordinator, entity_description: SelectEntityDescription):
        """Create an Selection Entity."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def options(self) -> list[str]:
        """Get the available operation mode options."""
        return list(self._options.keys())

    @property
    def current_option(self) -> str | None:
        """Get the currently selected operation mode."""
        operation_mode = self.coordinator.data.get(DeviceStateKeys.OperationModeZone1)
        selected_option = [key for key, value in self._options.items() if value == operation_mode]
        return selected_option[0] if len(selected_option) > 0 else None

    async def async_select_option(self, option: str) -> None:
        """Set the selected option."""
        option_to_select = self._options.get(option)
        if option_to_select is not None:
            await self.coordinator.device.set_operation_mode(option_to_select)
