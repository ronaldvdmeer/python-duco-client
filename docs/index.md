# python-duco-client Documentation

Async Python client library for the [DUCO ventilation box](https://www.duco.eu) local REST API, built on `aiohttp`.

## Pages

- [**Quickstart**](quickstart.md) — Installation and first API calls
- [**API Reference**](api-reference.md) — All client methods and response models
- [**CLI**](cli.md) — Built-in command-line interface
- [**Error Handling**](error-handling.md) — Exception hierarchy and best practices

## Supported hardware

This library communicates with the **DUCO Connectivity Board** (article 0000-4810) via its local REST API over WiFi or Ethernet.

| Hardware | Status |
|---|---|
| DUCO Connectivity Board 1.0 | Supported |
| DUCO Connectivity Board 2.0 | Not tested |

Compatible DucoBox models (as listed by Duco):

- DucoBox Silent Connect
- DucoBox Focus (from firmware version 17xxxx)
- DucoBox Hygro Plus
- DucoBox Energy Comfort / Energy Comfort Plus
- DucoBox Energy Premium

## Vendor documentation

Original Duco documents are archived in [docs/vendor/](vendor/) for reference.

| Document | Description |
|---|---|
| [Technical datasheet](vendor/technische-fiche-Duco-Connectivity-Board-1.0-(nl).pdf) | Connectivity Board 1.0 — specifications and LED indicators (NL) |
| [Installation guide](vendor/installatiehandleiding-Duco-Connectivity-Board-1.0-(nl).pdf) | Connectivity Board 1.0 — installation instructions (NL) |
