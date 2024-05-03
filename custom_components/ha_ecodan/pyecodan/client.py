import os
from typing import Dict, List

from aiohttp import ClientSession

from .device import Device
from .errors import DeviceAuthenticationError


class Client():
    """
    A client for communicating with an Ecodan Heatpump via MELCloud
    """

    base_url = "https://app.melcloud.com/Mitsubishi.Wifi.Client"

    def __init__(self,
                 username: str = os.getenv("ECODAN_USERNAME"),
                 password: str = os.getenv("ECODAN_PASSWORD"),
                 session: ClientSession = None):
        """
        :param username: MELCloud username. Default is taken from the environment variable `ECODAN_USERNAME`
        :param password: MELCloud password. Default is taken from the environment variable `ECODAN_PASSWORD`
        """
        self._username = username
        self._password = password
        self._context_key = None
        self._session = session or ClientSession()

    async def device_request(self, endpoint: str, state: Dict):
        if self._context_key is None:
            await self.login()

        auth_header = {"X-MitsContextKey": self._context_key}
        url = f"{Client.base_url}/Device/{endpoint}"
        async with self._session.post(url, headers=auth_header, json=state) as response:
            return await response.json()

    async def _user_request(self, endpoint) -> Dict:
        if self._context_key is None:
            await self.login()

        auth_header = {"X-MitsContextKey": self._context_key}
        url = f"{Client.base_url}/User/{endpoint}"
        async with self._session.get(url, headers=auth_header) as response:
            return await response.json()

    async def login(self) -> None:
        login_url = f"{Client.base_url}/Login/ClientLogin"
        login_data = {
            "Email": self._username,
            "Password": self._password,
            "Language": 0,
            "AppVersion": "1.26.2.0",
            "Persist": True,
            "CaptchaResponse": None
        }
        async with self._session.post(login_url, json=login_data) as response:
            response_data = await response.json()
            if response_data["ErrorId"] is not None:
                raise DeviceAuthenticationError("login error")
            self._context_key = response_data["LoginData"]["ContextKey"]

    async def get_device(self, device_id: str) -> Device | None:
        for location in await self._user_request("ListDevices"):
            structure = location["Structure"]
            for device in structure["Devices"]:
                if device["DeviceID"] == device_id:
                    return Device(self, device)

        return None

    async def list_devices(self) -> Dict:
        devices = {}
        for location in await self._user_request("ListDevices"):
            structure = location["Structure"]
            location_name = location["Name"]
            for device in structure["Devices"]:
                devices[device["DeviceName"]] = {
                    "location_name": location_name,
                    "id": device["DeviceID"]
                }

        return devices

    async def __aenter__(self) -> "Client":
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:
        await self._session.__aexit__(exc_type, exc_val, exc_tb)
