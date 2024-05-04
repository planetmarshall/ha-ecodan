import asyncio

import pyecodan


async def main():
    async with pyecodan.Client() as client:
        devices = await client.list_devices()
        device = devices["Naze View"]
        device = await client.get_device(device["id"])
        print(device.name)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
