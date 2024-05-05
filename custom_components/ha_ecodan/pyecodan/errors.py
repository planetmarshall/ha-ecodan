class DeviceCommunicationError(Exception):
    """An error communicating with the device."""

    def __init__(self, *args: object) -> None:
        """Create an error instance."""
        super().__init__(*args)


class DeviceAuthenticationError(Exception):
    """An error authenticating with MELCloud."""

    def __init__(self, *args: object) -> None:
        """Create an error instance."""
        super().__init__(*args)
