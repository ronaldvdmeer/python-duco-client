# python-duco-client

Async Python client for the DUCO ventilation box local REST API.

## Installation

```bash
pip install python-duco-client
```

## Quick start

```python
import asyncio
import aiohttp
from duco import DucoClient

async def main():
    async with aiohttp.ClientSession() as session:
        client = DucoClient(session=session, host="192.168.1.100")

        board = await client.async_get_board_info()
        print(f"Box: {board.box_name} ({board.box_sub_type_name})")

        nodes = await client.async_get_nodes()
        for node in nodes:
            print(f"Node {node.node_id}: {node.general.node_type}")
            if node.sensor and node.sensor.co2 is not None:
                print(f"  CO2: {node.sensor.co2} ppm")

        await client.async_set_ventilation_state(1, "MAN2")

asyncio.run(main())
```

## CLI

```bash
duco --host 192.168.1.100 info
duco --host 192.168.1.100 nodes
duco --host 192.168.1.100 set 1 MAN2
```

## Documentation

See the [docs/](docs/) folder for the full documentation:

- [Quickstart](docs/quickstart.md)
- [API Reference](docs/api-reference.md)
- [CLI](docs/cli.md)
- [Error Handling](docs/error-handling.md)

## License

MIT

