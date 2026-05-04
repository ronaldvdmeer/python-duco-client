"""Integration tests against a live Duco box.

Run with:
    pytest tests/integration/ -v
    pytest tests/integration/ -v --duco-host=192.168.1.x
    DUCO_HOST=192.168.1.x pytest tests/integration/ -v
"""

from __future__ import annotations

import pytest

from duco.client import DucoClient
from duco.models import ApiInfo, BoardInfo, DiagComponent, LanInfo, Node, Zone

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# API info
# ---------------------------------------------------------------------------


async def test_get_api_info(live_client: DucoClient) -> None:
    info = await live_client.async_get_api_info()
    assert isinstance(info, ApiInfo)
    assert info.api_version, "api_version should not be empty"
    assert info.public_api_version, "public_api_version should not be empty"
    assert isinstance(info.endpoints, list)


# ---------------------------------------------------------------------------
# Board info
# ---------------------------------------------------------------------------


async def test_get_board_info(live_client: DucoClient) -> None:
    board = await live_client.async_get_board_info()
    assert isinstance(board, BoardInfo)
    assert board.box_name, "box_name should not be empty"
    assert board.serial_board_box, "serial_board_box should not be empty"
    assert board.time > 0
    assert board.public_api_version is not None


# ---------------------------------------------------------------------------
# LAN info
# ---------------------------------------------------------------------------


async def test_get_lan_info(live_client: DucoClient) -> None:
    lan = await live_client.async_get_lan_info()
    assert isinstance(lan, LanInfo)
    assert lan.ip, "ip should not be empty"
    assert lan.mac, "mac should not be empty"
    assert lan.rssi_wifi < 0, "RSSI should be a negative dBm value"


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------


async def test_get_diagnostics(live_client: DucoClient) -> None:
    diags = await live_client.async_get_diagnostics()
    assert isinstance(diags, list)
    assert len(diags) > 0
    for diag in diags:
        assert isinstance(diag, DiagComponent)
        assert diag.component
        assert diag.status


# ---------------------------------------------------------------------------
# Write requests remaining
# ---------------------------------------------------------------------------


async def test_get_write_req_remaining(live_client: DucoClient) -> None:
    remaining = await live_client.async_get_write_req_remaining()
    assert isinstance(remaining, int)
    assert remaining >= 0


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------


async def test_get_nodes(live_client: DucoClient) -> None:
    nodes = await live_client.async_get_nodes()
    assert isinstance(nodes, list)
    assert len(nodes) > 0
    for node in nodes:
        assert isinstance(node, Node)
        assert node.node_id > 0
        assert node.general.node_type


async def test_get_node_ids(live_client: DucoClient) -> None:
    ids = await live_client.async_get_node_ids()
    assert isinstance(ids, list)
    assert len(ids) > 0
    assert all(isinstance(i, int) for i in ids)


async def test_get_node(live_client: DucoClient) -> None:
    """Fetch node 1 (the BOX node) individually."""
    node = await live_client.async_get_node(1)
    assert isinstance(node, Node)
    assert node.node_id == 1
    assert node.general.node_type == "BOX"


async def test_nodes_match_node_ids(live_client: DucoClient) -> None:
    """Node IDs from /nodes and /info/nodes must be consistent."""
    ids = await live_client.async_get_node_ids()
    nodes = await live_client.async_get_nodes()
    node_ids_from_nodes = {n.node_id for n in nodes}
    assert set(ids) == node_ids_from_nodes


# ---------------------------------------------------------------------------
# Zones
# ---------------------------------------------------------------------------


async def test_get_zones(live_client: DucoClient) -> None:
    zones = await live_client.async_get_zones()
    assert isinstance(zones, list)
    assert len(zones) > 0
    for zone in zones:
        assert isinstance(zone, Zone)
        assert zone.zone_id > 0


async def test_get_zone(live_client: DucoClient) -> None:
    """Fetch zone 1 individually."""
    zone = await live_client.async_get_zone(1)
    assert isinstance(zone, Zone)
    assert zone.zone_id == 1


# ---------------------------------------------------------------------------
# Ventilation state round-trip (non-destructive)
# ---------------------------------------------------------------------------


async def test_set_ventilation_state_round_trip(live_client: DucoClient) -> None:
    """Set node 1 to MAN1, verify, then restore original state."""
    nodes = await live_client.async_get_nodes()
    box_node = next(n for n in nodes if n.general.node_type == "BOX")
    assert box_node.ventilation is not None
    original_state = box_node.ventilation.state

    try:
        await live_client.async_set_ventilation_state(box_node.node_id, "MAN1")
        updated = await live_client.async_get_node(box_node.node_id)
        assert updated.ventilation is not None
        assert updated.ventilation.state == "MAN1"
    finally:
        # Always restore original state
        await live_client.async_set_ventilation_state(box_node.node_id, original_state)
