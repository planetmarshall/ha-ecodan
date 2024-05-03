import asyncio

import pyecodan


async def main():
    async with pyecodan.Client() as client:
        devices = await client.list_devices()
        device_id = [device["id"] for device in devices if device["name"] == "Naze View"]
        device = await client.get_device(device_id[0])
        print(device.name)
        await device.power_on()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
