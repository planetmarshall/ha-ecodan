from enum import IntFlag
from typing import Dict

from .errors import DeviceCommunicationError


class EffectiveFlags(IntFlag):
    Update = 0
    Power = 1


class InternalDeviceStateKeys:
    FlowTemperature = "FlowTemperature"
    Power = "Power"


class DeviceStateKeys:
    DeviceName = "DeviceName"
    DeviceID = "DeviceID"
    BuildingID = "BuildingID"
    EffectiveFlags = "EffectiveFlags"


class DeviceState:

    def __init__(self, device_state: Dict):
        self._state = {}
        internal_device_state = device_state["Device"]

        self._state[InternalDeviceStateKeys.FlowTemperature] = internal_device_state[InternalDeviceStateKeys.FlowTemperature]
        self._state[InternalDeviceStateKeys.Power] = internal_device_state[InternalDeviceStateKeys.Power]

        self._state[DeviceStateKeys.DeviceID] = device_state[DeviceStateKeys.DeviceID]
        self._state[DeviceStateKeys.DeviceName] = device_state[DeviceStateKeys.DeviceName]
        self._state[DeviceStateKeys.BuildingID] = device_state[DeviceStateKeys.BuildingID]


    def __getitem__(self, item):
        return self._state[item]

    def as_dict(self):
        return self._state

class Device:
    """
    Represents an Ecodan Heat Pump device
    """
    def __init__(self, client, device_state: Dict):
        self._client = client
        self._state = DeviceState(device_state)

    @property
    def id(self):
        return self._state[DeviceStateKeys.DeviceID]

    @property
    def name(self):
        return self._state[DeviceStateKeys.DeviceName]

    @property
    def building_id(self):
        return self._state[DeviceStateKeys.BuildingID]

    async def _request(self, effective_flags: EffectiveFlags, **kwargs) -> Dict:
        state = {
            DeviceStateKeys.BuildingID: self.building_id,
            DeviceStateKeys.DeviceID: self.id,
            DeviceStateKeys.EffectiveFlags: effective_flags
        }
        state.update(kwargs)
        return await self._client.device_request("SetAtw", state)

    async def get_state(self) -> Dict:
        device = await self._client.get_device(self.id)
        self._state = device._state
        return self._state.as_dict()

    @property
    def data(self):
        return self._state.as_dict()

    async def power_on(self) -> None:
        """
        Turn on the Heat Pump. Performs the same task as the `On` switch in the MELCloud interface
        """
        response_state = await self._request(EffectiveFlags.Power, Power=True)
        if not response_state[InternalDeviceStateKeys.Power]:
            raise DeviceCommunicationError("Power could not be set")

    async def power_off(self) -> None:
        """
        Turn off the Heat Pump. Performs the same task as the `Off` switch in the MELCloud interface
        """
        response_state = await self._request(EffectiveFlags.Power, Power=False)
        if response_state[InternalDeviceStateKeys.Power]:
            raise DeviceCommunicationError("Power could not be set")
