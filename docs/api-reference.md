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
