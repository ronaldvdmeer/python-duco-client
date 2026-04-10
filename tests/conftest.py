"""Common test fixtures for Duco API client tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def mock_host() -> str:
    """The mock Duco box host."""
    return "192.168.3.94"


@pytest.fixture
def base_url(mock_host) -> str:
    """The mock base URL."""
    return f"http://{mock_host}"


# ---------------------------------------------------------------------------
# Duco API mock response data
# ---------------------------------------------------------------------------


@pytest.fixture
def api_info_data():
    """Mock response for GET /api."""
    return {
        "PublicApiVersion": {"Val": "2.5"},
        "ApiInfo": [],
    }


@pytest.fixture
def board_info_data():
    """Mock response for GET /info?module=General&submodule=Board."""
    return {
        "General": {
            "Board": {
                "PublicApiVersion": {"Val": "2.5"},
                "BoxName": {"Val": "SILENT_CONNECT"},
                "BoxSubTypeName": {"Val": "Eu"},
                "SerialBoardBox": {"Val": "RS2420002577"},
                "SerialBoardComm": {"Val": "PS2424005629"},
                "SerialDucoBox": {"Val": "n/a"},
                "SerialDucoComm": {"Val": "P369348-241126-033"},
                "Time": {"Val": 1775082497},
            }
        }
    }


@pytest.fixture
def lan_info_data():
    """Mock response for GET /info?module=General&submodule=Lan."""
    return {
        "General": {
            "Lan": {
                "Mode": {"Val": "WIFI_CLIENT"},
                "Ip": {"Val": "192.168.3.94"},
                "NetMask": {"Val": "255.255.255.0"},
                "DefaultGateway": {"Val": "192.168.3.1"},
                "Dns": {"Val": "192.168.3.1"},
                "Mac": {"Val": "a0:dd:6c:06:12:90"},
                "HostName": {"Val": "duco_061293"},
                "DucoClientIp": {"Val": "0.0.0.0"},
                "RssiWifi": {"Val": -44},
                "ScanWifi": [],
            }
        }
    }


@pytest.fixture
def diag_data():
    """Mock response for GET /info?module=Diag."""
    return {
        "Diag": {
            "SubSystems": [
                {"Component": "Ventilation", "Status": "Ok"},
                {"Component": "VentCool", "Status": "Ok"},
                {"Component": "SunCtrl", "Status": "Ok"},
            ]
        }
    }


@pytest.fixture
def nodes_data():
    """Mock response for GET /info/nodes."""
    return {
        "Nodes": [
            {
                "Node": 1,
                "General": {
                    "Type": {"Val": "BOX"},
                    "SubType": {"Val": 1},
                    "NetworkType": {"Val": "VIRT"},
                    "Parent": {"Val": 0},
                    "Asso": {"Val": 0},
                    "Name": {"Val": ""},
                    "Identify": {"Val": 0},
                },
                "Ventilation": {
                    "State": {"Val": "CNT1"},
                    "TimeStateRemain": {"Val": 0},
                    "TimeStateEnd": {"Val": 0},
                    "Mode": {"Val": "MANU"},
                    "FlowLvlTgt": {"Val": 15},
                },
                "Sensor": {
                    "Rh": {"Val": 35.5},
                    "IaqRh": {"Val": 83},
                },
            },
            {
                "Node": 2,
                "General": {
                    "Type": {"Val": "UCCO2"},
                    "SubType": {"Val": 0},
                    "NetworkType": {"Val": "RF"},
                    "Parent": {"Val": 1},
                    "Asso": {"Val": 1},
                    "Name": {"Val": ""},
                    "Identify": {"Val": 0},
                },
                "Ventilation": {
                    "State": {"Val": "CNT1"},
                    "TimeStateRemain": {"Val": 0},
                    "TimeStateEnd": {"Val": 0},
                    "Mode": {"Val": "-"},
                },
                "Sensor": {
                    "Co2": {"Val": 536},
                    "IaqCo2": {"Val": 100},
                },
            },
            {
                "Node": 113,
                "General": {
                    "Type": {"Val": "BSRH"},
                    "SubType": {"Val": 0},
                    "NetworkType": {"Val": "VIRT"},
                    "Parent": {"Val": 1},
                    "Asso": {"Val": 1},
                    "Name": {"Val": ""},
                    "Identify": {"Val": 0},
                },
                "Ventilation": {
                    "State": {"Val": "CNT1"},
                    "TimeStateRemain": {"Val": 0},
                    "TimeStateEnd": {"Val": 0},
                    "Mode": {"Val": "-"},
                },
                "Sensor": {
                    "Rh": {"Val": 36.0},
                    "IaqRh": {"Val": 81},
                },
            },
        ]
    }


@pytest.fixture
def node_ids_data():
    """Mock response for GET /nodes (raw JSON array)."""
    return [{"Node": 1}, {"Node": 2}, {"Node": 113}]


@pytest.fixture
def zones_data():
    """Mock response for GET /info/zones."""
    return {
        "Zones": [
            {
                "Zone": 1,
                "DeviceGroupConfig": {"General": {"Name": {"Val": "VentEtaCentral"}}},
                "Groups": [
                    {
                        "Group": 1,
                        "DeviceGroupConfig": {"General": {"Nodes": [2, 113]}},
                    }
                ],
            }
        ]
    }
