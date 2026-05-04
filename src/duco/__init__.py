"""Async Python client for the Duco ventilation API."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from ._ssl import build_ssl_context
from .client import DucoClient
from .exceptions import (
    DucoAuthenticationError,
    DucoConnectionError,
    DucoError,
    DucoRateLimitError,
)
from .models import (
    ActionInfo,
    ApiEndpointInfo,
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
    "ApiEndpointInfo",
    "ApiInfo",
    "BoardInfo",
    "DiagComponent",
    "DiagStatus",
    "DucoAuthenticationError",
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
    "build_ssl_context",
]
