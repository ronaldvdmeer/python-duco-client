"""Tests for the DucoClient."""

from __future__ import annotations

import aiohttp
import pytest
from aioresponses import aioresponses

from duco.client import DucoClient
from duco.exceptions import DucoConnectionError, DucoError

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
    assert diags[0].status == "Ok"


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
    assert box.general.node_type == "BOX"
    assert box.general.network_type == "VIRT"
    assert box.ventilation is not None
    assert box.ventilation.state == "CNT1"
    assert box.ventilation.flow_lvl_tgt == 15
    assert box.sensor is None

    ucco2 = nodes[1]
    assert ucco2.node_id == 2
    assert ucco2.general.node_type == "UCCO2"
    assert ucco2.general.network_type == "RF"
    assert ucco2.sensor is not None
    assert ucco2.sensor.co2 == 536
    assert ucco2.sensor.iaq_co2 == 100

    bsrh = nodes[2]
    assert bsrh.node_id == 113
    assert bsrh.general.node_type == "BSRH"
    assert bsrh.sensor is None


# ---------------------------------------------------------------------------
# async_get_node
# ---------------------------------------------------------------------------


async def test_get_node(client, base_url, nodes_data):
    single_node = nodes_data["Nodes"][0]
    with aioresponses() as m:
        m.get(f"{base_url}/info/nodes/1", payload=single_node)
        node = await client.async_get_node(1)
    assert node.node_id == 1
    assert node.general.node_type == "BOX"


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
