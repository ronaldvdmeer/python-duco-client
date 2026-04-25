"""
Duco box inventory script.

Queries all known API endpoints of a Duco box and writes a Markdown report
with the raw responses, suitable for analysing what data is available for
enriching the Home Assistant integration.

Usage:
    python scripts/inventory.py [--host HOST] [--output PATH]

Defaults:
    --host   192.168.3.94
    --output duco_inventory.md
"""

from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import aiohttp

HOST_DEFAULT = "192.168.3.94"
OUTPUT_DEFAULT = "duco_inventory.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _pretty(data: Any) -> str:
    """Return compact, readable JSON block."""
    return json.dumps(data, indent=2, ensure_ascii=False)


async def _get(session: aiohttp.ClientSession, base: str, path: str, **params: str) -> tuple[int, Any]:
    """Perform a GET and return (status_code, parsed_body)."""
    url = f"{base}{path}"
    try:
        async with session.get(url, params=params or None, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            status = resp.status
            try:
                body = await resp.json(content_type=None)
            except Exception:
                body = await resp.text()
            return status, body
    except Exception as exc:
        return 0, f"ERROR: {exc}"


# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------


def _section(lines: list[str], heading: str, level: int = 2) -> None:
    prefix = "#" * level
    lines.append(f"\n{prefix} {heading}\n")


def _code(lines: list[str], data: Any, lang: str = "json") -> None:
    lines.append(f"```{lang}")
    lines.append(_pretty(data) if not isinstance(data, str) else data)
    lines.append("```\n")


def _field_table(lines: list[str], rows: list[tuple[str, str, str]]) -> None:
    """Render a markdown table with columns Path | Value | Notes."""
    lines.append("| Field path | Value | Notes |")
    lines.append("|---|---|---|")
    for path, value, notes in rows:
        lines.append(f"| `{path}` | `{value}` | {notes} |")
    lines.append("")


def _flatten(data: Any, prefix: str = "") -> list[tuple[str, Any]]:
    """Recursively flatten a JSON object into (dotted.path, value) pairs."""
    results: list[tuple[str, Any]] = []
    if isinstance(data, dict):
        for k, v in data.items():
            results.extend(_flatten(v, f"{prefix}.{k}" if prefix else k))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            results.extend(_flatten(v, f"{prefix}[{i}]"))
    else:
        results.append((prefix, data))
    return results


def _node_table(lines: list[str], nodes: list[dict[str, Any]]) -> None:
    """Render a summary table of all nodes."""
    lines.append("| Node | Type | SubType | Network | Name | Vent state | CO2 | RH | IAQ CO2 | IAQ RH |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for n in nodes:
        node_id = n.get("Node", "?")
        g = n.get("General", {})
        ntype = g.get("Type", {}).get("Val", "")
        sub = g.get("SubType", {}).get("Val", "")
        net = g.get("NetworkType", {}).get("Val", "")
        name = g.get("Name", {}).get("Val", "")
        vent = n.get("Ventilation", {}).get("State", {}).get("Val", "") if "Ventilation" in n else ""
        sensor = n.get("Sensor", {})
        co2 = sensor.get("Co2", {}).get("Val", "") if sensor else ""
        rh = sensor.get("Rh", {}).get("Val", "") if sensor else ""
        iaq_co2 = sensor.get("IaqCo2", {}).get("Val", "") if sensor else ""
        iaq_rh = sensor.get("IaqRh", {}).get("Val", "") if sensor else ""
        lines.append(f"| {node_id} | {ntype} | {sub} | {net} | {name} | {vent} | {co2} | {rh} | {iaq_co2} | {iaq_rh} |")
    lines.append("")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def run(host: str, output: Path) -> None:
    base = f"http://{host}"
    lines: list[str] = []

    lines.append("# Duco box API inventory")
    lines.append(f"\n_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} — host: `{host}`_\n")
    lines.append(
        "This document is an automated inventory of all data available from the Duco box REST API. "
        "It is used to determine which additional sensors and entities can be added to the Home Assistant integration.\n"
    )

    lines.append("## Table of contents\n")
    lines.append("1. [API version](#api-version)")
    lines.append("2. [Board info](#board-info)")
    lines.append("3. [Network (LAN) info](#network-lan-info)")
    lines.append("4. [Diagnostics](#diagnostics)")
    lines.append("5. [Write request budget](#write-request-budget)")
    lines.append("6. [Nodes overview](#nodes-overview)")
    lines.append("7. [Node detail — per node](#node-detail--per-node)")
    lines.append("8. [Ventilation temperatures](#ventilation-temperatures)")
    lines.append("9. [Heat recovery](#heat-recovery)")
    lines.append("10. [Zones](#zones)")
    lines.append("11. [Config — system](#config--system)")
    lines.append("12. [Config — nodes](#config--nodes)")
    lines.append("13. [Actions — system](#actions--system)")
    lines.append("14. [Actions — nodes](#actions--nodes)")
    lines.append("15. [Available endpoints from /api](#available-endpoints-from-api)")
    lines.append("")

    async with aiohttp.ClientSession() as session:

        # ------------------------------------------------------------------
        # /api
        # ------------------------------------------------------------------
        _section(lines, "Available endpoints from /api")
        status, data = await _get(session, base, "/api")
        lines.append(f"_Status: {status}_\n")
        _code(lines, data)

        # ------------------------------------------------------------------
        # /info?module=General&submodule=Board
        # ------------------------------------------------------------------
        _section(lines, "Board info")
        status, data = await _get(session, base, "/info", module="General", submodule="Board")
        lines.append(f"_Status: {status}_\n")
        board = {}
        if isinstance(data, dict):
            board = data.get("General", {}).get("Board", {})
            rows = [(k, v.get("Val", ""), "") for k, v in board.items() if isinstance(v, dict) and "Val" in v]
            _field_table(lines, rows)
        _code(lines, data)

        # ------------------------------------------------------------------
        # /info?module=General&submodule=Lan
        # ------------------------------------------------------------------
        _section(lines, "Network (LAN) info")
        status, data = await _get(session, base, "/info", module="General", submodule="Lan")
        lines.append(f"_Status: {status}_\n")
        if isinstance(data, dict):
            lan = data.get("General", {}).get("Lan", {})
            rows = []
            for k, v in lan.items():
                if isinstance(v, dict) and "Val" in v:
                    rows.append((k, str(v["Val"]), ""))
            _field_table(lines, rows)
        _code(lines, data)

        # ------------------------------------------------------------------
        # /info?module=General&submodule=PublicApi
        # ------------------------------------------------------------------
        _section(lines, "Write request budget")
        status, data = await _get(session, base, "/info", module="General", submodule="PublicApi")
        lines.append(f"_Status: {status}_\n")
        if isinstance(data, dict):
            pub = data.get("General", {}).get("PublicApi", {})
            remain = pub.get("WriteReqCntRemain", {}).get("Val", "?")
            lines.append(f"Remaining write requests: **{remain}**\n")
        _code(lines, data)

        # ------------------------------------------------------------------
        # /info?module=Diag
        # ------------------------------------------------------------------
        _section(lines, "Diagnostics")
        status, data = await _get(session, base, "/info", module="Diag")
        lines.append(f"_Status: {status}_\n")
        if isinstance(data, dict):
            subsystems = data.get("Diag", {}).get("SubSystems", [])
            if subsystems:
                lines.append("| Component | Status |")
                lines.append("|---|---|")
                for item in subsystems:
                    lines.append(f"| {item.get('Component', '')} | {item.get('Status', '')} |")
                lines.append("")
        _code(lines, data)

        # ------------------------------------------------------------------
        # /info?module=Ventilation  (temperatures)
        # ------------------------------------------------------------------
        _section(lines, "Ventilation temperatures")
        status, data = await _get(session, base, "/info", module="Ventilation")
        lines.append(f"_Status: {status}_\n")
        if isinstance(data, dict):
            sensor = data.get("Ventilation", {}).get("Sensor", {})
            if sensor:
                lines.append("| Sensor | Value (raw) | Description |")
                lines.append("|---|---|---|")
                desc = {
                    "TempOda": "Outside air temperature (°C × 10)",
                    "TempSup": "Supply air temperature (°C × 10)",
                    "TempEta": "Extract air temperature (°C × 10)",
                    "TempEha": "Exhaust air temperature (°C × 10)",
                }
                for k, v in sensor.items():
                    val = v.get("Val", "") if isinstance(v, dict) else ""
                    lines.append(f"| {k} | {val} | {desc.get(k, '')} |")
                lines.append("")
        _code(lines, data)

        # ------------------------------------------------------------------
        # /info?module=HeatRecovery
        # ------------------------------------------------------------------
        _section(lines, "Heat recovery")
        status, data = await _get(session, base, "/info", module="HeatRecovery")
        lines.append(f"_Status: {status}_\n")
        _code(lines, data)

        # ------------------------------------------------------------------
        # /info/nodes  (overview)
        # ------------------------------------------------------------------
        _section(lines, "Nodes overview")
        status, data = await _get(session, base, "/info/nodes")
        lines.append(f"_Status: {status}_\n")
        node_list: list[dict[str, Any]] = []
        if isinstance(data, dict):
            node_list = data.get("Nodes", [])
            _node_table(lines, node_list)
        _code(lines, data)

        # ------------------------------------------------------------------
        # /info/nodes/{node}  (per node detail)
        # ------------------------------------------------------------------
        _section(lines, "Node detail — per node")

        # Collect node IDs
        node_ids_status, node_ids_data = await _get(session, base, "/nodes")
        node_ids: list[int] = []
        if isinstance(node_ids_data, list):
            node_ids = [item["Node"] for item in node_ids_data if isinstance(item, dict) and "Node" in item]

        for nid in node_ids:
            _section(lines, f"Node {nid}", level=3)
            status, data = await _get(session, base, f"/info/nodes/{nid}")
            lines.append(f"_Status: {status}_\n")

            if isinstance(data, dict):
                g = data.get("General", {})
                ntype = g.get("Type", {}).get("Val", "unknown")
                name = g.get("Name", {}).get("Val", "")
                lines.append(f"**Type:** `{ntype}` — **Name:** `{name}`\n")

                # All fields flat
                rows = []
                for path, value in _flatten(data):
                    rows.append((path, str(value), ""))
                if rows:
                    lines.append("| Field | Value | Notes |")
                    lines.append("|---|---|---|")
                    for path, value, notes in rows:
                        lines.append(f"| `{path}` | `{value}` | {notes} |")
                    lines.append("")

            _code(lines, data)

        # ------------------------------------------------------------------
        # /info/zones
        # ------------------------------------------------------------------
        _section(lines, "Zones")
        status, data = await _get(session, base, "/info/zones")
        lines.append(f"_Status: {status}_\n")
        if isinstance(data, dict):
            zones = data.get("Zones", [])
            for z in zones:
                zone_id = z.get("Zone", "?")
                name = z.get("DeviceGroupConfig", {}).get("General", {}).get("Name", {}).get("Val", "")
                groups = z.get("Groups", [])
                lines.append(f"**Zone {zone_id}** — `{name}`\n")
                for g in groups:
                    gid = g.get("Group", "?")
                    nodes_in_group = g.get("DeviceGroupConfig", {}).get("General", {}).get("Nodes", [])
                    lines.append(f"- Group {gid}: nodes {nodes_in_group}")
                lines.append("")
        _code(lines, data)

        # ------------------------------------------------------------------
        # /config  (system config)
        # ------------------------------------------------------------------
        _section(lines, "Config — system")
        status, data = await _get(session, base, "/config")
        lines.append(f"_Status: {status}_\n")
        if isinstance(data, dict):
            rows = []
            for path, value in _flatten(data):
                # Only show "Val" fields to avoid Min/Max/Inc noise
                if path.endswith(".Val") or path.endswith("[Val]"):
                    short = path.rsplit(".", 1)[0]
                    rows.append((short, str(value), ""))
            if rows:
                lines.append("| Config key | Value | Notes |")
                lines.append("|---|---|---|")
                for path, value, notes in rows:
                    lines.append(f"| `{path}` | `{value}` | {notes} |")
                lines.append("")
        _code(lines, data)

        # ------------------------------------------------------------------
        # /config/nodes  (node config)
        # ------------------------------------------------------------------
        _section(lines, "Config — nodes")
        status, data = await _get(session, base, "/config/nodes")
        lines.append(f"_Status: {status}_\n")
        _code(lines, data)

        # ------------------------------------------------------------------
        # /action  (available system actions)
        # ------------------------------------------------------------------
        _section(lines, "Actions — system")
        status, data = await _get(session, base, "/action")
        lines.append(f"_Status: {status}_\n")
        _code(lines, data)

        # ------------------------------------------------------------------
        # /action/nodes  (available node actions)
        # ------------------------------------------------------------------
        _section(lines, "Actions — nodes")
        status, data = await _get(session, base, "/action/nodes")
        lines.append(f"_Status: {status}_\n")
        if isinstance(data, dict):
            node_actions = data.get("Nodes", [])
            for na in node_actions:
                nid = na.get("Node", "?")
                actions = na.get("Actions", [])
                if actions:
                    lines.append(f"**Node {nid}:**\n")
                    lines.append("| Action | ValType | Enum options |")
                    lines.append("|---|---|---|")
                    for a in actions:
                        enum_opts = ", ".join(a.get("Enum", [])) if a.get("Enum") else ""
                        lines.append(f"| {a.get('Action', '')} | {a.get('ValType', '')} | {enum_opts} |")
                    lines.append("")
        _code(lines, data)

    # Write output
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to: {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Duco box API inventory tool")
    parser.add_argument("--host", default=HOST_DEFAULT, help=f"Duco box host (default: {HOST_DEFAULT})")
    parser.add_argument("--output", default=OUTPUT_DEFAULT, help=f"Output markdown file (default: {OUTPUT_DEFAULT})")
    args = parser.parse_args()

    asyncio.run(run(args.host, Path(args.output)))


if __name__ == "__main__":
    main()
