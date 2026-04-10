"""Tests for the data models."""

from __future__ import annotations

import pytest

from duco.models import (
    ApiInfo,
    BoardInfo,
    DiagComponent,
    DiagStatus,
    NetworkType,
    Node,
    NodeConfig,
    NodeGeneralInfo,
    NodeSensorInfo,
    NodeType,
    NodeVentilationInfo,
    SystemConfig,
    VentilationMode,
    VentilationState,
    Zone,
    ZoneGroup,
)


class TestApiInfo:
    """Test ApiInfo dataclass."""

    def test_create(self):
        info = ApiInfo(api_version="2.5")
        assert info.api_version == "2.5"

    def test_frozen(self):
        info = ApiInfo(api_version="2.5")
        with pytest.raises(AttributeError):
            info.api_version = "3.0"  # type: ignore[misc]


class TestBoardInfo:
    """Test BoardInfo dataclass."""

    def test_create(self):
        board = BoardInfo(
            box_name="SILENT_CONNECT",
            box_sub_type_name="Eu",
            serial_board_box="RS2420002577",
            serial_board_comm="PS2424005629",
            serial_duco_box="n/a",
            serial_duco_comm="P369348-241126-033",
            time=1775082497,
        )
        assert board.box_name == "SILENT_CONNECT"
        assert board.box_sub_type_name == "Eu"
        assert board.time == 1775082497

    def test_frozen(self):
        board = BoardInfo(
            box_name="SILENT_CONNECT",
            box_sub_type_name="Eu",
            serial_board_box="RS2420002577",
            serial_board_comm="PS2424005629",
            serial_duco_box="n/a",
            serial_duco_comm="P369348-241126-033",
            time=1775082497,
        )
        with pytest.raises(AttributeError):
            board.box_name = "OTHER"  # type: ignore[misc]


class TestDiagComponent:
    """Test DiagComponent dataclass."""

    def test_create(self):
        comp = DiagComponent(component="Ventilation", status=DiagStatus.OK)
        assert comp.component == "Ventilation"
        assert comp.status == DiagStatus.OK


class TestNodeSensorInfo:
    """Test NodeSensorInfo dataclass."""

    def test_full(self):
        sensor = NodeSensorInfo(co2=536, iaq_co2=100, rh=35.5, iaq_rh=83)
        assert sensor.co2 == 536
        assert sensor.iaq_co2 == 100
        assert sensor.rh == 35.5
        assert sensor.iaq_rh == 83

    def test_co2_only(self):
        sensor = NodeSensorInfo(co2=536, iaq_co2=100)
        assert sensor.co2 == 536
        assert sensor.iaq_co2 == 100
        assert sensor.rh is None
        assert sensor.iaq_rh is None

    def test_rh_only(self):
        sensor = NodeSensorInfo(rh=40.0, iaq_rh=90)
        assert sensor.co2 is None
        assert sensor.iaq_co2 is None
        assert sensor.rh == 40.0
        assert sensor.iaq_rh == 90

    def test_optional_fields_default_none(self):
        sensor = NodeSensorInfo()
        assert sensor.co2 is None
        assert sensor.iaq_co2 is None
        assert sensor.rh is None
        assert sensor.iaq_rh is None


class TestNodeVentilationInfo:
    """Test NodeVentilationInfo dataclass."""

    def test_create(self):
        vent = NodeVentilationInfo(
            state=VentilationState.CNT1,
            time_state_remain=0,
            time_state_end=0,
            mode=VentilationMode.MANU,
            flow_lvl_tgt=15,
        )
        assert vent.state == VentilationState.CNT1
        assert vent.flow_lvl_tgt == 15

    def test_flow_lvl_tgt_optional(self):
        vent = NodeVentilationInfo(
            state=VentilationState.CNT1,
            time_state_remain=0,
            time_state_end=0,
            mode=VentilationMode.NONE,
        )
        assert vent.flow_lvl_tgt is None


class TestNodeGeneralInfo:
    """Test NodeGeneralInfo dataclass."""

    def test_create(self):
        general = NodeGeneralInfo(
            node_type=NodeType.BOX,
            sub_type=1,
            network_type=NetworkType.VIRT,
            parent=0,
            asso=0,
            name="",
            identify=0,
        )
        assert general.node_type == NodeType.BOX
        assert general.parent == 0


class TestNode:
    """Test Node dataclass."""

    def _make_general(self, node_type=NodeType.BOX, network_type=NetworkType.VIRT, parent=0):
        return NodeGeneralInfo(
            node_type=node_type,
            sub_type=0,
            network_type=network_type,
            parent=parent,
            asso=0,
            name="",
            identify=0,
        )

    def _make_ventilation(self, state=VentilationState.CNT1, mode=VentilationMode.MANU):
        return NodeVentilationInfo(
            state=state,
            time_state_remain=0,
            time_state_end=0,
            mode=mode,
        )

    def test_box_node(self):
        node = Node(
            node_id=1,
            general=self._make_general(),
            ventilation=self._make_ventilation(),
        )
        assert node.node_id == 1
        assert node.general.node_type == NodeType.BOX
        assert node.sensor is None

    def test_sensor_node(self):
        node = Node(
            node_id=2,
            general=self._make_general(node_type=NodeType.UCCO2, network_type=NetworkType.RF, parent=1),
            ventilation=self._make_ventilation(mode=VentilationMode.NONE),
            sensor=NodeSensorInfo(co2=536, iaq_co2=100),
        )
        assert node.sensor is not None
        assert node.sensor.co2 == 536

    def test_frozen(self):
        node = Node(node_id=1, general=self._make_general())
        with pytest.raises(AttributeError):
            node.node_id = 99  # type: ignore[misc]


class TestZoneGroup:
    """Test ZoneGroup dataclass."""

    def test_create(self):
        group = ZoneGroup(group_id=1, nodes=[2, 113])
        assert group.group_id == 1
        assert group.nodes == [2, 113]

    def test_empty_nodes_default(self):
        group = ZoneGroup(group_id=1)
        assert group.nodes == []


class TestZone:
    """Test Zone dataclass."""

    def test_create(self):
        zone = Zone(
            zone_id=1,
            name="VentEtaCentral",
            groups=[ZoneGroup(group_id=1, nodes=[2, 113])],
        )
        assert zone.zone_id == 1
        assert zone.name == "VentEtaCentral"
        assert len(zone.groups) == 1

    def test_empty_groups_default(self):
        zone = Zone(zone_id=1, name="Test")
        assert zone.groups == []


class TestSystemConfig:
    """Test SystemConfig dataclass."""

    def _make(self, **kwargs: object) -> SystemConfig:
        defaults: dict[str, object] = {
            "time_zone": 1,
            "dst": 1,
            "modbus_addr": 1,
            "modbus_offset": 1,
            "lan_mode": 1,
            "lan_dhcp": 1,
            "lan_static_ip": "0.0.0.0",
            "lan_static_net_mask": "255.255.255.0",
            "lan_static_default_gateway": "0.0.0.0",
            "lan_static_dns": "8.8.8.8",
            "lan_wifi_client_ssid": "IoT Wi-Fi",
            "lan_wifi_client_key": "",
            "auto_reboot_comm_period": 7,
            "auto_reboot_comm_time": 0,
        }
        defaults.update(kwargs)
        return SystemConfig(**defaults)  # type: ignore[arg-type]

    def test_create(self):
        config = self._make()
        assert config.time_zone == 1
        assert config.lan_wifi_client_ssid == "IoT Wi-Fi"
        assert config.auto_reboot_comm_period == 7

    def test_frozen(self):
        config = self._make()
        with pytest.raises(AttributeError):
            config.time_zone = 2  # type: ignore[misc]


class TestNodeConfig:
    """Tests for the NodeConfig model."""

    def test_create(self):
        config = NodeConfig(node_id=2, name="Living Room")
        assert config.node_id == 2
        assert config.name == "Living Room"

    def test_empty_name(self):
        config = NodeConfig(node_id=1, name="")
        assert config.name == ""

    def test_frozen(self):
        config = NodeConfig(node_id=2, name="Living Room")
        with pytest.raises(AttributeError):
            config.name = "Other"  # type: ignore[misc]
