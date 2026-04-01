# python-duco

Async Python client for the Duco ventilation box REST API.

## Installation

```bash
pip install python-duco
```

## Quick start

```python
import asyncio
import aiohttp
from duco import DucoClient

async def main():
    async with aiohttp.ClientSession() as session:
        client = DucoClient(session=session, host="192.168.1.100")

        # Get box info
        board = await client.async_get_board_info()
        print(f"Box: {board.box_name} ({board.box_sub_type_name})")

        # Get all nodes
        nodes = await client.async_get_nodes()
        for node in nodes:
            print(f"Node {node.node_id}: {node.general.node_type}")
            if node.sensor:
                print(f"  CO2: {node.sensor.co2} ppm")

        # Set ventilation to manual level 2
        await client.async_set_ventilation_state(1, "MAN2")

        # Set ventilation back to auto
        await client.async_set_ventilation_state(1, "AUTO")

asyncio.run(main())
```

## API

### `DucoClient(session, host, scheme="http")`

| Method | Description |
|--------|-------------|
| `async_get_api_info()` | Get API version |
| `async_get_board_info()` | Get box board info (serial numbers, type) |
| `async_get_lan_info()` | Get network info (IP, MAC, WiFi signal) |
| `async_get_diagnostics()` | Get diagnostic subsystem statuses |
| `async_get_write_req_remaining()` | Get remaining write request count |
| `async_get_nodes()` | Get all nodes with details |
| `async_get_node(node_id)` | Get a specific node |
| `async_get_node_ids()` | Get list of node IDs |
| `async_get_zones()` | Get all zones with groups |
| `async_get_zone(zone_id)` | Get a specific zone |
| `async_set_ventilation_state(node_id, state)` | Set ventilation state |
| `async_set_identify(node_id, enabled=True)` | Toggle identify mode |
| `async_set_identify_all(enabled=True)` | Toggle identify on all devices |
| `async_reconnect_wifi()` | Reconnect WiFi |
| `async_scan_wifi()` | Start WiFi scan |
| `async_set_node_name(node_id, name)` | Set node name |

### Ventilation states

| State | Description |
|-------|-------------|
| `AUTO` | Fully automatic |
| `MAN1` / `MAN2` / `MAN3` | Manual low / medium / high |
| `CNT1` / `CNT2` / `CNT3` | Continuous low / medium / high |
| `EMPT` | Away / minimal ventilation |

## CLI

The package installs a `duco` command for quick interaction with the box from the terminal.

```bash
duco [--host HOST] <command>
```

The host defaults to `192.168.3.94`. Override with `--host` or the `DUCO_HOST` environment variable.

### Commands

| Command | Description |
|---------|-------------|
| `duco info` | Board info, IP address, WiFi signal, write requests remaining |
| `duco nodes` | All nodes with type, ventilation state, mode, and sensor readings |
| `duco zones` | All zones and their groups |
| `duco set <NODE_ID> <STATE>` | Set ventilation state on a node |

### Examples

```bash
# Show box status
duco info

# List all nodes
duco nodes

# Set node 1 to manual level 2
duco set 1 MAN2

# Set node 1 back to automatic
duco set 1 AUTO

# Use a different host
duco --host 192.168.1.100 nodes

# Via environment variable
DUCO_HOST=192.168.1.100 duco nodes
```

## License

MIT
