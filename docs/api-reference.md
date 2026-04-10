# API Reference

All methods are `async` and belong to `DucoClient`.

```python
from duco import DucoClient
import aiohttp

async with aiohttp.ClientSession() as session:
    client = DucoClient(session=session, host="192.168.1.100")
```

---

## API info

### `async_get_api_info()`

Get the API version of the Connectivity Board.

```python
info = await client.async_get_api_info()
```

**Returns:** `ApiInfo`

| Field | Type | Description |
|---|---|---|
| `api_version` | `str` | Public API version (e.g. `"2.5"`) |

---

## Box info

### `async_get_board_info()`

Get board identification and serial numbers.

```python
board = await client.async_get_board_info()
print(board.box_name, board.serial_duco_comm)
```

**Returns:** `BoardInfo`

| Field | Type | Description |
|---|---|---|
| `box_name` | `str` | Box type (e.g. `"SILENT_CONNECT"`) |
| `box_sub_type_name` | `str` | Subtype (e.g. `"Eu"`) |
| `serial_board_box` | `str` | Box board serial number |
| `serial_board_comm` | `str` | Communication board serial number |
| `serial_duco_box` | `str` | Duco box serial number |
| `serial_duco_comm` | `str` | Duco communication module serial number |
| `time` | `int` | Current Unix timestamp on the box |

---

### `async_get_lan_info()`

Get network / LAN information.

```python
lan = await client.async_get_lan_info()
print(lan.ip, lan.rssi_wifi)
```

**Returns:** `LanInfo`

| Field | Type | Description |
|---|---|---|
| `mode` | `str` | Network mode (e.g. `"WIFI_CLIENT"`) |
| `ip` | `str` | IP address |
| `net_mask` | `str` | Subnet mask |
| `default_gateway` | `str` | Default gateway |
| `dns` | `str` | DNS server |
| `mac` | `str` | MAC address |
| `host_name` | `str` | Hostname on the network |
| `rssi_wifi` | `int` | WiFi signal strength in dBm |

---

### `async_get_diagnostics()`

Get diagnostic status of all subsystems.

```python
diags = await client.async_get_diagnostics()
for d in diags:
    print(d.component, d.status)
```

**Returns:** `list[DiagComponent]`

| Field | Type | Description |
|---|---|---|
| `component` | `str` | Component name (e.g. `"Ventilation"`) |
| `status` | `DiagStatus` | Status (`DiagStatus.OK`, `DiagStatus.ERROR`, `DiagStatus.DISABLE`) |

---

### `async_get_write_req_remaining()`

Get the number of remaining API write requests (rate limit).

```python
remaining = await client.async_get_write_req_remaining()
print(f"{remaining} write requests remaining")
```

**Returns:** `int`

---

## Nodes

### `async_get_nodes()`

Get all nodes with their details.

```python
nodes = await client.async_get_nodes()
```

**Returns:** `list[Node]`

---

### `async_get_node(node_id)`

Get a specific node by ID.

```python
node = await client.async_get_node(1)
```

**Returns:** `Node`

---

### `async_get_node_ids()`

Get the list of all node IDs.

```python
ids = await client.async_get_node_ids()
```

**Returns:** `list[int]`

---

### `Node` model

| Field | Type | Description |
|---|---|---|
| `node_id` | `int` | Unique node identifier |
| `general` | `NodeGeneralInfo` | General node information |
| `ventilation` | `NodeVentilationInfo \| None` | Ventilation state, or `None` |
| `sensor` | `NodeSensorInfo \| None` | Sensor data, or `None` |

### `NodeGeneralInfo`

| Field | Type | Description |
|---|---|---|
| `node_type` | `NodeType` | Node type (`NodeType.BOX`, `NodeType.UCCO2`, `NodeType.BSRH`) |
| `sub_type` | `int` | Node subtype number |
| `network_type` | `NetworkType` | Connection type (`NetworkType.VIRT` or `NetworkType.RF`) |
| `parent` | `int` | Parent node ID (0 = no parent) |
| `asso` | `int` | Associated node ID (0 = no association) |
| `name` | `str` | User-assigned name |
| `identify` | `int` | Identification mode (0 = off, 1 = on) |

### `NodeVentilationInfo`

Present on nodes that control ventilation (e.g. `BOX`).

| Field | Type | Description |
|---|---|---|
| `state` | `VentilationState` | Current ventilation state (see [Ventilation states](#ventilation-states)) |
| `time_state_remain` | `int` | Remaining time in current state (seconds) |
| `time_state_end` | `int` | End time of current state (Unix timestamp; 0 = permanent) |
| `mode` | `VentilationMode` | Ventilation mode (`VentilationMode.MANU`, `VentilationMode.AUTO`, `VentilationMode.FOLLOW`) |
| `flow_lvl_tgt` | `int \| None` | Target flow level (BOX nodes only) |

### `NodeSensorInfo`

Present on sensor nodes (e.g. `UCCO2`, `BSRH`).

| Field | Type | Description |
|---|---|---|
| `co2` | `int \| None` | CO2 concentration in ppm (CO2 sensor nodes only) |
| `iaq_co2` | `int \| None` | Indoor Air Quality index based on CO2 (0–100; CO2 nodes only) |
| `rh` | `float \| None` | Relative humidity in % (humidity sensor nodes only) |
| `iaq_rh` | `int \| None` | Indoor Air Quality index based on humidity (0–100; humidity nodes only) |

---

## Zones

### `async_get_zones()`

Get all zones with their groups (from `/info/zones`).

```python
zones = await client.async_get_zones()
```

**Returns:** `list[Zone]`

---

### `async_get_zone(zone_id)`

Get a specific zone by ID (from `/info/zones/{zone}`).

```python
zone = await client.async_get_zone(1)
```

**Returns:** `Zone`

---

### `Zone` model

| Field | Type | Description |
|---|---|---|
| `zone_id` | `int` | Zone identifier |
| `name` | `str` | Zone name |
| `groups` | `list[ZoneGroup]` | Groups within this zone |

### `ZoneGroup`

| Field | Type | Description |
|---|---|---|
| `group_id` | `int` | Group identifier |
| `nodes` | `list[int]` | Node IDs in this group |

---

## System config

### `async_get_system_config()`

Read the full system configuration (time, Modbus, network, auto-reboot).

```python
cfg = await client.async_get_system_config()
print(cfg.lan_wifi_client_ssid, cfg.auto_reboot_comm_period)
```

**Returns:** `SystemConfig`

| Field | Type | Description |
|---|---|---|
| `time_zone` | `int` | UTC offset in hours (`-11` to `12`) |
| `dst` | `int` | Daylight saving time (`0` = off, `1` = on) |
| `modbus_addr` | `int` | Modbus device address (`1`–`254`) |
| `modbus_offset` | `int` | Modbus address offset (`0` or `1`) |
| `lan_mode` | `int` | LAN mode (read-only on most boxes) |
| `lan_dhcp` | `int` | DHCP enabled (`0` = static, `1` = DHCP) |
| `lan_static_ip` | `str` | Static IP address |
| `lan_static_net_mask` | `str` | Static subnet mask |
| `lan_static_default_gateway` | `str` | Static default gateway |
| `lan_static_dns` | `str` | Static DNS server |
| `lan_wifi_client_ssid` | `str` | WiFi SSID to connect to |
| `lan_wifi_client_key` | `str` | WiFi password |
| `auto_reboot_comm_period` | `int` | Auto-reboot period in days (`0` = disabled) |
| `auto_reboot_comm_time` | `int` | Auto-reboot time of day in minutes since midnight |

---

### `async_set_system_config(**kwargs)`

Update system configuration — only the supplied keyword arguments are sent; all others remain unchanged.

```python
await client.async_set_system_config(time_zone=1, dst=1)
await client.async_set_system_config(lan_wifi_client_ssid="MyNetwork", lan_wifi_client_key="secret")
await client.async_set_system_config(auto_reboot_comm_period=7, auto_reboot_comm_time=120)
```

Accepts the same keyword arguments as the `SystemConfig` fields, all optional.

---

## Node config

### `async_get_node_configs()`

Read name configuration for all nodes.

```python
configs = await client.async_get_node_configs()
for c in configs:
    print(c.node_id, c.name)
```

**Returns:** `list[NodeConfig]`

---

### `async_get_node_config(node_id)`

Read name configuration for a single node.

```python
cfg = await client.async_get_node_config(2)
print(cfg.name)
```

**Returns:** `NodeConfig`

---

### `async_set_node_name(node_id, name)`

Set the user-assigned name of a node.

```python
await client.async_set_node_name(2, "Living room CO2")
```

---

### `NodeConfig` model

| Field | Type | Description |
|---|---|---|
| `node_id` | `int` | Node identifier |
| `name` | `str` | User-assigned name (empty string if not set) |

---

## Zone config

### `async_get_zone_configs()`

Read configuration for all zones.

```python
configs = await client.async_get_zone_configs()
for c in configs:
    print(c.zone_id, c.name)
```

**Returns:** `list[Zone]`

---

### `async_get_zone_config(zone_id)`

Read configuration for a single zone.

```python
cfg = await client.async_get_zone_config(1)
```

**Returns:** `Zone`

---

### `async_set_zone_name(zone_id, name)`

Set the user-assigned name of a zone.

```python
await client.async_set_zone_name(1, "Ground floor")
```

---

### `async_get_zone_group_config(zone_id, group_id)`

Read the node assignment for a specific group within a zone.

```python
group = await client.async_get_zone_group_config(1, 1)
print(group.nodes)
```

**Returns:** `ZoneGroup`

---

### `async_set_zone_group_nodes(zone_id, group_id, node_ids)`

Assign a list of nodes to a group.

```python
await client.async_set_zone_group_nodes(1, 1, [2, 113])
```

---

## Action listing

### `async_get_actions()`

List all system-level actions the box supports.

```python
actions = await client.async_get_actions()
for a in actions:
    print(a.action, a.val_type)
```

**Returns:** `list[ActionInfo]`

---

### `async_get_node_actions()`

List available actions for all nodes.

```python
node_actions = await client.async_get_node_actions()
for na in node_actions:
    print(f"Node {na.node_id}: {[a.action for a in na.actions]}")
```

**Returns:** `list[NodeActions]`

---

### `async_get_node_action_list(node_id)`

List available actions for a single node.

```python
na = await client.async_get_node_action_list(1)
```

**Returns:** `NodeActions`

---

### `ActionInfo` model

| Field | Type | Description |
|---|---|---|
| `action` | `str` | Action name (e.g. `"SetVentilationState"`, `"SetTime"`) |
| `val_type` | `str` | Value type: `"Integer"`, `"Boolean"`, `"Enum"`, or `"None"` |
| `enum_values` | `list[str]` | Allowed values when `val_type` is `"Enum"`; empty list otherwise |

### `NodeActions` model

| Field | Type | Description |
|---|---|---|
| `node_id` | `int` | Node identifier |
| `actions` | `list[ActionInfo]` | Actions available on this node |

---

## Actions

### `async_set_ventilation_state(node_id, state)`

Set the ventilation state for a node.

```python
await client.async_set_ventilation_state(1, "MAN2")
await client.async_set_ventilation_state(1, "AUTO")
```

See [Ventilation states](#ventilation-states) for valid values. Use `VentilationState` for type-safe values:

```python
from duco import VentilationState
await client.async_set_ventilation_state(1, VentilationState.MAN2)
```

---

### `async_set_identify(node_id, *, enabled)`

Enable or disable identification mode on a node (the device will flash its LED).

```python
await client.async_set_identify(2, enabled=True)
await client.async_set_identify(2, enabled=False)
```

---

### `async_set_identify_all(*, enabled)`

Enable or disable identification mode on all devices simultaneously.

```python
await client.async_set_identify_all(enabled=True)
```

---

### `async_reconnect_wifi()`

Trigger a WiFi reconnect on the Connectivity Board.

```python
await client.async_reconnect_wifi()
```

---

### `async_scan_wifi()`

Start a WiFi network scan.

```python
await client.async_scan_wifi()
```

---

### `async_set_time(timestamp)`

Set the system time on the box.

```python
import time
await client.async_set_time(int(time.time()))
```

---

### `async_set_wifi_ap_mode(*, enabled)`

Enable or disable WiFi access point mode on the Connectivity Board.

```python
await client.async_set_wifi_ap_mode(enabled=True)
await client.async_set_wifi_ap_mode(enabled=False)
```

---

## Ventilation states

| State | Description |
|---|---|
| `AUTO` | Fully automatic |
| `AUT1` / `AUT2` / `AUT3` | Automatic mode variants |
| `MAN1` / `MAN2` / `MAN3` | Manual low / medium / high |
| `CNT1` / `CNT2` / `CNT3` | Continuous low / medium / high |
| `MAN1x2` … `MAN3x3` | Manual extended modes |
| `EMPT` | Away / minimal ventilation |

All values are available as `VentilationState` enum members:

```python
from duco import VentilationState

print(VentilationState.MAN2)   # "MAN2"
print(VentilationState.AUTO)   # "AUTO"
```

---

## Enums

All enums are `StrEnum` — they compare equal to their string values and can be used interchangeably with raw strings.

### `VentilationState`

Full list of ventilation states, see [Ventilation states](#ventilation-states) above.

### `VentilationMode`

| Value | Description |
|---|---|
| `VentilationMode.AUTO` | Automatic (sensor-driven) |
| `VentilationMode.MANU` | Manual (user-controlled) |
| `VentilationMode.FOLLOW` | Follows parent node (`"-"`) |

### `NodeType`

| Value | Description |
|---|---|
| `NodeType.BOX` | Main ventilation unit |
| `NodeType.UCCO2` | CO2 user control sensor |
| `NodeType.BSRH` | Relative humidity sensor |

### `NetworkType`

| Value | Description |
|---|---|
| `NetworkType.VIRT` | Virtual / internal to the box |
| `NetworkType.RF` | Wireless (radio frequency) |

### `DiagStatus`

| Value | Description |
|---|---|
| `DiagStatus.OK` | System operating normally |
| `DiagStatus.ERROR` | Fault detected |
| `DiagStatus.DISABLE` | Subsystem disabled |


### `async_get_api_info()`

Get the API version of the Connectivity Board.

```python
info = await client.async_get_api_info()
```

**Returns:** `ApiInfo`

| Field | Type | Description |
|---|---|---|
| `api_version` | `str` | Public API version (e.g. `"2.5"`) |

---

## Box info

### `async_get_board_info()`

Get board identification and serial numbers.

```python
board = await client.async_get_board_info()
print(board.box_name, board.serial_duco_comm)
```

**Returns:** `BoardInfo`

| Field | Type | Description |
|---|---|---|
| `box_name` | `str` | Box type (e.g. `"SILENT_CONNECT"`) |
| `box_sub_type_name` | `str` | Subtype (e.g. `"Eu"`) |
| `serial_board_box` | `str` | Box board serial number |
| `serial_board_comm` | `str` | Communication board serial number |
| `serial_duco_box` | `str` | Duco box serial number |
| `serial_duco_comm` | `str` | Duco communication module serial number |
| `time` | `int` | Current Unix timestamp on the box |

---

### `async_get_lan_info()`

Get network / LAN information.

```python
lan = await client.async_get_lan_info()
print(lan.ip, lan.rssi_wifi)
```

**Returns:** `LanInfo`

| Field | Type | Description |
|---|---|---|
| `mode` | `str` | Network mode (e.g. `"WIFI_CLIENT"`) |
| `ip` | `str` | IP address |
| `net_mask` | `str` | Subnet mask |
| `default_gateway` | `str` | Default gateway |
| `dns` | `str` | DNS server |
| `mac` | `str` | MAC address |
| `host_name` | `str` | Hostname on the network |
| `rssi_wifi` | `int` | WiFi signal strength in dBm |

---

### `async_get_diagnostics()`

Get diagnostic status of all subsystems.

```python
diags = await client.async_get_diagnostics()
for d in diags:
    print(d.component, d.status)
```

**Returns:** `list[DiagComponent]`

| Field | Type | Description |
|---|---|---|
| `component` | `str` | Component name (e.g. `"Ventilation"`) |
| `status` | `str` | Status string (e.g. `"Ok"`) |

---

### `async_get_write_req_remaining()`

Get the number of remaining API write requests (rate limit).

```python
remaining = await client.async_get_write_req_remaining()
print(f"{remaining} write requests remaining")
```

**Returns:** `int`

---

## Nodes

### `async_get_nodes()`

Get all nodes with their details.

```python
nodes = await client.async_get_nodes()
```

**Returns:** `list[Node]`

---

### `async_get_node(node_id)`

Get a specific node by ID.

```python
node = await client.async_get_node(1)
```

**Returns:** `Node`

---

### `async_get_node_ids()`

Get the list of all node IDs.

```python
ids = await client.async_get_node_ids()
```

**Returns:** `list[int]`

---

### `Node` model

| Field | Type | Description |
|---|---|---|
| `node_id` | `int` | Unique node identifier |
| `general` | `NodeGeneralInfo` | General node information |
| `ventilation` | `NodeVentilationInfo \| None` | Ventilation state, or `None` |
| `sensor` | `NodeSensorInfo \| None` | Sensor data, or `None` |

### `NodeGeneralInfo`

| Field | Type | Description |
|---|---|---|
| `node_type` | `str` | Node type (`"BOX"`, `"UCCO2"`, `"BSRH"`) |
| `sub_type` | `int` | Node subtype number |
| `network_type` | `str` | Connection type (`"VIRT"` or `"RF"`) |
| `parent` | `int` | Parent node ID (0 = no parent) |
| `asso` | `int` | Associated node ID (0 = no association) |
| `name` | `str` | User-assigned name |
| `identify` | `int` | Identification mode (0 = off, 1 = on) |

### `NodeVentilationInfo`

Present on nodes that control ventilation (e.g. `BOX`).

| Field | Type | Description |
|---|---|---|
| `state` | `str` | Current ventilation state (see [Ventilation states](#ventilation-states)) |
| `time_state_remain` | `int` | Remaining time in current state (seconds) |
| `time_state_end` | `int` | End time of current state (Unix timestamp; 0 = permanent) |
| `mode` | `str` | Ventilation mode (`"MANU"`, `"AUTO"`, `"-"`) |
| `flow_lvl_tgt` | `int \| None` | Target flow level (BOX nodes only) |

### `NodeSensorInfo`

Present on sensor nodes (e.g. `UCCO2`).

| Field | Type | Description |
|---|---|---|
| `co2` | `int \| None` | CO2 concentration in ppm |
| `iaq_co2` | `int \| None` | Indoor Air Quality index based on CO2 (0–100) |

---

## Zones

### `async_get_zones()`

Get all zones with their groups.

```python
zones = await client.async_get_zones()
```

**Returns:** `list[Zone]`

---

### `async_get_zone(zone_id)`

Get a specific zone by ID.

```python
zone = await client.async_get_zone(1)
```

**Returns:** `Zone`

---

### `Zone` model

| Field | Type | Description |
|---|---|---|
| `zone_id` | `int` | Zone identifier |
| `name` | `str` | Zone name |
| `groups` | `list[ZoneGroup]` | Groups within this zone |

### `ZoneGroup`

| Field | Type | Description |
|---|---|---|
| `group_id` | `int` | Group identifier |
| `nodes` | `list[int]` | Node IDs in this group |

---

## Actions

### `async_set_ventilation_state(node_id, state)`

Set the ventilation state for a node.

```python
await client.async_set_ventilation_state(1, "MAN2")
await client.async_set_ventilation_state(1, "AUTO")
```

See [Ventilation states](#ventilation-states) for valid values. Use `VentilationState` for type-safe values:

```python
from duco import VentilationState
await client.async_set_ventilation_state(1, VentilationState.MAN2)
```

---

### `async_set_identify(node_id, *, enabled)`

Enable or disable identification mode on a node (the device will flash its LED).

```python
await client.async_set_identify(2, enabled=True)
await client.async_set_identify(2, enabled=False)
```

---

### `async_set_identify_all(*, enabled)`

Enable or disable identification mode on all devices simultaneously.

```python
await client.async_set_identify_all(enabled=True)
```

---

### `async_reconnect_wifi()`

Trigger a WiFi reconnect on the Connectivity Board.

```python
await client.async_reconnect_wifi()
```

---

### `async_scan_wifi()`

Start a WiFi network scan.

```python
await client.async_scan_wifi()
```

---

## Config

### `async_set_node_name(node_id, name)`

Set the user-assigned name of a node.

```python
await client.async_set_node_name(2, "Living room CO2")
```

---

## Ventilation states

| State | Description |
|---|---|
| `AUTO` | Fully automatic |
| `AUT1` / `AUT2` / `AUT3` | Automatic mode variants |
| `MAN1` / `MAN2` / `MAN3` | Manual low / medium / high |
| `CNT1` / `CNT2` / `CNT3` | Continuous low / medium / high |
| `MAN1x2` … `MAN3x3` | Manual extended modes |
| `EMPT` | Away / minimal ventilation |

All values are available as `VentilationState` enum members:

```python
from duco import VentilationState

print(VentilationState.MAN2)   # "MAN2"
print(VentilationState.AUTO)   # "AUTO"
```
