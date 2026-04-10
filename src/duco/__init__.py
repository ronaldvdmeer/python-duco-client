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
    ActionInfo,
    ApiInfo,
    BoardInfo,
    DiagComponent,
    DiagStatus,
    LanInfo,
    NetworkType,
    Node,
    NodeActions,
    NodeConfig,
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
    "ActionInfo",
    "ApiInfo",
    "BoardInfo",
    "DiagComponent",
    "DiagStatus",
    "DucoClient",
    "DucoConnectionError",
    "DucoError",
    "DucoRateLimitError",
    "LanInfo",
    "NetworkType",
    "Node",
    "NodeActions",
    "NodeConfig",
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
