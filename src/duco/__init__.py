"""Async Python client for the Duco ventilation API."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from .client import DucoClient
from .exceptions import (
    DucoConnectionError,
    DucoError,
    DucoRateLimitError,
)
from .models import (
    ApiInfo,
    BoardInfo,
    DiagComponent,
    LanInfo,
    NetworkType,
    Node,
    NodeGeneralInfo,
    NodeSensorInfo,
    NodeType,
    NodeVentilationInfo,
    SystemConfig,
    VentilationMode,
    VentilationState,
    Zone,
    ZoneGroup,
)

try:
    __version__ = version("python-duco-client")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "ApiInfo",
    "BoardInfo",
    "DiagComponent",
    "DucoClient",
    "DucoConnectionError",
    "DucoError",
    "DucoRateLimitError",
    "LanInfo",
    "NetworkType",
    "Node",
    "NodeGeneralInfo",
    "NodeSensorInfo",
    "NodeType",
    "NodeVentilationInfo",
    "SystemConfig",
    "VentilationMode",
    "VentilationState",
    "Zone",
    "ZoneGroup",
    "__version__",
]
