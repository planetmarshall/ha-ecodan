"""Switch platform for integration_blueprint."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .const import DOMAIN
from .coordinator import EcodanDataUpdateCoordinator
from .entity import EcodanEntity
from .pyecodan.device import DeviceStateKeys

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="ha_ecodan",
        name="Power Switch",
        icon="mdi:power"
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        EcodanPowerSwitch(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class EcodanPowerSwitch(EcodanEntity, SwitchEntity):
    def __init__(
        self,
        coordinator: EcodanDataUpdateCoordinator,
        entity_description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self.coordinator.data.get(DeviceStateKeys.Power)

    async def async_turn_on(self, **_: any) -> None:
        """Turn on the switch."""
        await self.coordinator.device.power_on()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: any) -> None:
        """Turn off the switch."""
        await self.coordinator.device.power_off()
        await self.coordinator.async_request_refresh()
