"""Data models for the Duco ventilation API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class VentilationState(StrEnum):
    """Ventilation state values."""

    AUTO = "AUTO"
    AUT1 = "AUT1"
    AUT2 = "AUT2"
    AUT3 = "AUT3"
    MAN1 = "MAN1"
    MAN2 = "MAN2"
    MAN3 = "MAN3"
    EMPT = "EMPT"
    CNT1 = "CNT1"
    CNT2 = "CNT2"
    CNT3 = "CNT3"
    MAN1x2 = "MAN1x2"
    MAN2x2 = "MAN2x2"
    MAN3x2 = "MAN3x2"
    MAN1x3 = "MAN1x3"
    MAN2x3 = "MAN2x3"
    MAN3x3 = "MAN3x3"


class NodeType(StrEnum):
    """Known node types."""

    BOX = "BOX"
    UCCO2 = "UCCO2"
    BSRH = "BSRH"


class NetworkType(StrEnum):
    """Network connection types."""

    VIRT = "VIRT"
    RF = "RF"


class VentilationMode(StrEnum):
    """Ventilation mode values."""

    MANU = "MANU"
    AUTO = "AUTO"
    NONE = "-"


@dataclass(frozen=True, slots=True)
class ApiInfo:
    """API version and endpoint information.

    Attributes:
        api_version: Public API version string (e.g. ``"2.5"``).
    """

    api_version: str


@dataclass(frozen=True, slots=True)
class BoardInfo:
    """Box board information.

    Attributes:
        box_name: Type name of the box (e.g. ``"SILENT_CONNECT"``).
        box_sub_type_name: Subtype (e.g. ``"Eu"``).
        serial_board_box: Serial number of the box board.
        serial_board_comm: Serial number of the communication board.
        serial_duco_box: Duco serial number for the box.
        serial_duco_comm: Duco serial number for the communication module.
        time: Current Unix timestamp on the box.
    """

    box_name: str
    box_sub_type_name: str
    serial_board_box: str
    serial_board_comm: str
    serial_duco_box: str
    serial_duco_comm: str
    time: int


@dataclass(frozen=True, slots=True)
class LanInfo:
    """Network / LAN information.

    Attributes:
        mode: Network mode (e.g. ``"WIFI_CLIENT"``).
        ip: Current IP address.
        net_mask: Subnet mask.
        default_gateway: Default gateway address.
        dns: DNS server address.
        mac: MAC address.
        host_name: Hostname on the network.
        rssi_wifi: WiFi signal strength in dBm.
    """

    mode: str
    ip: str
    net_mask: str
    default_gateway: str
    dns: str
    mac: str
    host_name: str
    rssi_wifi: int


@dataclass(frozen=True, slots=True)
class DiagComponent:
    """Diagnostic subsystem status.

    Attributes:
        component: Component name (e.g. ``"Ventilation"``).
        status: Status string (e.g. ``"Ok"``).
    """

    component: str
    status: str


@dataclass(frozen=True, slots=True)
class NodeSensorInfo:
    """Sensor readings for a node.

    Attributes:
        co2: CO2 concentration in ppm, or ``None`` if not available.
        iaq_co2: Indoor Air Quality index based on CO2 (0-100), or ``None``.
    """

    co2: int | None = None
    iaq_co2: int | None = None


@dataclass(frozen=True, slots=True)
class NodeVentilationInfo:
    """Ventilation state of a node.

    Attributes:
        state: Current ventilation state.
        time_state_remain: Remaining time in current state (seconds).
        time_state_end: End time of current state (Unix timestamp, 0 = permanent).
        mode: Ventilation mode.
        flow_lvl_tgt: Target flow level (only on BOX nodes), or ``None``.
    """

    state: VentilationState
    time_state_remain: int
    time_state_end: int
    mode: str
    flow_lvl_tgt: int | None = None


@dataclass(frozen=True, slots=True)
class NodeGeneralInfo:
    """General information about a node.

    Attributes:
        node_type: Node type (e.g. ``"BOX"``, ``"UCCO2"``).
        sub_type: Node subtype number.
        network_type: Connection type (``"VIRT"`` or ``"RF"``).
        parent: Parent node ID (0 = no parent).
        asso: Associated node ID (0 = no association).
        name: User-assigned name.
        identify: Identification mode (0 = off, 1 = on).
    """

    node_type: str
    sub_type: int
    network_type: str
    parent: int
    asso: int
    name: str
    identify: int


@dataclass(frozen=True, slots=True)
class Node:
    """A node (box, sensor, or valve) in the Duco system.

    Attributes:
        node_id: Unique node identifier.
        general: General node information.
        ventilation: Ventilation state, or ``None``.
        sensor: Sensor data, or ``None``.
    """

    node_id: int
    general: NodeGeneralInfo
    ventilation: NodeVentilationInfo | None = None
    sensor: NodeSensorInfo | None = None


@dataclass(frozen=True, slots=True)
class ZoneGroup:
    """A group within a zone.

    Attributes:
        group_id: Group identifier.
        nodes: List of node IDs in this group.
    """

    group_id: int
    nodes: list[int] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class Zone:
    """A ventilation zone.

    Attributes:
        zone_id: Zone identifier.
        name: Zone name.
        groups: Groups within this zone.
    """

    zone_id: int
    name: str
    groups: list[ZoneGroup] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class SystemConfig:
    """System configuration of the Duco box.

    Attributes:
        time_zone: UTC offset in hours (``-11`` to ``12``).
        dst: Daylight saving time enabled (``0`` or ``1``).
        modbus_addr: Modbus device address (``1`` to ``254``).
        modbus_offset: Modbus address offset (``0`` or ``1``).
        lan_mode: LAN mode (read-only on most boxes).
        lan_dhcp: DHCP enabled (``0`` = static, ``1`` = DHCP).
        lan_static_ip: Static IP address.
        lan_static_net_mask: Static subnet mask.
        lan_static_default_gateway: Static default gateway.
        lan_static_dns: Static DNS server.
        lan_wifi_client_ssid: WiFi SSID to connect to.
        lan_wifi_client_key: WiFi password.
        auto_reboot_comm_period: Auto-reboot period in days (``0`` = disabled, max ``365``).
        auto_reboot_comm_time: Auto-reboot time of day in minutes since midnight (``0``–``1439``).
    """

    time_zone: int
    dst: int
    modbus_addr: int
    modbus_offset: int
    lan_mode: int
    lan_dhcp: int
    lan_static_ip: str
    lan_static_net_mask: str
    lan_static_default_gateway: str
    lan_static_dns: str
    lan_wifi_client_ssid: str
    lan_wifi_client_key: str
    auto_reboot_comm_period: int
    auto_reboot_comm_time: int
