# CLI

The package installs a `duco` command for quick interaction with the box from the terminal.

## Usage

```bash
duco [--host HOST] [--https] <command>
```

Use `--host` or the `DUCO_HOST` environment variable to specify the IP address or hostname of your Duco box.

Use `--https` to connect over HTTPS with the bundled Duco CA certificate. This is required for newer
Duco Connectivity Board firmware that only exposes certain data (such as node temperature) over the
authenticated HTTPS API. The bundled CA is trusted automatically; no extra configuration is needed.

## Options

| Option | Default | Description |
|---|---|---|
| `--host HOST` | _(required)_ | IP address or hostname of the Duco box |
| `--https` | off | Use HTTPS with the bundled Duco CA certificate |

Both options can also be set via environment variables: `DUCO_HOST` and `DUCO_HTTPS=1`.

## Commands

| Command | Description |
|---|---|
| `duco info` | Board info, IP address, WiFi signal, write requests remaining |
| `duco nodes` | All nodes with type, ventilation state, mode, and sensor readings |
| `duco zones` | All zones and their groups |
| `duco set <NODE_ID> <STATE>` | Set ventilation state on a node |

## Examples

```bash
# Show box status over HTTP (default)
duco info

# Show box status over HTTPS (required for temperature data)
duco --https info

# List all nodes including temperature readings
duco --https nodes

# List all zones
duco zones

# Set node 1 to manual level 2
duco set 1 MAN2

# Set node 1 back to automatic
duco set 1 AUTO

# Use a different host
duco --host 192.168.1.100 nodes

# Use a different host over HTTPS
duco --host 192.168.1.100 --https nodes

# Via environment variables
DUCO_HOST=192.168.1.100 DUCO_HTTPS=1 duco nodes
```

## Ventilation states for `set`

All values from `VentilationState` are valid: `AUTO`, `MAN1`, `MAN2`, `MAN3`, `CNT1`, `CNT2`, `CNT3`, `EMPT`, and extended variants.

See [API Reference — Ventilation states](api-reference.md#ventilation-states) for the full list.
