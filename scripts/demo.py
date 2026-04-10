"""Demo script for the python-duco-client library.

Connects to a real Duco Connectivity Board and prints a structured overview
of all data returned by every available GET method.

Usage:
    python scripts/demo.py
    python scripts/demo.py --host 192.168.1.100
"""

from __future__ import annotations

import argparse
import asyncio
import time

import aiohttp

from duco import DucoClient

DEFAULT_HOST = "192.168.3.94"


def header(title: str) -> None:
    width = 60
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


def section(title: str) -> None:
    print()
    print(f"--- {title} ---")


async def run(host: str) -> None:
    async with aiohttp.ClientSession() as session:
        client = DucoClient(session=session, host=host)

        print(f"\nConnecting to Duco box at {host} …\n")

        # ── API info ──────────────────────────────────────────────────────────
        header("API INFO")
        api = await client.async_get_api_info()
        print(f"  API version : {api.api_version}")

        # ── Board info ────────────────────────────────────────────────────────
        header("BOARD INFO")
        board = await client.async_get_board_info()
        print(f"  Box name            : {board.box_name}")
        print(f"  Box sub-type        : {board.box_sub_type_name}")
        print(f"  Serial (box board)  : {board.serial_board_box}")
        print(f"  Serial (comm board) : {board.serial_board_comm}")
        print(f"  Serial (Duco box)   : {board.serial_duco_box}")
        print(f"  Serial (Duco comm)  : {board.serial_duco_comm}")
        box_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(board.time))
        print(f"  Box time            : {box_time}")

        # ── LAN info ──────────────────────────────────────────────────────────
        header("NETWORK (LAN)")
        lan = await client.async_get_lan_info()
        print(f"  Mode            : {lan.mode}")
        print(f"  IP              : {lan.ip}")
        print(f"  Subnet mask     : {lan.net_mask}")
        print(f"  Default gateway : {lan.default_gateway}")
        print(f"  DNS             : {lan.dns}")
        print(f"  MAC             : {lan.mac}")
        print(f"  Hostname        : {lan.host_name}")
        print(f"  WiFi RSSI       : {lan.rssi_wifi} dBm")

        # ── Diagnostics ───────────────────────────────────────────────────────
        header("DIAGNOSTICS")
        diags = await client.async_get_diagnostics()
        for d in diags:
            print(f"  {d.component:<30}  {d.status}")

        # ── Write request budget ──────────────────────────────────────────────
        header("WRITE REQUEST BUDGET")
        remaining = await client.async_get_write_req_remaining()
        print(f"  Remaining write requests : {remaining}")

        # ── System config ─────────────────────────────────────────────────────
        header("SYSTEM CONFIG")
        cfg = await client.async_get_system_config()
        print(f"  Time zone               : UTC{cfg.time_zone:+d}")
        print(f"  DST                     : {'on' if cfg.dst else 'off'}")
        print(f"  Modbus address          : {cfg.modbus_addr}")
        print(f"  Modbus offset           : {cfg.modbus_offset}")
        print(f"  LAN DHCP                : {'on' if cfg.lan_dhcp else 'off'}")
        print(f"  LAN static IP           : {cfg.lan_static_ip}")
        print(f"  LAN static netmask      : {cfg.lan_static_net_mask}")
        print(f"  LAN static gateway      : {cfg.lan_static_default_gateway}")
        print(f"  LAN static DNS          : {cfg.lan_static_dns}")
        print(f"  WiFi SSID               : {cfg.lan_wifi_client_ssid}")
        print(f"  Auto-reboot period      : {cfg.auto_reboot_comm_period} days")
        reboot_hh = cfg.auto_reboot_comm_time // 60
        reboot_mm = cfg.auto_reboot_comm_time % 60
        print(f"  Auto-reboot time        : {reboot_hh:02d}:{reboot_mm:02d}")

        # ── Nodes ─────────────────────────────────────────────────────────────
        header("NODES")
        nodes = await client.async_get_nodes()
        print(f"  Total nodes: {len(nodes)}")
        for node in nodes:
            section(f"Node {node.node_id} — {node.general.node_type} ({node.general.name or '(no name)'})")
            g = node.general
            print(f"    Type         : {g.node_type}")
            print(f"    Network      : {g.network_type}")
            print(f"    Sub-type     : {g.sub_type}")
            print(f"    Parent       : {g.parent}")
            print(f"    Association  : {g.asso}")
            if node.ventilation is not None:
                v = node.ventilation
                print(f"    Vent state   : {v.state}")
                print(f"    Vent mode    : {v.mode}")
                if v.flow_lvl_tgt is not None:
                    print(f"    Flow level   : {v.flow_lvl_tgt}")
                remaining_s = v.time_state_remain
                print(f"    State remain : {remaining_s} s")
            if node.sensor is not None:
                s = node.sensor
                if s.co2 is not None:
                    print(f"    CO2          : {s.co2} ppm  (IAQ {s.iaq_co2})")
                if s.rh is not None:
                    print(f"    Humidity     : {s.rh:.1f} %  (IAQ {s.iaq_rh})")

        # ── Node configs ──────────────────────────────────────────────────────
        header("NODE CONFIGS")
        node_configs = await client.async_get_node_configs()
        for nc in node_configs:
            name_display = nc.name if nc.name else "(no name)"
            print(f"  Node {nc.node_id:<4}  {name_display}")

        # ── Zones (info) ──────────────────────────────────────────────────────
        header("ZONES (INFO)")
        zones = await client.async_get_zones()
        print(f"  Total zones: {len(zones)}")
        for z in zones:
            print(f"  Zone {z.zone_id}: {z.name}")
            for g in z.groups:
                print(f"    Group {g.group_id}: nodes {g.nodes}")

        # ── Zones (config) ────────────────────────────────────────────────────
        header("ZONES (CONFIG)")
        zone_configs = await client.async_get_zone_configs()
        for z in zone_configs:
            print(f"  Zone {z.zone_id}: {z.name}")
            for g in z.groups:
                print(f"    Group {g.group_id}: nodes {g.nodes}")

        # ── Actions (system-level) ────────────────────────────────────────────
        header("SYSTEM ACTIONS")
        actions = await client.async_get_actions()
        for a in actions:
            if a.enum_values:
                print(f"  {a.action:<35}  {a.val_type}  {a.enum_values}")
            else:
                print(f"  {a.action:<35}  {a.val_type}")

        # ── Actions (per node) ────────────────────────────────────────────────
        header("NODE ACTIONS")
        node_actions = await client.async_get_node_actions()
        for na in node_actions:
            names = [a.action for a in na.actions]
            print(f"  Node {na.node_id:<4}  {names}")

        print()
        print("Done.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Duco client demo — print all box data.")
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"IP address or hostname of the Duco box (default: {DEFAULT_HOST})",
    )
    args = parser.parse_args()
    asyncio.run(run(args.host))


if __name__ == "__main__":
    main()
