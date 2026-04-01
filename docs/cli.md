# CLI

The package installs a `duco` command for quick interaction with the box from the terminal.

## Usage

```bash
duco [--host HOST] <command>
```

The host defaults to `192.168.3.94`. Override with `--host` or the `DUCO_HOST` environment variable.

## Commands

| Command | Description |
|---|---|
| `duco info` | Board info, IP address, WiFi signal, write requests remaining |
| `duco nodes` | All nodes with type, ventilation state, mode, and sensor readings |
| `duco zones` | All zones and their groups |
| `duco set <NODE_ID> <STATE>` | Set ventilation state on a node |

## Examples

```bash
# Show box status
duco info

# List all nodes
duco nodes

# List all zones
duco zones

# Set node 1 to manual level 2
duco set 1 MAN2

# Set node 1 back to automatic
duco set 1 AUTO

# Use a different host
duco --host 192.168.1.100 nodes

# Via environment variable
DUCO_HOST=192.168.1.100 duco nodes
```

## Ventilation states for `set`

All values from `VentilationState` are valid: `AUTO`, `MAN1`, `MAN2`, `MAN3`, `CNT1`, `CNT2`, `CNT3`, `EMPT`, and extended variants.

See [API Reference — Ventilation states](api-reference.md#ventilation-states) for the full list.
