"""Async client for the Duco ventilation API."""

from __future__ import annotations

import json as _json
import ssl
import time as _time
from typing import Any

from aiohttp import ClientSession

from ._ssl import build_ssl_context
from .exceptions import (
    DucoAuthenticationError,
    DucoConnectionError,
    DucoError,
    DucoRateLimitError,
)
from .models import (
    ActionInfo,
    ApiInfo,
    BoardInfo,
    DiagComponent,
    DiagStatus,
    LanInfo,
    NetworkType,
    Node,
    NodeActions,
    NodeConfig,
    NodeGeneralInfo,
    NodeSensorInfo,
    NodeType,
    NodeVentilationInfo,
    SystemConfig,
    VentilationMode,
    Zone,
    ZoneGroup,
)


class _ApiKeyGenerator:
    """Generates the daily API key from board serial, MAC address, and device time."""

    def _transform_char(self, c1: str, c2: str) -> str:
        result = (ord(c1) ^ ord(c2)) & 127
        if result < 48:
            result = (result % 26) + 97
        elif 57 < result < 65:
            result = (result % 26) + 65
        elif 90 < result < 97 or result > 122:
            result = (result % 10) + 48
        return chr(result)

    def generate(self, board_serial: str, mac_address: str, device_time: int) -> str:
        """Generate a 64-character API key."""
        key = list("n4W2lNnb2IPnfBrXwSTzTlvmDvsbemYRvXBRWrfNtQJlMiQ8yPVRmGcoPd7szSu2")
        for i in range(min(len(mac_address), 32)):
            key[i] = self._transform_char(key[i], mac_address[i])
        for i in range(min(len(board_serial), 32)):
            key[i + 32] = self._transform_char(key[i + 32], board_serial[i])
        adjusted_time = device_time // 86400
        for i in range(16):
            if (adjusted_time & (1 << i)) != 0:
                idx = i * 4
                key[idx] = self._transform_char(key[idx], key[i * 2 + 32])
                key[idx + 1] = self._transform_char(key[idx + 1], key[63 - (i * 2)])
                key[idx + 2] = self._transform_char(key[idx], key[idx + 1])
                key[idx + 3] = self._transform_char(key[idx + 1], key[idx + 2])
        return "".join(key)


class DucoClient:
    """Async client for the Duco ventilation box REST API.

    Example::

        async with aiohttp.ClientSession() as session:
            client = DucoClient(session=session, host="192.168.3.94")
            info = await client.async_get_board_info()
            print(f"Box: {info.box_name}")

            nodes = await client.async_get_nodes()
            for node in nodes:
                print(f"Node {node.node_id}: {node.general.node_type}")
    """

    def __init__(
        self,
        session: ClientSession,
        host: str,
        scheme: str = "https",
        ssl_context: ssl.SSLContext | None = None,
    ) -> None:
        """Initialize the client.

        Args:
            session: aiohttp session for HTTP requests.
            host: IP address or hostname of the Duco box.
            scheme: URL scheme (default ``"https"``).
            ssl_context: Optional pre-built SSL context.  When provided the
                caller is responsible for constructing it (e.g. via
                :func:`duco.build_ssl_context` in an executor).  When omitted
                and *scheme* is ``"https"``, :func:`build_ssl_context` is
                called implicitly — which performs blocking I/O and should not
                be used inside an asyncio event loop.

        """
        self._session = session
        self._base_url = f"{scheme}://{host}"
        if ssl_context is not None:
            self._ssl_context: ssl.SSLContext | None = ssl_context
        elif scheme == "https":
            self._ssl_context = build_ssl_context()
        else:
            self._ssl_context = None
        self._api_key: str | None = None
        self._api_key_day: int = -1

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    async def _ensure_api_key(self) -> None:
        """Fetch and cache the daily API key from the Duco box."""
        today = int(_time.time()) // 86400
        if self._api_key is not None and self._api_key_day == today:
            return
        try:
            board_data = await self._request(
                "GET",
                "/info",
                params={"module": "General", "submodule": "Board"},
                _skip_auth=True,
            )
            lan_data = await self._request(
                "GET",
                "/info",
                params={"module": "General", "submodule": "Lan"},
                _skip_auth=True,
            )
        except DucoConnectionError:
            raise
        except DucoError as err:
            msg = f"Failed to fetch device info for API key generation: {err}"
            raise DucoAuthenticationError(msg) from err
        serial = board_data["General"]["Board"]["SerialBoardBox"]["Val"]
        device_time = board_data["General"]["Board"]["Time"]["Val"]
        mac = lan_data["General"]["Lan"]["Mac"]["Val"]
        self._api_key = _ApiKeyGenerator().generate(serial, mac, device_time)
        self._api_key_day = today

    async def _request(self, method: str, path: str, *, _skip_auth: bool = False, **kwargs: Any) -> Any:
        """Make a request to the Duco API.

        Args:
            method: HTTP method.
            path: API path (e.g. ``"/info"``).
            **kwargs: Additional arguments for the HTTP request.

        Returns:
            Parsed JSON response.

        Raises:
            DucoConnectionError: If the box is unreachable.
            DucoError: For API errors.

        """
        if not _skip_auth:
            await self._ensure_api_key()
        try:
            # The Duco box rejects JSON with spaces between tokens.
            # Serialize manually with compact separators when a json body is given.
            if "json" in kwargs:
                kwargs["data"] = _json.dumps(kwargs.pop("json"), separators=(",", ":")).encode()
                kwargs.setdefault("headers", {})["Content-Type"] = "application/json"
            if self._api_key is not None:
                kwargs.setdefault("headers", {})["Api-Key"] = self._api_key
            response = await self._session.request(
                method,
                f"{self._base_url}{path}",
                ssl=self._ssl_context if self._ssl_context is not None else True,
                **kwargs,
            )
        except Exception as err:
            msg = f"Failed to connect to Duco box: {err}"
            raise DucoConnectionError(msg) from err

        if response.status == 429:
            raise DucoRateLimitError()

        if response.status >= 400:
            text = await response.text()
            msg = f"Duco API error ({response.status}): {text}"
            raise DucoError(msg)

        return await response.json()

    @staticmethod
    def _val(data: dict[str, Any]) -> Any:
        """Extract the ``Val`` field from a Duco API value wrapper."""
        return data["Val"]

    # -------------------------------------------------------------------------
    # API info
    # -------------------------------------------------------------------------

    async def async_get_api_info(self) -> ApiInfo:
        """Get the API version information.

        Returns:
            API version info.

        """
        data = await self._request("GET", "/api")
        return ApiInfo(
            api_version=self._val(data["PublicApiVersion"]),
        )

    # -------------------------------------------------------------------------
    # Box info
    # -------------------------------------------------------------------------

    async def async_get_board_info(self) -> BoardInfo:
        """Get board information.

        Returns:
            Board info with serial numbers and box identification.

        """
        data = await self._request("GET", "/info", params={"module": "General", "submodule": "Board"})
        board = data["General"]["Board"]
        return BoardInfo(
            box_name=self._val(board["BoxName"]),
            box_sub_type_name=self._val(board["BoxSubTypeName"]),
            serial_board_box=self._val(board["SerialBoardBox"]),
            serial_board_comm=self._val(board["SerialBoardComm"]),
            serial_duco_box=self._val(board["SerialDucoBox"]),
            serial_duco_comm=self._val(board["SerialDucoComm"]),
            time=self._val(board["Time"]),
        )

    async def async_get_lan_info(self) -> LanInfo:
        """Get network / LAN information.

        Returns:
            Network info with IP, MAC, WiFi signal, etc.

        """
        data = await self._request("GET", "/info", params={"module": "General", "submodule": "Lan"})
        lan = data["General"]["Lan"]
        return LanInfo(
            mode=self._val(lan["Mode"]),
            ip=self._val(lan["Ip"]),
            net_mask=self._val(lan["NetMask"]),
            default_gateway=self._val(lan["DefaultGateway"]),
            dns=self._val(lan["Dns"]),
            mac=self._val(lan["Mac"]),
            host_name=self._val(lan["HostName"]),
            rssi_wifi=self._val(lan["RssiWifi"]) if "RssiWifi" in lan else None,
        )

    async def async_get_diagnostics(self) -> list[DiagComponent]:
        """Get diagnostic subsystem statuses.

        Returns:
            List of diagnostic component statuses.

        """
        data = await self._request("GET", "/info", params={"module": "Diag"})
        return [
            DiagComponent(
                component=item["Component"],
                status=DiagStatus(item["Status"]),
            )
            for item in data["Diag"]["SubSystems"]
        ]

    async def async_get_write_req_remaining(self) -> int:
        """Get the number of remaining API write requests.

        Returns:
            Number of remaining write requests.

        """
        data = await self._request(
            "GET",
            "/info",
            params={"module": "General", "submodule": "PublicApi"},
        )
        return int(self._val(data["General"]["PublicApi"]["WriteReqCntRemain"]))

    # -------------------------------------------------------------------------
    # Nodes
    # -------------------------------------------------------------------------

    async def async_get_nodes(self) -> list[Node]:
        """Get all nodes with their details.

        Returns:
            List of nodes with general info, ventilation state, and sensor data.

        """
        data = await self._request("GET", "/info/nodes")
        return [self._parse_node(node_data) for node_data in data["Nodes"]]

    async def async_get_node(self, node_id: int) -> Node:
        """Get a specific node by ID.

        Args:
            node_id: The node ID.

        Returns:
            Node with general info, ventilation state, and sensor data.

        """
        data = await self._request("GET", f"/info/nodes/{node_id}")
        return self._parse_node(data)

    def _parse_node(self, data: dict[str, Any]) -> Node:
        """Parse a node from the API response."""
        general_data = data["General"]
        raw_type = self._val(general_data["Type"])
        try:
            node_type = NodeType(raw_type)
        except ValueError:
            node_type = NodeType.UNKNOWN
        general = NodeGeneralInfo(
            node_type=node_type,
            sub_type=self._val(general_data["SubType"]),
            network_type=NetworkType(self._val(general_data["NetworkType"])),
            parent=self._val(general_data["Parent"]),
            asso=self._val(general_data["Asso"]),
            name=self._val(general_data["Name"]),
            identify=self._val(general_data["Identify"]),
        )

        ventilation = None
        if "Ventilation" in data:
            vent_data = data["Ventilation"]
            ventilation = NodeVentilationInfo(
                state=self._val(vent_data["State"]),
                time_state_remain=self._val(vent_data["TimeStateRemain"]),
                time_state_end=self._val(vent_data["TimeStateEnd"]),
                mode=VentilationMode(self._val(vent_data["Mode"])),
                flow_lvl_tgt=self._val(vent_data["FlowLvlTgt"]) if "FlowLvlTgt" in vent_data else None,
            )

        sensor = None
        if "Sensor" in data:
            sensor_data = data["Sensor"]
            sensor = NodeSensorInfo(
                co2=self._val(sensor_data["Co2"]) if "Co2" in sensor_data else None,
                iaq_co2=self._val(sensor_data["IaqCo2"]) if "IaqCo2" in sensor_data else None,
                rh=self._val(sensor_data["Rh"]) if "Rh" in sensor_data else None,
                iaq_rh=self._val(sensor_data["IaqRh"]) if "IaqRh" in sensor_data else None,
                temp=self._val(sensor_data["Temp"]) if "Temp" in sensor_data else None,
            )

        return Node(
            node_id=data["Node"],
            general=general,
            ventilation=ventilation,
            sensor=sensor,
        )

    async def async_get_node_ids(self) -> list[int]:
        """Get a list of all node IDs.

        Returns:
            List of node IDs.

        """
        data = await self._request("GET", "/nodes")
        return [item["Node"] for item in data]

    # -------------------------------------------------------------------------
    # Zones
    # -------------------------------------------------------------------------

    async def async_get_zones(self) -> list[Zone]:
        """Get all zones with their groups.

        Returns:
            List of zones.

        """
        data = await self._request("GET", "/info/zones")
        return [self._parse_zone(zone_data) for zone_data in data["Zones"]]

    async def async_get_zone(self, zone_id: int) -> Zone:
        """Get a specific zone by ID.

        Args:
            zone_id: The zone ID.

        Returns:
            Zone with groups.

        """
        data = await self._request("GET", f"/info/zones/{zone_id}")
        return self._parse_zone(data)

    def _parse_zone(self, data: dict[str, Any]) -> Zone:
        """Parse a zone from the API response."""
        groups = []
        for group_data in data.get("Groups", []):
            nodes = group_data.get("DeviceGroupConfig", {}).get("General", {}).get("Nodes", [])
            groups.append(
                ZoneGroup(
                    group_id=group_data["Group"],
                    nodes=list(nodes),
                ),
            )

        name = self._val(data.get("DeviceGroupConfig", {}).get("General", {}).get("Name", {"Val": ""}))

        return Zone(
            zone_id=data["Zone"],
            name=name,
            groups=groups,
        )

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------

    async def async_get_actions(self) -> list[ActionInfo]:
        """Return all actions available on the box.

        Returns:
            List of :class:`ActionInfo` objects.

        """
        data = await self._request("GET", "/action")
        return [self._parse_action(item) for item in data]

    async def async_get_node_actions(self) -> list[NodeActions]:
        """Return available actions for all nodes.

        Returns:
            List of :class:`NodeActions`, one per node.

        """
        data = await self._request("GET", "/action/nodes")
        return [
            NodeActions(
                node_id=node_data["Node"],
                actions=[self._parse_action(a) for a in node_data.get("Actions", [])],
            )
            for node_data in data["Nodes"]
        ]

    async def async_get_node_action_list(self, node_id: int) -> NodeActions:
        """Return available actions for a single node.

        Args:
            node_id: The node ID.

        Returns:
            :class:`NodeActions` for the requested node.

        """
        data = await self._request("GET", f"/action/nodes/{node_id}")
        return NodeActions(
            node_id=data["Node"],
            actions=[self._parse_action(a) for a in data.get("Actions", [])],
        )

    @staticmethod
    def _parse_action(data: dict[str, Any]) -> ActionInfo:
        """Parse an action descriptor from the API response."""
        return ActionInfo(
            action=data["Action"],
            val_type=data["ValType"],
            enum_values=list(data.get("Enum", [])),
        )

    async def async_set_ventilation_state(self, node_id: int, state: str) -> None:
        """Set the ventilation state for a node.

        Args:
            node_id: The node ID.
            state: Ventilation state (e.g. ``"AUTO"``, ``"MAN1"``, ``"MAN3"``).
                   See :class:`~duco.models.VentilationState` for all values.

        Raises:
            DucoRateLimitError: If the write rate limit is exceeded.

        """
        await self._request(
            "POST",
            f"/action/nodes/{node_id}",
            json={"Action": "SetVentilationState", "Val": state},
        )

    async def async_set_identify(self, node_id: int, *, enabled: bool) -> None:
        """Enable or disable identification mode on a node.

        Args:
            node_id: The node ID.
            enabled: Whether to enable identification.

        """
        await self._request(
            "POST",
            f"/action/nodes/{node_id}",
            json={"Action": "SetIdentify", "Val": enabled},
        )

    async def async_set_identify_all(self, *, enabled: bool) -> None:
        """Enable or disable identification mode on all devices.

        Args:
            enabled: Whether to enable identification.

        """
        await self._request(
            "POST",
            "/action",
            json={"Action": "SetIdentifyAll", "Val": enabled},
        )

    async def async_reconnect_wifi(self) -> None:
        """Reconnect WiFi."""
        await self._request(
            "POST",
            "/action",
            json={"Action": "ReconnectWifi"},
        )

    async def async_scan_wifi(self) -> None:
        """Start a WiFi scan."""
        await self._request(
            "POST",
            "/action",
            json={"Action": "ScanWifi"},
        )

    async def async_set_time(self, timestamp: int) -> None:
        """Set the system time on the box.

        Args:
            timestamp: Unix timestamp (seconds since epoch).

        Raises:
            DucoRateLimitError: If the write rate limit is exceeded.

        """
        await self._request(
            "POST",
            "/action",
            json={"Action": "SetTime", "Val": timestamp},
        )

    async def async_set_wifi_ap_mode(self, *, enabled: bool) -> None:
        """Enable or disable WiFi access point mode.

        Args:
            enabled: Whether to enable access point mode.

        Raises:
            DucoRateLimitError: If the write rate limit is exceeded.

        """
        await self._request(
            "POST",
            "/action",
            json={"Action": "SetWifiApMode", "Val": enabled},
        )

    # -------------------------------------------------------------------------
    # Config
    # -------------------------------------------------------------------------

    async def async_get_system_config(self) -> SystemConfig:
        """Get the system configuration.

        Returns:
            System configuration including time, network, and reboot settings.

        """
        data = await self._request("GET", "/config", params={"module": "General"})
        general = data["General"]
        return SystemConfig(
            time_zone=self._val(general["Time"]["TimeZone"]),
            dst=self._val(general["Time"]["Dst"]),
            modbus_addr=self._val(general["Modbus"]["Addr"]),
            modbus_offset=self._val(general["Modbus"]["Offset"]),
            lan_mode=self._val(general["Lan"]["Mode"]),
            lan_dhcp=self._val(general["Lan"]["Dhcp"]),
            lan_static_ip=self._val(general["Lan"]["StaticIp"]),
            lan_static_net_mask=self._val(general["Lan"]["StaticNetMask"]),
            lan_static_default_gateway=self._val(general["Lan"]["StaticDefaultGateway"]),
            lan_static_dns=self._val(general["Lan"]["StaticDns"]),
            lan_wifi_client_ssid=self._val(general["Lan"]["WifiClientSsid"]),
            lan_wifi_client_key=self._val(general["Lan"]["WifiClientKey"]),
            auto_reboot_comm_period=self._val(general["AutoRebootComm"]["Period"]),
            auto_reboot_comm_time=self._val(general["AutoRebootComm"]["Time"]),
        )

    async def async_set_system_config(
        self,
        *,
        time_zone: int | None = None,
        dst: int | None = None,
        modbus_addr: int | None = None,
        modbus_offset: int | None = None,
        lan_dhcp: int | None = None,
        lan_static_ip: str | None = None,
        lan_static_net_mask: str | None = None,
        lan_static_default_gateway: str | None = None,
        lan_static_dns: str | None = None,
        lan_wifi_client_ssid: str | None = None,
        lan_wifi_client_key: str | None = None,
        auto_reboot_comm_period: int | None = None,
        auto_reboot_comm_time: int | None = None,
    ) -> None:
        """Update system configuration (partial update).

        Only the provided keyword arguments are sent. Omitted arguments are not
        included in the request, leaving those settings unchanged on the box.

        Args:
            time_zone: UTC offset in hours (``-11`` to ``12``).
            dst: Daylight saving time (``0`` = off, ``1`` = on).
            modbus_addr: Modbus device address (``1`` to ``254``).
            modbus_offset: Modbus address offset (``0`` or ``1``).
            lan_dhcp: DHCP enabled (``0`` = static, ``1`` = DHCP).
            lan_static_ip: Static IP address.
            lan_static_net_mask: Static subnet mask.
            lan_static_default_gateway: Static default gateway.
            lan_static_dns: Static DNS server.
            lan_wifi_client_ssid: WiFi SSID to connect to.
            lan_wifi_client_key: WiFi password.
            auto_reboot_comm_period: Auto-reboot period in days (``0`` = disabled).
            auto_reboot_comm_time: Auto-reboot time in minutes since midnight.

        """
        body: dict[str, Any] = {"General": {}}
        if time_zone is not None:
            body["General"].setdefault("Time", {})["TimeZone"] = time_zone
        if dst is not None:
            body["General"].setdefault("Time", {})["Dst"] = dst
        if modbus_addr is not None:
            body["General"].setdefault("Modbus", {})["Addr"] = modbus_addr
        if modbus_offset is not None:
            body["General"].setdefault("Modbus", {})["Offset"] = modbus_offset
        if lan_dhcp is not None:
            body["General"].setdefault("Lan", {})["Dhcp"] = lan_dhcp
        if lan_static_ip is not None:
            body["General"].setdefault("Lan", {})["StaticIp"] = lan_static_ip
        if lan_static_net_mask is not None:
            body["General"].setdefault("Lan", {})["StaticNetMask"] = lan_static_net_mask
        if lan_static_default_gateway is not None:
            body["General"].setdefault("Lan", {})["StaticDefaultGateway"] = lan_static_default_gateway
        if lan_static_dns is not None:
            body["General"].setdefault("Lan", {})["StaticDns"] = lan_static_dns
        if lan_wifi_client_ssid is not None:
            body["General"].setdefault("Lan", {})["WifiClientSsid"] = lan_wifi_client_ssid
        if lan_wifi_client_key is not None:
            body["General"].setdefault("Lan", {})["WifiClientKey"] = lan_wifi_client_key
        if auto_reboot_comm_period is not None:
            body["General"].setdefault("AutoRebootComm", {})["Period"] = auto_reboot_comm_period
        if auto_reboot_comm_time is not None:
            body["General"].setdefault("AutoRebootComm", {})["Time"] = auto_reboot_comm_time
        await self._request("PATCH", "/config", json=body)

    async def async_get_zone_configs(self) -> list[Zone]:
        """Return configuration for all zones.

        Returns:
            List of :class:`Zone` objects, one per zone.

        """
        data = await self._request("GET", "/config/zones")
        return [self._parse_zone(zone_data) for zone_data in data["Zones"]]

    async def async_get_zone_config(self, zone_id: int) -> Zone:
        """Return configuration for a single zone.

        Args:
            zone_id: The zone ID.

        Returns:
            :class:`Zone` for the requested zone.

        """
        data = await self._request("GET", f"/config/zones/{zone_id}")
        return self._parse_zone(data)

    async def async_set_zone_name(self, zone_id: int, name: str) -> None:
        """Set the name of a zone.

        Args:
            zone_id: The zone ID.
            name: The new zone name.

        """
        await self._request(
            "PATCH",
            f"/config/zones/{zone_id}",
            json={"DeviceGroupConfig": {"General": {"Name": name}}},
        )

    async def async_get_zone_group_config(self, zone_id: int, group_id: int) -> ZoneGroup:
        """Return configuration for a single group within a zone.

        Args:
            zone_id: The zone ID.
            group_id: The group ID.

        Returns:
            :class:`ZoneGroup` for the requested group.

        """
        data = await self._request("GET", f"/config/zones/{zone_id}/groups/{group_id}")
        nodes = data.get("DeviceGroupConfig", {}).get("General", {}).get("Nodes", [])
        return ZoneGroup(group_id=data["Group"], nodes=list(nodes))

    async def async_set_zone_group_nodes(self, zone_id: int, group_id: int, node_ids: list[int]) -> None:
        """Set the nodes assigned to a group.

        Args:
            zone_id: The zone ID.
            group_id: The group ID.
            node_ids: List of node IDs to assign to the group.

        """
        await self._request(
            "PATCH",
            f"/config/zones/{zone_id}/groups/{group_id}",
            json={"DeviceGroupConfig": {"General": {"Nodes": node_ids}}},
        )

    async def async_get_node_configs(self) -> list[NodeConfig]:
        """Return configuration for all nodes.

        Returns:
            List of :class:`NodeConfig` objects, one per node.

        """
        data = await self._request("GET", "/config/nodes")
        return [NodeConfig(node_id=item["Node"], name=self._val(item["Name"])) for item in data["Nodes"]]

    async def async_get_node_config(self, node_id: int) -> NodeConfig:
        """Return configuration for a single node.

        Args:
            node_id: The node ID.

        Returns:
            :class:`NodeConfig` for the requested node.

        """
        data = await self._request("GET", f"/config/nodes/{node_id}")
        return NodeConfig(node_id=data["Node"], name=self._val(data["Name"]))

    async def async_set_node_name(self, node_id: int, name: str) -> None:
        """Set the name of a node.

        Args:
            node_id: The node ID.
            name: The new node name.

        """
        await self._request(
            "PATCH",
            f"/config/nodes/{node_id}",
            json={"Name": name},
        )
