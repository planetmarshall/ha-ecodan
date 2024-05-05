from enum import IntEnum, IntFlag

from .errors import DeviceCommunicationError


class EffectiveFlags(IntFlag):
    Update = 0x0
    Power = 0x1
    OperationModeZone1 = 0x1000004000028


class DeviceStateKeys:
    ErrorMessage = "ErrorMessage"
    FlowTemperature = "FlowTemperature"
    OutdoorTemperature = "OutdoorTemperature"
    HotWaterTemperature = "TankWaterTemperature"
    OperationModeZone1 = "OperationModeZone1"
    Power = "Power"


class DevicePropertyKeys:
    DeviceName = "DeviceName"
    DeviceID = "DeviceID"
    BuildingID = "BuildingID"
    EffectiveFlags = "EffectiveFlags"


class OperationMode(IntEnum):
    Room = 0,
    Flow = 1,
    Curve = 2


class DeviceState:

    def __init__(self, device_state: dict):
        self._state = {}
        internal_device_state = device_state["Device"]

        for field in (
            DeviceStateKeys.FlowTemperature,
            DeviceStateKeys.Power,
            DeviceStateKeys.OutdoorTemperature,
            DeviceStateKeys.HotWaterTemperature,
            DeviceStateKeys.OperationModeZone1
        ):
            self._state[field] = internal_device_state[field]

        self._state[DevicePropertyKeys.DeviceID] = device_state[DevicePropertyKeys.DeviceID]
        self._state[DevicePropertyKeys.DeviceName] = device_state[DevicePropertyKeys.DeviceName]
        self._state[DevicePropertyKeys.BuildingID] = device_state[DevicePropertyKeys.BuildingID]


    def __getitem__(self, item):
        return self._state[item]

    def as_dict(self):
        return self._state

class Device:
    """
    Represents an Ecodan Heat Pump device
    """
    def __init__(self, client, device_state: dict):
        self._client = client
        self._state = DeviceState(device_state)

    @property
    def id(self):
        return self._state[DevicePropertyKeys.DeviceID]

    @property
    def name(self):
        return self._state[DevicePropertyKeys.DeviceName]

    @property
    def building_id(self):
        return self._state[DevicePropertyKeys.BuildingID]

    @property
    def operation_mode(self) -> OperationMode:
        return OperationMode(self._state[DeviceStateKeys.OperationModeZone1])

    async def _request(self, effective_flags: EffectiveFlags, **kwargs) -> dict:
        state = {
            #DevicePropertyKeys.BuildingID: self.building_id,
            DevicePropertyKeys.DeviceID: self.id,
            DevicePropertyKeys.EffectiveFlags: effective_flags
        }
        state.update(kwargs)
        return await self._client.device_request("SetAtw", state)

    async def get_state(self) -> dict:
        device = await self._client.get_device(self.id)
        self._state = device._state
        return self._state.as_dict()

    @property
    def data(self):
        return self._state.as_dict()

    @staticmethod
    def _check_response(response: dict):
        error_message = response[DeviceStateKeys.ErrorMessage]
        if error_message is not None:
            raise DeviceCommunicationError(error_message)

    async def set_operation_mode(self, operation_mode: OperationMode):
        """
        Set the operation mode to Room (auto), Flow (set flow temperature manually) or Curve.
        """
        response_state = await self._request(EffectiveFlags.OperationModeZone1, OperationModeZone1=operation_mode)
        self._check_response(response_state)

    async def power_on(self) -> None:
        """
        Turn on the Heat Pump. Performs the same task as the `On` switch in the MELCloud interface
        """
        response_state = await self._request(EffectiveFlags.Power, Power=True)
        if not response_state[DeviceStateKeys.Power]:
            raise DeviceCommunicationError("Power could not be set")

    async def power_off(self) -> None:
        """
        Turn off the Heat Pump. Performs the same task as the `Off` switch in the MELCloud interface
        """
        response_state = await self._request(EffectiveFlags.Power, Power=False)
        if response_state[DeviceStateKeys.Power]:
            raise DeviceCommunicationError("Power could not be set")
