"""Switch platform for integration_blueprint."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .const import DOMAIN
from .coordinator import EcodanDataUpdateCoordinator
from .entity import EcodanEntity
from .pyecodan.device import Device, DeviceStateKeys


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        EcodanSwitch(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


@dataclass(kw_only=True)
class EcodanSwitchEntityDescription(SwitchEntityDescription):
    """Custom description class for Ecodan Switch Entities."""

    state_key: str
    turn_on_fn: Callable[[], Device]
    turn_off_fn: Callable[[], Device]


ENTITY_DESCRIPTIONS = [
    EcodanSwitchEntityDescription(
        key="ha_ecodan",
        name="Power Switch",
        icon="mdi:power",
        state_key=DeviceStateKeys.Power,
        turn_on_fn=Device.power_on,
        turn_off_fn=Device.power_off,
    ),
    EcodanSwitchEntityDescription(
        key="ha_ecodan",
        name="Force Hot Water",
        icon="mdi:thermometer-water",
        state_key = DeviceStateKeys.ForcedHotWaterMode,
        turn_on_fn = lambda device: device.force_hot_water(True),
        turn_off_fn = lambda device: device.force_hot_water(False),
    )
]


class EcodanSwitch(EcodanEntity, SwitchEntity):
    """A Switch Entity for Ecodan Heatpumps."""

    def __init__(
        self,
        coordinator: EcodanDataUpdateCoordinator,
        entity_description: EcodanSwitchEntityDescription,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self.coordinator.data.get(self.entity_description.state_key)

    async def async_turn_on(self, **_: any) -> None:
        """Turn on the switch."""
        await self.entity_description.turn_on_fn(self.coordinator.device)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: any) -> None:
        """Turn off the switch."""
        await self.entity_description.turn_off_fn(self.coordinator.device)
        await self.coordinator.async_request_refresh()
