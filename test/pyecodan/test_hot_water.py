import pytest

from custom_components.ha_ecodan.pyecodan.device import Device

from unittest.mock import Mock, AsyncMock


@pytest.mark.parametrize("force_hot_water", [True, False])
def test_hot_water_mode_from_state(melcloud, force_hot_water):
    client = Mock()
    device = Device(client, melcloud.device_state_with(ForcedHotWaterMode=force_hot_water))

    assert device.forced_hot_water is force_hot_water


@pytest.mark.asyncio
@pytest.mark.parametrize("force_hot_water", [True, False])
async def test_hot_water_mode_from_state(melcloud, force_hot_water):
    client = Mock()
    client.device_request = AsyncMock(return_value=melcloud.response_with(ForcedHotWaterMode=force_hot_water))

    device = Device(client, melcloud.device_state)
    await device.force_hot_water(force_hot_water)

    client.device_request.assert_awaited_with(
        melcloud.request_with(EffectiveFlags=65536, ForcedHotWaterMode=force_hot_water))
