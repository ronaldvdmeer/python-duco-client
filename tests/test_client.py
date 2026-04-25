"""Tests for the DucoClient."""

from __future__ import annotations

import time

import aiohttp
import pytest
from aioresponses import aioresponses

from duco.client import DucoClient
from duco.exceptions import DucoAuthenticationError, DucoConnectionError, DucoError, DucoRateLimitError
from duco.models import DiagStatus, NetworkType, NodeType, VentilationState

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_PRELOADED_API_KEY = "test-api-key-preloaded-for-unit-tests"


@pytest.fixture
async def client(mock_host):
    """DucoClient with a pre-loaded API key so tests don't trigger auth."""
    async with aiohttp.ClientSession() as session:
        c = DucoClient(session=session, host=mock_host, scheme="http")
        c._api_key = _PRELOADED_API_KEY
        c._api_key_day = int(time.time()) // 86400
        yield c


@pytest.fixture
async def unauthenticated_client(mock_host):
    """DucoClient without a pre-loaded API key for testing auth logic."""
    async with aiohttp.ClientSession() as session:
        yield DucoClient(session=session, host=mock_host, scheme="http")


# ---------------------------------------------------------------------------
# async_get_api_info
# ---------------------------------------------------------------------------


async def test_get_api_info(client, base_url, api_info_data):
    with aioresponses() as m:
        m.get(f"{base_url}/api", payload=api_info_data)
        info = await client.async_get_api_info()
    assert info.api_version == "2.5"


# ---------------------------------------------------------------------------
# async_get_board_info
# ---------------------------------------------------------------------------


async def test_get_board_info(client, base_url, board_info_data):
    with aioresponses() as m:
        m.get(
            f"{base_url}/info?module=General&submodule=Board",
            payload=board_info_data,
        )
        board = await client.async_get_board_info()
    assert board.box_name == "SILENT_CONNECT"
    assert board.box_sub_type_name == "Eu"
    assert board.serial_board_box == "RS2420002577"
    assert board.serial_board_comm == "PS2424005629"
    assert board.serial_duco_box == "n/a"
    assert board.serial_duco_comm == "P369348-241126-033"
    assert board.time == 1775082497


# ---------------------------------------------------------------------------
# async_get_lan_info
# ---------------------------------------------------------------------------


async def test_get_lan_info(client, base_url, lan_info_data):
    with aioresponses() as m:
        m.get(
            f"{base_url}/info?module=General&submodule=Lan",
            payload=lan_info_data,
        )
        lan = await client.async_get_lan_info()
    assert lan.mode == "WIFI_CLIENT"
    assert lan.ip == "192.168.3.94"
    assert lan.rssi_wifi == -44


async def test_get_lan_info_ethernet(client, base_url, lan_info_ethernet_data):
    with aioresponses() as m:
        m.get(
            f"{base_url}/info?module=General&submodule=Lan",
            payload=lan_info_ethernet_data,
        )
        lan = await client.async_get_lan_info()
    assert lan.mode == "ETHERNET"
    assert lan.ip == "192.168.1.97"
    assert lan.rssi_wifi is None


# ---------------------------------------------------------------------------
# async_get_diagnostics
# ---------------------------------------------------------------------------


async def test_get_diagnostics(client, base_url, diag_data):
    with aioresponses() as m:
        m.get(
            f"{base_url}/info?module=Diag",
            payload=diag_data,
        )
        diags = await client.async_get_diagnostics()
    assert len(diags) == 3
    assert diags[0].component == "Ventilation"
    assert diags[0].status == DiagStatus.OK


# ---------------------------------------------------------------------------
# async_get_nodes
# ---------------------------------------------------------------------------


async def test_get_nodes(client, base_url, nodes_data):
    with aioresponses() as m:
        m.get(f"{base_url}/info/nodes", payload=nodes_data)
        nodes = await client.async_get_nodes()

    assert len(nodes) == 3

    box = nodes[0]
    assert box.node_id == 1
    assert box.general.node_type == NodeType.BOX
    assert box.general.network_type == NetworkType.VIRT
    assert box.ventilation is not None
    assert box.ventilation.state == VentilationState.CNT1
    assert box.ventilation.flow_lvl_tgt == 15
    assert box.sensor is not None
    assert box.sensor.rh == 35.5
    assert box.sensor.iaq_rh == 83
    assert box.sensor.co2 is None
    assert box.sensor.temp == 27.9

    ucco2 = nodes[1]
    assert ucco2.node_id == 2
    assert ucco2.general.node_type == NodeType.UCCO2
    assert ucco2.general.network_type == NetworkType.RF
    assert ucco2.sensor is not None
    assert ucco2.sensor.co2 == 536
    assert ucco2.sensor.iaq_co2 == 100
    assert ucco2.sensor.rh is None
    assert ucco2.sensor.iaq_rh is None
    assert ucco2.sensor.temp == 19.8

    bsrh = nodes[2]
    assert bsrh.node_id == 113
    assert bsrh.general.node_type == NodeType.BSRH
    assert bsrh.sensor is not None
    assert bsrh.sensor.rh == 36.0
    assert bsrh.sensor.iaq_rh == 81
    assert bsrh.sensor.co2 is None
    assert bsrh.sensor.temp == 27.9


# ---------------------------------------------------------------------------
# async_get_node
# ---------------------------------------------------------------------------


async def test_get_node(client, base_url, nodes_data):
    single_node = nodes_data["Nodes"][0]
    with aioresponses() as m:
        m.get(f"{base_url}/info/nodes/1", payload=single_node)
        node = await client.async_get_node(1)
    assert node.node_id == 1
    assert node.general.node_type == NodeType.BOX


# ---------------------------------------------------------------------------
# async_get_node_ids
# ---------------------------------------------------------------------------


async def test_get_node_ids(client, base_url, node_ids_data):
    with aioresponses() as m:
        m.get(f"{base_url}/nodes", payload=node_ids_data)
        ids = await client.async_get_node_ids()
    assert ids == [1, 2, 113]


# ---------------------------------------------------------------------------
# async_get_zones
# ---------------------------------------------------------------------------


async def test_get_zones(client, base_url, zones_data):
    with aioresponses() as m:
        m.get(f"{base_url}/info/zones", payload=zones_data)
        zones = await client.async_get_zones()

    assert len(zones) == 1
    zone = zones[0]
    assert zone.zone_id == 1
    assert zone.name == "VentEtaCentral"
    assert len(zone.groups) == 1
    assert zone.groups[0].group_id == 1
    assert sorted(zone.groups[0].nodes) == [2, 113]


# ---------------------------------------------------------------------------
# async_get_zone_configs / async_get_zone_config
# ---------------------------------------------------------------------------


async def test_get_zone_configs(client, base_url, zone_configs_data):
    with aioresponses() as m:
        m.get(f"{base_url}/config/zones", payload=zone_configs_data)
        result = await client.async_get_zone_configs()

    assert len(result) == 1
    zone = result[0]
    assert zone.zone_id == 1
    assert zone.name == "VentEtaCentral"
    assert len(zone.groups) == 1
    assert zone.groups[0].group_id == 1
    assert sorted(zone.groups[0].nodes) == [2, 113]


async def test_get_zone_config(client, base_url, zone_config_data):
    with aioresponses() as m:
        m.get(f"{base_url}/config/zones/1", payload=zone_config_data)
        result = await client.async_get_zone_config(1)

    assert result.zone_id == 1
    assert result.name == "VentEtaCentral"
    assert len(result.groups) == 1
    assert result.groups[0].nodes == [2, 113]


async def test_set_zone_name(client, base_url):
    with aioresponses() as m:
        m.patch(f"{base_url}/config/zones/1", payload={})
        await client.async_set_zone_name(1, "Living Area")
    # No exception means success


# ---------------------------------------------------------------------------
# async_get_zone_group_config / async_set_zone_group_nodes
# ---------------------------------------------------------------------------


async def test_get_zone_group_config(client, base_url, zone_group_config_data):
    with aioresponses() as m:
        m.get(f"{base_url}/config/zones/1/groups/1", payload=zone_group_config_data)
        result = await client.async_get_zone_group_config(1, 1)

    assert result.group_id == 1
    assert sorted(result.nodes) == [2, 113]


async def test_set_zone_group_nodes(client, base_url):
    with aioresponses() as m:
        m.patch(f"{base_url}/config/zones/1/groups/1", payload={})
        await client.async_set_zone_group_nodes(1, 1, [2, 113])
    # No exception means success


# ---------------------------------------------------------------------------
# async_get_actions / async_get_node_actions / async_get_node_action_list
# ---------------------------------------------------------------------------


async def test_get_actions(client, base_url, actions_data):
    with aioresponses() as m:
        m.get(f"{base_url}/action", payload=actions_data)
        result = await client.async_get_actions()

    assert len(result) == 4
    set_time = result[0]
    assert set_time.action == "SetTime"
    assert set_time.val_type == "Integer"
    assert set_time.enum_values == []


async def test_get_node_actions(client, base_url, node_actions_data):
    with aioresponses() as m:
        m.get(f"{base_url}/action/nodes", payload=node_actions_data)
        result = await client.async_get_node_actions()

    assert len(result) == 2
    node1 = result[0]
    assert node1.node_id == 1
    assert len(node1.actions) == 2
    vent_action = node1.actions[0]
    assert vent_action.action == "SetVentilationState"
    assert vent_action.val_type == "Enum"
    assert "AUTO" in vent_action.enum_values
    assert "MAN3" in vent_action.enum_values


async def test_get_node_action_list(client, base_url, node_action_list_data):
    with aioresponses() as m:
        m.get(f"{base_url}/action/nodes/1", payload=node_action_list_data)
        result = await client.async_get_node_action_list(1)

    assert result.node_id == 1
    assert len(result.actions) == 2
    assert result.actions[0].action == "SetVentilationState"
    assert result.actions[1].action == "SetIdentify"
    assert result.actions[1].enum_values == []


# ---------------------------------------------------------------------------
# async_set_ventilation_state
# ---------------------------------------------------------------------------


async def test_set_ventilation_state(client, base_url):
    with aioresponses() as m:
        m.post(f"{base_url}/action/nodes/1", payload={})
        await client.async_set_ventilation_state(1, "MAN2")
    # No exception means success


# ---------------------------------------------------------------------------
# async_set_identify
# ---------------------------------------------------------------------------


async def test_set_identify(client, base_url):
    with aioresponses() as m:
        m.post(f"{base_url}/action/nodes/1", payload={})
        await client.async_set_identify(1, enabled=True)
    # No exception means success


# ---------------------------------------------------------------------------
# async_set_identify_all
# ---------------------------------------------------------------------------


async def test_set_identify_all(client, base_url):
    with aioresponses() as m:
        m.post(f"{base_url}/action", payload={})
        await client.async_set_identify_all(enabled=False)
    # No exception means success


# ---------------------------------------------------------------------------
# async_reconnect_wifi
# ---------------------------------------------------------------------------


async def test_reconnect_wifi(client, base_url):
    with aioresponses() as m:
        m.post(f"{base_url}/action", payload={})
        await client.async_reconnect_wifi()
    # No exception means success


# ---------------------------------------------------------------------------
# async_scan_wifi
# ---------------------------------------------------------------------------


async def test_scan_wifi(client, base_url):
    with aioresponses() as m:
        m.post(f"{base_url}/action", payload={})
        await client.async_scan_wifi()
    # No exception means success


# ---------------------------------------------------------------------------
# async_set_time / async_set_wifi_ap_mode
# ---------------------------------------------------------------------------


async def test_set_time(client, base_url):
    with aioresponses() as m:
        m.post(f"{base_url}/action", payload={})
        await client.async_set_time(1775082497)
    # No exception means success


async def test_set_wifi_ap_mode_enable(client, base_url):
    with aioresponses() as m:
        m.post(f"{base_url}/action", payload={})
        await client.async_set_wifi_ap_mode(enabled=True)
    # No exception means success


async def test_set_wifi_ap_mode_disable(client, base_url):
    with aioresponses() as m:
        m.post(f"{base_url}/action", payload={})
        await client.async_set_wifi_ap_mode(enabled=False)
    # No exception means success


# ---------------------------------------------------------------------------
# async_set_node_name
# ---------------------------------------------------------------------------


async def test_set_node_name(client, base_url):
    with aioresponses() as m:
        m.patch(f"{base_url}/config/nodes/2", payload={})
        await client.async_set_node_name(2, "CO2 Sensor")
    # No exception means success


# ---------------------------------------------------------------------------
# async_get_system_config
# ---------------------------------------------------------------------------


async def test_get_system_config(client, base_url, system_config_data):
    with aioresponses() as m:
        m.get(f"{base_url}/config?module=General", payload=system_config_data)
        config = await client.async_get_system_config()
    assert config.time_zone == 1
    assert config.dst == 1
    assert config.modbus_addr == 1
    assert config.modbus_offset == 1
    assert config.lan_mode == 1
    assert config.lan_dhcp == 1
    assert config.lan_static_ip == "0.0.0.0"
    assert config.lan_static_net_mask == "255.255.255.0"
    assert config.lan_static_default_gateway == "0.0.0.0"
    assert config.lan_static_dns == "8.8.8.8"
    assert config.lan_wifi_client_ssid == "IoT Wi-Fi"
    assert config.lan_wifi_client_key == ""
    assert config.auto_reboot_comm_period == 7
    assert config.auto_reboot_comm_time == 0


# ---------------------------------------------------------------------------
# async_set_system_config
# ---------------------------------------------------------------------------


async def test_set_system_config_time_zone(client, base_url):
    with aioresponses() as m:
        m.patch(f"{base_url}/config", payload={})
        await client.async_set_system_config(time_zone=2)
    # No exception means success


async def test_set_system_config_multiple_fields(client, base_url):
    with aioresponses() as m:
        m.patch(f"{base_url}/config", payload={})
        await client.async_set_system_config(
            time_zone=2,
            dst=0,
            auto_reboot_comm_period=14,
        )
    # No exception means success


async def test_set_system_config_wifi(client, base_url):
    with aioresponses() as m:
        m.patch(f"{base_url}/config", payload={})
        await client.async_set_system_config(
            lan_wifi_client_ssid="MyNetwork",
            lan_wifi_client_key="secret",
        )
    # No exception means success


async def test_get_node_configs(client, base_url, node_configs_data):
    with aioresponses() as m:
        m.get(f"{base_url}/config/nodes", payload=node_configs_data)
        result = await client.async_get_node_configs()
    assert len(result) == 3
    assert result[0].node_id == 1
    assert result[0].name == ""
    assert result[1].node_id == 2
    assert result[1].name == "Living Room"
    assert result[2].node_id == 113
    assert result[2].name == ""


async def test_get_node_config(client, base_url, node_config_data):
    with aioresponses() as m:
        m.get(f"{base_url}/config/nodes/2", payload=node_config_data)
        result = await client.async_get_node_config(2)
    assert result.node_id == 2
    assert result.name == "Living Room"


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


async def test_connection_error(unauthenticated_client, base_url, board_info_data, lan_info_data):
    with aioresponses() as m:
        m.get(
            f"{base_url}/info?module=General&submodule=Board",
            payload=board_info_data,
        )
        m.get(
            f"{base_url}/info?module=General&submodule=Lan",
            payload=lan_info_data,
        )
        m.get(
            f"{base_url}/api",
            exception=aiohttp.ClientConnectionError("unreachable"),
        )
        with pytest.raises(DucoConnectionError):
            await unauthenticated_client.async_get_api_info()


async def test_http_error(client, base_url):
    with aioresponses() as m:
        m.get(f"{base_url}/api", status=500)
        with pytest.raises(DucoError):
            await client.async_get_api_info()


async def test_rate_limit_error(client, base_url):
    with aioresponses() as m:
        m.post(f"{base_url}/action/nodes/1", status=429)
        with pytest.raises(DucoRateLimitError):
            await client.async_set_ventilation_state(1, "MAN2")


async def test_rate_limit_error_is_duco_error(client, base_url):
    """DucoRateLimitError must be catchable as DucoError (inheritance)."""
    with aioresponses() as m:
        m.post(f"{base_url}/action/nodes/1", status=429)
        with pytest.raises(DucoError):
            await client.async_set_ventilation_state(1, "MAN2")


# ---------------------------------------------------------------------------
# API key authentication
# ---------------------------------------------------------------------------


async def test_api_key_sent_in_request_header(client, base_url, api_info_data):
    """The Api-Key header is included in every authenticated request."""
    with aioresponses() as m:
        m.get(f"{base_url}/api", payload=api_info_data)
        await client.async_get_api_info()
        request = list(m.requests.values())[0][0]
    assert request.kwargs["headers"]["Api-Key"] == _PRELOADED_API_KEY


async def test_api_key_fetched_on_first_request(
    unauthenticated_client, base_url, board_info_data, lan_info_data, api_info_data
):
    """API key is generated from /info on the first authenticated request."""
    with aioresponses() as m:
        m.get(
            f"{base_url}/info?module=General&submodule=Board",
            payload=board_info_data,
        )
        m.get(
            f"{base_url}/info?module=General&submodule=Lan",
            payload=lan_info_data,
        )
        m.get(f"{base_url}/api", payload=api_info_data)
        await unauthenticated_client.async_get_api_info()
    assert unauthenticated_client._api_key is not None
    assert len(unauthenticated_client._api_key) == 64


async def test_api_key_cached_within_same_day(
    unauthenticated_client, base_url, board_info_data, lan_info_data, api_info_data
):
    """API key is not re-fetched when it is still valid for today."""
    with aioresponses() as m:
        m.get(
            f"{base_url}/info?module=General&submodule=Board",
            payload=board_info_data,
        )
        m.get(
            f"{base_url}/info?module=General&submodule=Lan",
            payload=lan_info_data,
        )
        m.get(f"{base_url}/api", payload=api_info_data)
        m.get(f"{base_url}/api", payload=api_info_data)
        await unauthenticated_client.async_get_api_info()
        first_key = unauthenticated_client._api_key
        await unauthenticated_client.async_get_api_info()
    # Key should be identical – no new /info fetch happened
    assert unauthenticated_client._api_key == first_key


async def test_api_key_generation_failure_raises_authentication_error(unauthenticated_client, base_url):
    """DucoAuthenticationError is raised when /info is unreachable."""
    with aioresponses():
        with pytest.raises(DucoAuthenticationError):
            await unauthenticated_client.async_get_api_info()


async def test_authentication_error_is_duco_error(unauthenticated_client, base_url):
    """DucoAuthenticationError must be catchable as DucoError (inheritance)."""
    with aioresponses():
        with pytest.raises(DucoError):
            await unauthenticated_client.async_get_api_info()
