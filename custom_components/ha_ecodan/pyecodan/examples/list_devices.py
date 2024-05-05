import asyncio

import pyecodan
from pyecodan.device import OperationMode


async def main():
    async with pyecodan.Client() as client:
        devices = await client.list_devices()
        device = devices["Naze View"]
        device = await client.get_device(device["id"])

        await device.set_operation_mode(OperationMode.Room)
        print(device.name)
        print(device.id)
        print(device.operation_mode)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
