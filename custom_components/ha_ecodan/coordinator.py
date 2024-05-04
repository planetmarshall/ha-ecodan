from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from .pyecodan import Device
from .pyecodan.errors import DeviceCommunicationError, DeviceAuthenticationError

from .const import DOMAIN, LOGGER


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class EcodanDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        device: Device,
    ) -> None:
        """Initialize."""
        self._device = device
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=2),
        )

    @property
    def device(self) -> Device:
        """Get the ecodan device."""
        return self._device

    async def _async_update_data(self):
        """Update data via library."""
        try:
            return await self._device.get_state()
        except DeviceAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except DeviceCommunicationError as exception:
            raise UpdateFailed(exception) from exception
