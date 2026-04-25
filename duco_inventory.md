# Duco box API inventory

_Generated: 2026-04-10 15:06:58 — host: `192.168.3.94`_

This document is an automated inventory of all data available from the Duco box REST API. It is used to determine which additional sensors and entities can be added to the Home Assistant integration.

## Table of contents

1. [API version](#api-version)
2. [Board info](#board-info)
3. [Network (LAN) info](#network-lan-info)
4. [Diagnostics](#diagnostics)
5. [Write request budget](#write-request-budget)
6. [Nodes overview](#nodes-overview)
7. [Node detail — per node](#node-detail--per-node)
8. [Ventilation temperatures](#ventilation-temperatures)
9. [Heat recovery](#heat-recovery)
10. [Zones](#zones)
11. [Config — system](#config--system)
12. [Config — nodes](#config--nodes)
13. [Actions — system](#actions--system)
14. [Actions — nodes](#actions--nodes)
15. [Available endpoints from /api](#available-endpoints-from-api)


## Available endpoints from /api

_Status: 200_

```json
{
  "PublicApiVersion": {
    "Val": "2.5"
  },
  "ApiInfo": [
    {
      "Url": "/api",
      "QueryParameters": [],
      "Methods": [
        "GET"
      ]
    },
    {
      "Url": "/info",
      "QueryParameters": [
        "module",
        "submodule",
        "parameter"
      ],
      "Methods": [
        "GET"
      ],
      "Modules": [
        "General",
        "Diag",
        "Ventilation",
        "WeatherHandler"
      ]
    },
    {
      "Url": "/info/nodes",
      "QueryParameters": [
        "from",
        "module",
        "parameter"
      ],
      "Methods": [
        "GET"
      ],
      "Modules": [
        "General",
        "NetworkDuco",
        "Sensor"
      ]
    },
    {
      "Url": "/info/nodes/{node}",
      "QueryParameters": [
        "module",
        "parameter"
      ],
      "Methods": [
        "GET"
      ],
      "Modules": [
        "General",
        "NetworkDuco",
        "Sensor"
      ]
    },
    {
      "Url": "/info/zones",
      "QueryParameters": [
        "from",
        "zone",
        "group",
        "module",
        "submodule",
        "parameter"
      ],
      "Methods": [
        "GET"
      ],
      "Modules": [
        "DeviceGroupConfig"
      ]
    },
    {
      "Url": "/info/zones/{zone}",
      "QueryParameters": [
        "group",
        "module",
        "submodule",
        "parameter"
      ],
      "Methods": [
        "GET"
      ],
      "Modules": [
        "DeviceGroupConfig"
      ]
    },
    {
      "Url": "/info/zones/{zone}/groups/{group}",
      "QueryParameters": [
        "module",
        "submodule",
        "parameter"
      ],
      "Methods": [
        "GET"
      ],
      "Modules": [
        "DeviceGroupConfig"
      ]
    },
    {
      "Url": "/config",
      "QueryParameters": [
        "module",
        "submodule",
        "parameter"
      ],
      "Methods": [
        "GET",
        "PATCH"
      ],
      "Modules": [
        "General"
      ]
    },
    {
      "Url": "/config/nodes",
      "QueryParameters": [
        "from",
        "parameter"
      ],
      "Methods": [
        "GET"
      ]
    },
    {
      "Url": "/nodes",
      "QueryParameters": [],
      "Methods": [
        "GET"
      ]
    },
    {
      "Url": "/config/nodes/{node}",
      "QueryParameters": [
        "parameter"
      ],
      "Methods": [
        "GET",
        "PATCH"
      ]
    },
    {
      "Url": "/config/zones",
      "QueryParameters": [
        "from",
        "zone",
        "group",
        "module",
        "submodule",
        "parameter"
      ],
      "Methods": [
        "GET"
      ],
      "Modules": [
        "DeviceGroupConfig"
      ]
    },
    {
      "Url": "/config/zones/{zone}",
      "QueryParameters": [
        "group",
        "module",
        "submodule",
        "parameter"
      ],
      "Methods": [
        "GET",
        "PATCH"
      ],
      "Modules": [
        "DeviceGroupConfig"
      ]
    },
    {
      "Url": "/config/zones/{zone}/groups/{group}",
      "QueryParameters": [
        "module",
        "submodule",
        "parameter"
      ],
      "Methods": [
        "GET",
        "PATCH"
      ],
      "Modules": []
    },
    {
      "Url": "/action",
      "QueryParameters": [
        "action"
      ],
      "Methods": [
        "GET",
        "POST"
      ]
    },
    {
      "Url": "/action/nodes",
      "QueryParameters": [
        "from",
        "action"
      ],
      "Methods": [
        "GET"
      ]
    },
    {
      "Url": "/action/nodes/{node}",
      "QueryParameters": [
        "from",
        "action"
      ],
      "Methods": [
        "GET",
        "POST"
      ]
    }
  ]
}
```


## Board info

_Status: 200_

| Field path | Value | Notes |
|---|---|---|
| `PublicApiVersion` | `2.5` |  |
| `BoxName` | `SILENT_CONNECT` |  |
| `BoxSubTypeName` | `Eu` |  |
| `SerialBoardBox` | `RS2420002577` |  |
| `SerialBoardComm` | `PS2424005629` |  |
| `SerialDucoBox` | `n/a` |  |
| `SerialDucoComm` | `P369348-241126-033` |  |
| `Time` | `1775833618` |  |

```json
{
  "General": {
    "Board": {
      "PublicApiVersion": {
        "Val": "2.5"
      },
      "BoxName": {
        "Val": "SILENT_CONNECT"
      },
      "BoxSubTypeName": {
        "Val": "Eu"
      },
      "SerialBoardBox": {
        "Val": "RS2420002577"
      },
      "SerialBoardComm": {
        "Val": "PS2424005629"
      },
      "SerialDucoBox": {
        "Val": "n/a"
      },
      "SerialDucoComm": {
        "Val": "P369348-241126-033"
      },
      "Time": {
        "Val": 1775833618
      }
    }
  }
}
```


## Network (LAN) info

_Status: 200_

| Field path | Value | Notes |
|---|---|---|
| `Mode` | `WIFI_CLIENT` |  |
| `Ip` | `192.168.3.94` |  |
| `NetMask` | `255.255.255.0` |  |
| `DefaultGateway` | `192.168.3.1` |  |
| `Dns` | `192.168.3.1` |  |
| `Mac` | `a0:dd:6c:06:12:90` |  |
| `HostName` | `duco_061293` |  |
| `DucoClientIp` | `0.0.0.0` |  |
| `WifiApSsid` | `DUCO` |  |
| `WifiApKey` | `12345678` |  |
| `RssiWifi` | `-43` |  |

```json
{
  "General": {
    "Lan": {
      "Mode": {
        "Val": "WIFI_CLIENT"
      },
      "Ip": {
        "Val": "192.168.3.94"
      },
      "NetMask": {
        "Val": "255.255.255.0"
      },
      "DefaultGateway": {
        "Val": "192.168.3.1"
      },
      "Dns": {
        "Val": "192.168.3.1"
      },
      "Mac": {
        "Val": "a0:dd:6c:06:12:90"
      },
      "HostName": {
        "Val": "duco_061293"
      },
      "DucoClientIp": {
        "Val": "0.0.0.0"
      },
      "WifiApSsid": {
        "Val": "DUCO"
      },
      "WifiApKey": {
        "Val": "12345678"
      },
      "RssiWifi": {
        "Val": -43
      },
      "ScanWifi": []
    }
  }
}
```


## Write request budget

_Status: 200_

Remaining write requests: **200**

```json
{
  "General": {
    "PublicApi": {
      "WriteReqCntRemain": {
        "Val": 200
      }
    }
  }
}
```


## Diagnostics

_Status: 200_

| Component | Status |
|---|---|
| Ventilation | Ok |
| VentCool | Ok |
| SunCtrl | Ok |

```json
{
  "Diag": {
    "SubSystems": [
      {
        "Component": "Ventilation",
        "Status": "Ok"
      },
      {
        "Component": "VentCool",
        "Status": "Ok"
      },
      {
        "Component": "SunCtrl",
        "Status": "Ok"
      }
    ]
  }
}
```


## Ventilation temperatures

_Status: 400_

```json
{
  "Code": 3,
  "Result": "FAILED"
}
```


## Heat recovery

_Status: 400_

```json
{
  "Code": 3,
  "Result": "FAILED"
}
```


## Nodes overview

_Status: 200_

| Node | Type | SubType | Network | Name | Vent state | CO2 | RH | IAQ CO2 | IAQ RH |
|---|---|---|---|---|---|---|---|---|---|
| 1 | BOX | 1 | VIRT |  | AUTO |  | 34 |  | 76 |
| 2 | UCCO2 | 0 | RF |  | AUTO | 429 |  | 100 |  |
| 113 | BSRH | 0 | VIRT |  | AUTO |  | 34 |  | 75 |

```json
{
  "Nodes": [
    {
      "Node": 1,
      "General": {
        "Type": {
          "Val": "BOX"
        },
        "SubType": {
          "Val": 1
        },
        "NetworkType": {
          "Val": "VIRT"
        },
        "Parent": {
          "Val": 0
        },
        "Asso": {
          "Val": 0
        },
        "Name": {
          "Val": ""
        },
        "Identify": {
          "Val": 0
        }
      },
      "Ventilation": {
        "State": {
          "Val": "AUTO"
        },
        "TimeStateRemain": {
          "Val": 0
        },
        "TimeStateEnd": {
          "Val": 0
        },
        "Mode": {
          "Val": "AUTO"
        },
        "FlowLvlTgt": {
          "Val": 30
        }
      },
      "Sensor": {
        "Rh": {
          "Val": 34
        },
        "IaqRh": {
          "Val": 76
        }
      }
    },
    {
      "Node": 2,
      "General": {
        "Type": {
          "Val": "UCCO2"
        },
        "SubType": {
          "Val": 0
        },
        "NetworkType": {
          "Val": "RF"
        },
        "Parent": {
          "Val": 1
        },
        "Asso": {
          "Val": 1
        },
        "Name": {
          "Val": ""
        },
        "Identify": {
          "Val": 0
        }
      },
      "Ventilation": {
        "State": {
          "Val": "AUTO"
        },
        "TimeStateRemain": {
          "Val": 0
        },
        "TimeStateEnd": {
          "Val": 0
        },
        "Mode": {
          "Val": "-"
        }
      },
      "Sensor": {
        "Co2": {
          "Val": 429
        },
        "IaqCo2": {
          "Val": 100
        }
      }
    },
    {
      "Node": 113,
      "General": {
        "Type": {
          "Val": "BSRH"
        },
        "SubType": {
          "Val": 0
        },
        "NetworkType": {
          "Val": "VIRT"
        },
        "Parent": {
          "Val": 1
        },
        "Asso": {
          "Val": 1
        },
        "Name": {
          "Val": ""
        },
        "Identify": {
          "Val": 0
        }
      },
      "Ventilation": {
        "State": {
          "Val": "AUTO"
        },
        "TimeStateRemain": {
          "Val": 0
        },
        "TimeStateEnd": {
          "Val": 0
        },
        "Mode": {
          "Val": "-"
        }
      },
      "Sensor": {
        "Rh": {
          "Val": 34
        },
        "IaqRh": {
          "Val": 75
        }
      }
    }
  ]
}
```


## Node detail — per node


### Node 1

_Status: 200_

**Type:** `BOX` — **Name:** ``

| Field | Value | Notes |
|---|---|---|
| `Node` | `1` |  |
| `General.Type.Val` | `BOX` |  |
| `General.SubType.Val` | `1` |  |
| `General.NetworkType.Val` | `VIRT` |  |
| `General.Parent.Val` | `0` |  |
| `General.Asso.Val` | `0` |  |
| `General.Name.Val` | `` |  |
| `General.Identify.Val` | `0` |  |
| `Ventilation.State.Val` | `AUTO` |  |
| `Ventilation.TimeStateRemain.Val` | `0` |  |
| `Ventilation.TimeStateEnd.Val` | `0` |  |
| `Ventilation.Mode.Val` | `AUTO` |  |
| `Ventilation.FlowLvlTgt.Val` | `30` |  |
| `Sensor.Rh.Val` | `34` |  |
| `Sensor.IaqRh.Val` | `76` |  |

```json
{
  "Node": 1,
  "General": {
    "Type": {
      "Val": "BOX"
    },
    "SubType": {
      "Val": 1
    },
    "NetworkType": {
      "Val": "VIRT"
    },
    "Parent": {
      "Val": 0
    },
    "Asso": {
      "Val": 0
    },
    "Name": {
      "Val": ""
    },
    "Identify": {
      "Val": 0
    }
  },
  "Ventilation": {
    "State": {
      "Val": "AUTO"
    },
    "TimeStateRemain": {
      "Val": 0
    },
    "TimeStateEnd": {
      "Val": 0
    },
    "Mode": {
      "Val": "AUTO"
    },
    "FlowLvlTgt": {
      "Val": 30
    }
  },
  "Sensor": {
    "Rh": {
      "Val": 34
    },
    "IaqRh": {
      "Val": 76
    }
  }
}
```


### Node 2

_Status: 200_

**Type:** `UCCO2` — **Name:** ``

| Field | Value | Notes |
|---|---|---|
| `Node` | `2` |  |
| `General.Type.Val` | `UCCO2` |  |
| `General.SubType.Val` | `0` |  |
| `General.NetworkType.Val` | `RF` |  |
| `General.Parent.Val` | `1` |  |
| `General.Asso.Val` | `1` |  |
| `General.Name.Val` | `` |  |
| `General.Identify.Val` | `0` |  |
| `Ventilation.State.Val` | `AUTO` |  |
| `Ventilation.TimeStateRemain.Val` | `0` |  |
| `Ventilation.TimeStateEnd.Val` | `0` |  |
| `Ventilation.Mode.Val` | `-` |  |
| `Sensor.Co2.Val` | `429` |  |
| `Sensor.IaqCo2.Val` | `100` |  |

```json
{
  "Node": 2,
  "General": {
    "Type": {
      "Val": "UCCO2"
    },
    "SubType": {
      "Val": 0
    },
    "NetworkType": {
      "Val": "RF"
    },
    "Parent": {
      "Val": 1
    },
    "Asso": {
      "Val": 1
    },
    "Name": {
      "Val": ""
    },
    "Identify": {
      "Val": 0
    }
  },
  "Ventilation": {
    "State": {
      "Val": "AUTO"
    },
    "TimeStateRemain": {
      "Val": 0
    },
    "TimeStateEnd": {
      "Val": 0
    },
    "Mode": {
      "Val": "-"
    }
  },
  "Sensor": {
    "Co2": {
      "Val": 429
    },
    "IaqCo2": {
      "Val": 100
    }
  }
}
```


### Node 113

_Status: 200_

**Type:** `BSRH` — **Name:** ``

| Field | Value | Notes |
|---|---|---|
| `Node` | `113` |  |
| `General.Type.Val` | `BSRH` |  |
| `General.SubType.Val` | `0` |  |
| `General.NetworkType.Val` | `VIRT` |  |
| `General.Parent.Val` | `1` |  |
| `General.Asso.Val` | `1` |  |
| `General.Name.Val` | `` |  |
| `General.Identify.Val` | `0` |  |
| `Ventilation.State.Val` | `AUTO` |  |
| `Ventilation.TimeStateRemain.Val` | `0` |  |
| `Ventilation.TimeStateEnd.Val` | `0` |  |
| `Ventilation.Mode.Val` | `-` |  |
| `Sensor.Rh.Val` | `34` |  |
| `Sensor.IaqRh.Val` | `75` |  |

```json
{
  "Node": 113,
  "General": {
    "Type": {
      "Val": "BSRH"
    },
    "SubType": {
      "Val": 0
    },
    "NetworkType": {
      "Val": "VIRT"
    },
    "Parent": {
      "Val": 1
    },
    "Asso": {
      "Val": 1
    },
    "Name": {
      "Val": ""
    },
    "Identify": {
      "Val": 0
    }
  },
  "Ventilation": {
    "State": {
      "Val": "AUTO"
    },
    "TimeStateRemain": {
      "Val": 0
    },
    "TimeStateEnd": {
      "Val": 0
    },
    "Mode": {
      "Val": "-"
    }
  },
  "Sensor": {
    "Rh": {
      "Val": 34
    },
    "IaqRh": {
      "Val": 75
    }
  }
}
```


## Zones

_Status: 200_

**Zone 1** — `VentEtaCentral`

- Group 1: nodes [2, 113]

```json
{
  "Zones": [
    {
      "Zone": 1,
      "DeviceGroupConfig": {
        "General": {
          "Name": {
            "Val": "VentEtaCentral"
          }
        }
      },
      "Groups": [
        {
          "Group": 1,
          "DeviceGroupConfig": {
            "General": {
              "Nodes": [
                2,
                113
              ]
            }
          }
        }
      ]
    }
  ]
}
```


## Config — system

_Status: 200_

| Config key | Value | Notes |
|---|---|---|
| `General.Time.TimeZone` | `1` |  |
| `General.Time.Dst` | `1` |  |
| `General.Modbus.Addr` | `1` |  |
| `General.Modbus.Offset` | `1` |  |
| `General.Lan.Mode` | `1` |  |
| `General.Lan.Dhcp` | `1` |  |
| `General.Lan.StaticIp` | `0.0.0.0` |  |
| `General.Lan.StaticNetMask` | `255.255.255.0` |  |
| `General.Lan.StaticDefaultGateway` | `0.0.0.0` |  |
| `General.Lan.StaticDns` | `8.8.8.8` |  |
| `General.Lan.WifiClientSsid` | `IoT Wi-Fi` |  |
| `General.Lan.WifiClientKey` | `` |  |
| `General.AutoRebootComm.Period` | `7` |  |
| `General.AutoRebootComm.Time` | `0` |  |

```json
{
  "General": {
    "Time": {
      "TimeZone": {
        "Val": 1,
        "Min": -11,
        "Inc": 1,
        "Max": 12
      },
      "Dst": {
        "Val": 1,
        "Min": 0,
        "Inc": 1,
        "Max": 1
      }
    },
    "Modbus": {
      "Addr": {
        "Val": 1,
        "Min": 1,
        "Inc": 1,
        "Max": 254
      },
      "Offset": {
        "Val": 1,
        "Min": 0,
        "Inc": 1,
        "Max": 1
      }
    },
    "Lan": {
      "Mode": {
        "Val": 1,
        "Min": 1,
        "Inc": 1,
        "Max": 1
      },
      "Dhcp": {
        "Val": 1,
        "Min": 0,
        "Inc": 1,
        "Max": 1
      },
      "StaticIp": {
        "Val": "0.0.0.0"
      },
      "StaticNetMask": {
        "Val": "255.255.255.0"
      },
      "StaticDefaultGateway": {
        "Val": "0.0.0.0"
      },
      "StaticDns": {
        "Val": "8.8.8.8"
      },
      "WifiClientSsid": {
        "Val": "IoT Wi-Fi"
      },
      "WifiClientKey": {
        "Val": ""
      }
    },
    "AutoRebootComm": {
      "Period": {
        "Val": 7,
        "Min": 0,
        "Inc": 1,
        "Max": 365
      },
      "Time": {
        "Val": 0,
        "Min": 0,
        "Inc": 1,
        "Max": 1439
      }
    }
  }
}
```


## Config — nodes

_Status: 200_

```json
{
  "Nodes": [
    {
      "Node": 1,
      "Name": {
        "Val": ""
      }
    },
    {
      "Node": 2,
      "Name": {
        "Val": ""
      }
    },
    {
      "Node": 113,
      "Name": {
        "Val": ""
      }
    }
  ]
}
```


## Actions — system

_Status: 200_

```json
[
  {
    "Action": "SetTime",
    "ValType": "Integer"
  },
  {
    "Action": "SetIdentify",
    "ValType": "Boolean"
  },
  {
    "Action": "SetIdentifyAll",
    "ValType": "Boolean"
  },
  {
    "Action": "ReconnectWifi",
    "ValType": "None"
  },
  {
    "Action": "ScanWifi",
    "ValType": "None"
  },
  {
    "Action": "SetWifiApMode",
    "ValType": "Boolean"
  }
]
```


## Actions — nodes

_Status: 200_

**Node 1:**

| Action | ValType | Enum options |
|---|---|---|
| SetVentilationState | Enum | AUTO, AUT1, AUT2, AUT3, MAN1, MAN2, MAN3, EMPT, CNT1, CNT2, CNT3, MAN1x2, MAN2x2, MAN3x2, MAN1x3, MAN2x3, MAN3x3 |
| SetIdentify | Boolean |  |

**Node 2:**

| Action | ValType | Enum options |
|---|---|---|
| SetVentilationState | Enum | AUTO, AUT1, AUT2, AUT3, MAN1, MAN2, MAN3, EMPT, CNT1, CNT2, CNT3, MAN1x2, MAN2x2, MAN3x2, MAN1x3, MAN2x3, MAN3x3 |
| SetIdentify | Boolean |  |

**Node 113:**

| Action | ValType | Enum options |
|---|---|---|
| SetVentilationState | Enum | AUTO, AUT1, AUT2, AUT3, MAN1, MAN2, MAN3, EMPT, CNT1, CNT2, CNT3, MAN1x2, MAN2x2, MAN3x2, MAN1x3, MAN2x3, MAN3x3 |

```json
{
  "Nodes": [
    {
      "Node": 1,
      "Actions": [
        {
          "Action": "SetVentilationState",
          "ValType": "Enum",
          "Enum": [
            "AUTO",
            "AUT1",
            "AUT2",
            "AUT3",
            "MAN1",
            "MAN2",
            "MAN3",
            "EMPT",
            "CNT1",
            "CNT2",
            "CNT3",
            "MAN1x2",
            "MAN2x2",
            "MAN3x2",
            "MAN1x3",
            "MAN2x3",
            "MAN3x3"
          ]
        },
        {
          "Action": "SetIdentify",
          "ValType": "Boolean"
        }
      ]
    },
    {
      "Node": 2,
      "Actions": [
        {
          "Action": "SetVentilationState",
          "ValType": "Enum",
          "Enum": [
            "AUTO",
            "AUT1",
            "AUT2",
            "AUT3",
            "MAN1",
            "MAN2",
            "MAN3",
            "EMPT",
            "CNT1",
            "CNT2",
            "CNT3",
            "MAN1x2",
            "MAN2x2",
            "MAN3x2",
            "MAN1x3",
            "MAN2x3",
            "MAN3x3"
          ]
        },
        {
          "Action": "SetIdentify",
          "ValType": "Boolean"
        }
      ]
    },
    {
      "Node": 113,
      "Actions": [
        {
          "Action": "SetVentilationState",
          "ValType": "Enum",
          "Enum": [
            "AUTO",
            "AUT1",
            "AUT2",
            "AUT3",
            "MAN1",
            "MAN2",
            "MAN3",
            "EMPT",
            "CNT1",
            "CNT2",
            "CNT3",
            "MAN1x2",
            "MAN2x2",
            "MAN3x2",
            "MAN1x3",
            "MAN2x3",
            "MAN3x3"
          ]
        }
      ]
    }
  ]
}
```
