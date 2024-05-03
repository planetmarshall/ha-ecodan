class DeviceCommunicationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DeviceAuthenticationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
