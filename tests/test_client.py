"""Tests for the DucoClient."""

from __future__ import annotations

import aiohttp
import pytest
from aioresponses import aioresponses

from duco.client import DucoClient
from duco.exceptions import DucoConnectionError, DucoError
from duco.models import DiagStatus, NetworkType, NodeType, VentilationState

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
async def client(mock_host):
    """DucoClient with a real aiohttp session."""
    async with aiohttp.ClientSession() as session:
        yield DucoClient(session=session, host=mock_host)


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

    ucco2 = nodes[1]
    assert ucco2.node_id == 2
    assert ucco2.general.node_type == NodeType.UCCO2
    assert ucco2.general.network_type == NetworkType.RF
    assert ucco2.sensor is not None
    assert ucco2.sensor.co2 == 536
    assert ucco2.sensor.iaq_co2 == 100
    assert ucco2.sensor.rh is None
    assert ucco2.sensor.iaq_rh is None

    bsrh = nodes[2]
    assert bsrh.node_id == 113
    assert bsrh.general.node_type == NodeType.BSRH
    assert bsrh.sensor is not None
    assert bsrh.sensor.rh == 36.0
    assert bsrh.sensor.iaq_rh == 81
    assert bsrh.sensor.co2 is None


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


async def test_connection_error(mock_host):
    async with aiohttp.ClientSession() as session:
        client = DucoClient(session=session, host=mock_host)
        with aioresponses() as m:
            m.get(
                f"http://{mock_host}/api",
                exception=aiohttp.ClientConnectionError("unreachable"),
            )
            with pytest.raises(DucoConnectionError):
                await client.async_get_api_info()


async def test_http_error(client, base_url):
    with aioresponses() as m:
        m.get(f"{base_url}/api", status=500)
        with pytest.raises(DucoError):
            await client.async_get_api_info()
