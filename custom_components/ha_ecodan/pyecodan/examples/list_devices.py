import asyncio

from custom_components.ha_ecodan.pyecodan.client import Client
from custom_components.ha_ecodan.pyecodan.device import OperationMode


async def main():
    async with Client() as client:
        devices = await client.list_devices()
        device = devices["Naze View"]
        device = await client.get_device(device["id"])

        await device.force_hot_water(True)
        print(device.name)
        print(device.id)
        print(device.forced_hot_water)


if __name__ == "__main__":
    asyncio.run(main())
