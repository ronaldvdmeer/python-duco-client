# Quickstart

## Requirements

- Python 3.11+
- aiohttp 3.9+

## Installation

```bash
pip install python-duco-client
```

## Connect to the box

You need the IP address of your DUCO Connectivity Board. Find it via your router's DHCP table, or run:

```bash
duco --host <ip> info
```

## First API calls

```python
import asyncio
import aiohttp
from duco import DucoClient

async def main():
    async with aiohttp.ClientSession() as session:
        client = DucoClient(session=session, host="192.168.1.100")

        # Get box info
        board = await client.async_get_board_info()
        print(f"Box:    {board.box_name} ({board.box_sub_type_name})")
        print(f"Serial: {board.serial_duco_comm}")

        # Get network info
        lan = await client.async_get_lan_info()
        print(f"IP:     {lan.ip}  WiFi: {lan.rssi_wifi} dBm")

        # List all nodes
        nodes = await client.async_get_nodes()
        for node in nodes:
            print(f"Node {node.node_id}: {node.general.node_type}")
            if node.sensor and node.sensor.co2 is not None:
                print(f"  CO2: {node.sensor.co2} ppm")

        # Set ventilation to manual level 2
        await client.async_set_ventilation_state(1, "MAN2")

        # Back to automatic
        await client.async_set_ventilation_state(1, "AUTO")

asyncio.run(main())
```

## Using the CLI

The package also installs a `duco` command for quick terminal access:

```bash
duco --host 192.168.1.100 info
duco --host 192.168.1.100 nodes
duco --host 192.168.1.100 set 1 MAN2
```

See [CLI](cli.md) for full details.
