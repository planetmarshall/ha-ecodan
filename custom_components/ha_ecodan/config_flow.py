"""Adds config flow for Blueprint."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.selector import selector, TextSelector, TextSelectorConfig, TextSelectorType
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .pyecodan import Client
from .pyecodan.errors import DeviceCommunicationError, DeviceAuthenticationError

from .const import DOMAIN, LOGGER


class EcodanFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    async def async_step_user(
            self,
            user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                client = Client(
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                    session=async_create_clientsession(self.hass),
                )
                self._account = user_input
                self._devices = await client.list_devices()
            except DeviceAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except DeviceCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            else:
                return await self.async_step_select_device(user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME,
                        default=(user_input or {}).get(CONF_USERNAME),
                    ): TextSelector(
                        TextSelectorConfig(
                            type=TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(CONF_PASSWORD): TextSelector(
                        TextSelectorConfig(
                            type=TextSelectorType.PASSWORD
                        ),
                    ),
                }
            ),
            errors=_errors,
        )

    async def async_step_select_device(
            self,
            user_input: dict
    ) -> config_entries.FlowResult:
        """List the available devices to the user"""

        _errors = {}
        device_name = user_input.get("device")
        if device_name is not None:
            device_id = self._devices[device_name]["id"]
            await self.async_set_unique_id(device_id)
            self._abort_if_unique_id_configured()
            data = dict(self._account)
            data.update({
                "device_id": device_id,
                "device_name": device_name
            })
            return self.async_create_entry(
                title=data[CONF_USERNAME], data=data
            )
        else:
            return self.async_show_form(
                step_id="select_device",
                data_schema=vol.Schema(
                    {
                        "device": selector({
                            "select": {
                                "options": list(self._devices.keys())
                            }
                        })
                    }
                ),
                errors=_errors,
            )
