from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION
from .coordinator import EcodanDataUpdateCoordinator


class EcodanEntity(CoordinatorEntity):
    """Base class for Ecodan entities."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: EcodanDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.device.id)},
            name=NAME,
            model=VERSION,
            manufacturer=NAME,
        )
