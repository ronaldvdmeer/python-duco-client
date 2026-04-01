"""Command-line interface for the Duco ventilation API."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys

import aiohttp

from .client import DucoClient
from .exceptions import DucoConnectionError, DucoError
from .models import VentilationState


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="duco",
        description="Duco ventilation box CLI",
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("DUCO_HOST", "192.168.3.94"),
        metavar="HOST",
        help="IP address or hostname of the Duco box (default: 192.168.3.94, or DUCO_HOST env var)",
    )

    sub = parser.add_subparsers(dest="command", metavar="command")
    sub.required = True

    # info
    sub.add_parser("info", help="Show board and LAN information")

    # nodes
    sub.add_parser("nodes", help="List all nodes and their ventilation state")

    # zones
    sub.add_parser("zones", help="List all zones and groups")

    # set
    set_p = sub.add_parser("set", help="Set ventilation state on a node")
    set_p.add_argument("node_id", type=int, metavar="NODE_ID", help="Node ID (e.g. 1)")
    set_p.add_argument(
        "state",
        metavar="STATE",
        help=f"Ventilation state. Valid values: {', '.join(s.value for s in VentilationState)}",
    )

    return parser


async def _run(args: argparse.Namespace) -> int:
    async with aiohttp.ClientSession() as session:
        client = DucoClient(session=session, host=args.host)

        if args.command == "info":
            board = await client.async_get_board_info()
            lan = await client.async_get_lan_info()
            remaining = await client.async_get_write_req_remaining()
            print(f"Box:        {board.box_name} ({board.box_sub_type_name})")
            print(f"Serial:     {board.serial_duco_comm}")
            print(f"IP:         {lan.ip}  WiFi: {lan.rssi_wifi} dBm")
            print(f"Host:       {lan.host_name}")
            print(f"Write req:  {remaining} remaining")

        elif args.command == "nodes":
            nodes = await client.async_get_nodes()
            for node in nodes:
                g = node.general
                v = node.ventilation
                state = v.state if v else "-"
                mode = v.mode if v else "-"
                sensor_str = ""
                if node.sensor:
                    parts = []
                    if node.sensor.co2 is not None:
                        parts.append(f"CO2={node.sensor.co2}ppm")
                    if node.sensor.iaq_co2 is not None:
                        parts.append(f"IAQ={node.sensor.iaq_co2}")
                    sensor_str = f"  [{', '.join(parts)}]"
                print(
                    f"Node {node.node_id:>3}  {g.node_type:<6}  {g.network_type:<4}"
                    f"  state={state:<8}  mode={mode:<4}{sensor_str}"
                )

        elif args.command == "zones":
            zones = await client.async_get_zones()
            for zone in zones:
                print(f"Zone {zone.zone_id}: {zone.name}")
                for group in zone.groups:
                    print(f"  Group {group.group_id}: nodes {group.nodes}")

        elif args.command == "set":
            await client.async_set_ventilation_state(args.node_id, args.state)
            print(f"Node {args.node_id}: state set to {args.state}")

    return 0


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    try:
        sys.exit(asyncio.run(_run(args)))
    except DucoConnectionError as err:
        print(f"Connection error: {err}", file=sys.stderr)
        sys.exit(1)
    except DucoError as err:
        print(f"API error: {err}", file=sys.stderr)
        sys.exit(1)
