# Duco Silent Connect API Documentatie

> **Reverse-engineered** API documentatie voor de Duco Silent Connect mechanische ventilatie box.
>
> - **API Versie:** 2.5
> - **Base URL:** `http://<ip-adres>`
> - **Box Type:** SILENT_CONNECT (Eu)

---

## Inhoudsopgave

- [Overzicht](#overzicht)
- [Algemene Conventies](#algemene-conventies)
- [Endpoints](#endpoints)
  - [GET /api](#get-api)
  - [GET /info](#get-info)
  - [GET /info/nodes](#get-infonodes)
  - [GET /info/nodes/{node}](#get-infonodesnode)
  - [GET /info/zones](#get-infozones)
  - [GET /info/zones/{zone}](#get-infozoneszone)
  - [GET /info/zones/{zone}/groups/{group}](#get-infozoneszonegroup)
  - [GET /nodes](#get-nodes)
  - [GET /config](#get-config)
  - [GET /config/nodes](#get-confignodes)
  - [GET /config/nodes/{node}](#get-confignodesnode)
  - [GET /config/zones](#get-configzones)
  - [GET /config/zones/{zone}](#get-configzoneszone)
  - [GET /config/zones/{zone}/groups/{group}](#get-configzoneszonegroup)
  - [GET /action](#get-action)
  - [POST /action](#post-action)
  - [GET /action/nodes](#get-actionnodes)
  - [GET /action/nodes/{node}](#get-actionnodesnode)
  - [POST /action/nodes/{node}](#post-actionnodesnode)
- [Datamodellen](#datamodellen)
- [Ventilatie States](#ventilatie-states)
- [Node Types](#node-types)
- [Foutcodes](#foutcodes)

---

## Overzicht

De Duco Silent Connect biedt een lokale REST API op het netwerk waarmee je:

- **Informatie** kunt uitlezen over de box, nodes (sensoren/kleppen) en zones
- **Configuratie** kunt lezen en aanpassen
- **Acties** kunt uitvoeren zoals ventilatiestand wijzigen en WiFi-beheer

## Algemene Conventies

### Waarden

Alle waarden worden gewrapped in een `Val` object:

```json
{
  "BoxName": {
    "Val": "SILENT_CONNECT"
  }
}
```

### Configuratiewaarden

Configureerbare parameters bevatten extra velden voor validatie:

```json
{
  "TimeZone": {
    "Val": 1,
    "Min": -11,
    "Inc": 1,
    "Max": 12
  }
}
```

| Veld  | Beschrijving                      |
|-------|-----------------------------------|
| `Val` | Huidige waarde                    |
| `Min` | Minimaal toegestane waarde        |
| `Max` | Maximaal toegestane waarde        |
| `Inc` | Stapgrootte (increment)           |

### Query Parameters

De meeste endpoints ondersteunen filtering via query parameters:

| Parameter    | Beschrijving                                                   |
|-------------|----------------------------------------------------------------|
| `module`    | Filter op module (bijv. `General`, `Sensor`, `Ventilation`)    |
| `submodule` | Filter op submodule (bijv. `Board`, `Lan`)                     |
| `parameter` | Filter op specifieke parameter (bijv. `BoxName`, `Co2`)        |
| `from`      | Paginatie startpunt voor lijsten                               |
| `zone`      | Filter op zone ID                                              |
| `group`     | Filter op groep ID                                             |

**Voorbeeld:** Alleen de CO2-waarde ophalen:
```
GET /info/nodes/2?module=Sensor&parameter=Co2
```

### Foutresponse

Bij fouten retourneert de API een JSON response met HTTP-foutcode:

```json
{
  "Code": 3,
  "Result": "FAILED"
}
```

### Rate Limiting

De API houdt een teller bij van resterende schrijfverzoeken:

- **PublicApi schrijflimiet:** zichtbaar via `/info` → `General.PublicApi.WriteReqCntRemain`
- **Modbus schrijflimiet:** zichtbaar via `/info` → `General.Modbus.WriteReqCntRemain`

---

## Endpoints

### GET /api

Retourneert de API-versie en een lijst van alle beschikbare endpoints met hun methoden, query parameters en modules.

**Response:**

```json
{
  "PublicApiVersion": {
    "Val": "2.5"
  },
  "ApiInfo": [
    {
      "Url": "/info",
      "QueryParameters": ["module", "submodule", "parameter"],
      "Methods": ["GET"],
      "Modules": ["General", "Diag", "Ventilation", "WeatherHandler"]
    }
  ]
}
```

---

### GET /info

Retourneert uitgebreide informatie over de box zelf.

**Query Parameters:** `module`, `submodule`, `parameter`

**Beschikbare Modules:** `General`, `Diag`, `Ventilation`, `WeatherHandler`

**Response (volledig):**

```json
{
  "General": {
    "Board": {
      "PublicApiVersion": { "Val": "2.5" },
      "BoxName": { "Val": "SILENT_CONNECT" },
      "BoxSubTypeName": { "Val": "Eu" },
      "SerialBoardBox": { "Val": "RS2420002577" },
      "SerialBoardComm": { "Val": "PS2424005629" },
      "SerialDucoBox": { "Val": "n/a" },
      "SerialDucoComm": { "Val": "P369348-241126-033" },
      "Time": { "Val": 1775082497 }
    },
    "Lan": {
      "Mode": { "Val": "WIFI_CLIENT" },
      "Ip": { "Val": "192.168.3.94" },
      "NetMask": { "Val": "255.255.255.0" },
      "DefaultGateway": { "Val": "192.168.3.1" },
      "Dns": { "Val": "192.168.3.1" },
      "Mac": { "Val": "a0:dd:6c:06:12:90" },
      "HostName": { "Val": "duco_061293" },
      "DucoClientIp": { "Val": "0.0.0.0" },
      "WifiApSsid": { "Val": "DUCO" },
      "WifiApKey": { "Val": "12345678" },
      "RssiWifi": { "Val": -44 },
      "ScanWifi": []
    },
    "PublicApi": {
      "WriteReqCntRemain": { "Val": 170 }
    },
    "Modbus": {
      "WriteReqCntRemain": { "Val": 200 }
    }
  },
  "Diag": {
    "SubSystems": [
      { "Component": "Ventilation", "Status": "Ok" },
      { "Component": "VentCool", "Status": "Ok" },
      { "Component": "SunCtrl", "Status": "Ok" }
    ]
  }
}
```

#### General.Board Parameters

| Parameter          | Type    | Beschrijving                         |
|--------------------|---------|--------------------------------------|
| `PublicApiVersion` | string  | Versie van de publieke API           |
| `BoxName`          | string  | Type naam van de box                 |
| `BoxSubTypeName`   | string  | Subtype (bijv. `Eu` voor Europa)     |
| `SerialBoardBox`   | string  | Serienummer van het box-board        |
| `SerialBoardComm`  | string  | Serienummer van het communicatieboard|
| `SerialDucoBox`    | string  | Duco serienummer box                 |
| `SerialDucoComm`   | string  | Duco serienummer communicatie        |
| `Time`             | integer | Huidige Unix-timestamp               |

#### General.Lan Parameters

| Parameter        | Type    | Beschrijving                              |
|------------------|---------|-------------------------------------------|
| `Mode`           | string  | Netwerkmodus (`WIFI_CLIENT`)              |
| `Ip`             | string  | Huidig IP-adres                           |
| `NetMask`        | string  | Subnetmasker                              |
| `DefaultGateway` | string  | Standaard gateway                         |
| `Dns`            | string  | DNS server                                |
| `Mac`            | string  | MAC-adres                                 |
| `HostName`       | string  | Hostname op het netwerk                   |
| `DucoClientIp`   | string  | IP van Duco client                        |
| `WifiApSsid`     | string  | SSID in access point modus                |
| `WifiApKey`      | string  | Wachtwoord in access point modus          |
| `RssiWifi`       | integer | WiFi signaalsterkte (dBm, neg = sterker)  |
| `ScanWifi`       | array   | Lijst van gescande WiFi-netwerken         |

#### Diag.SubSystems

| Component     | Beschrijving                        |
|---------------|-------------------------------------|
| `Ventilation` | Status van het ventilatiesubsysteem |
| `VentCool`    | Status van de ventilatie-koeling    |
| `SunCtrl`     | Status van de zonwering-sturing     |

---

### GET /info/nodes

Retourneert informatie over alle nodes (box, sensoren, kleppen) in het systeem.

**Query Parameters:** `from`, `module`, `parameter`

**Beschikbare Modules:** `General`, `NetworkDuco`, `Sensor`

**Response:**

```json
{
  "Nodes": [
    {
      "Node": 1,
      "General": {
        "Type": { "Val": "BOX" },
        "SubType": { "Val": 1 },
        "NetworkType": { "Val": "VIRT" },
        "Parent": { "Val": 0 },
        "Asso": { "Val": 0 },
        "Name": { "Val": "" },
        "Identify": { "Val": 0 }
      },
      "Ventilation": {
        "State": { "Val": "CNT1" },
        "TimeStateRemain": { "Val": 0 },
        "TimeStateEnd": { "Val": 0 },
        "Mode": { "Val": "MANU" },
        "FlowLvlTgt": { "Val": 15 }
      }
    },
    {
      "Node": 2,
      "General": {
        "Type": { "Val": "UCCO2" },
        "SubType": { "Val": 0 },
        "NetworkType": { "Val": "RF" },
        "Parent": { "Val": 1 },
        "Asso": { "Val": 1 },
        "Name": { "Val": "" },
        "Identify": { "Val": 0 }
      },
      "Ventilation": {
        "State": { "Val": "CNT1" },
        "TimeStateRemain": { "Val": 0 },
        "TimeStateEnd": { "Val": 0 },
        "Mode": { "Val": "-" }
      },
      "Sensor": {
        "Co2": { "Val": 536 },
        "IaqCo2": { "Val": 100 }
      }
    },
    {
      "Node": 113,
      "General": {
        "Type": { "Val": "BSRH" },
        "SubType": { "Val": 0 },
        "NetworkType": { "Val": "VIRT" },
        "Parent": { "Val": 1 },
        "Asso": { "Val": 1 },
        "Name": { "Val": "" },
        "Identify": { "Val": 0 }
      },
      "Ventilation": {
        "State": { "Val": "CNT1" },
        "TimeStateRemain": { "Val": 0 },
        "TimeStateEnd": { "Val": 0 },
        "Mode": { "Val": "-" }
      }
    }
  ]
}
```

#### Node General Parameters

| Parameter     | Type    | Beschrijving                                               |
|---------------|---------|------------------------------------------------------------|
| `Type`        | string  | Type node (zie [Node Types](#node-types))                  |
| `SubType`     | integer | Subtype van de node                                        |
| `NetworkType` | string  | Verbindingstype: `VIRT` (virtueel/intern), `RF` (draadloos)|
| `Parent`      | integer | Node ID van de parent (0 = geen parent)                    |
| `Asso`        | integer | Geassocieerde node ID (0 = geen associatie)                |
| `Name`        | string  | Gebruikersnaam van de node                                 |
| `Identify`    | integer | Identificatiemodus (0 = uit, 1 = aan)                      |

#### Node Ventilation Parameters

| Parameter         | Type    | Beschrijving                                                |
|-------------------|---------|-------------------------------------------------------------|
| `State`           | string  | Huidige ventilatiestand (zie [Ventilatie States](#ventilatie-states)) |
| `TimeStateRemain` | integer | Resterende tijd in huidige state (seconden)                 |
| `TimeStateEnd`    | integer | Eindtijd van huidige state (Unix timestamp, 0 = permanent) |
| `Mode`            | string  | Modus: `MANU` (handmatig), `AUTO`, `-` (volgt parent)      |
| `FlowLvlTgt`      | integer | Doelluchtstroom niveau (alleen bij BOX node)                |

#### Node Sensor Parameters

| Parameter | Type    | Beschrijving                                          |
|-----------|---------|-------------------------------------------------------|
| `Co2`     | integer | CO2-concentratie in ppm                               |
| `IaqCo2`  | integer | Indoor Air Quality index op basis van CO2 (0-100 schaal) |

**Voorbeeld: Alleen sensordata ophalen:**
```
GET /info/nodes?module=Sensor
```

```json
{
  "Nodes": [
    {
      "Node": 2,
      "Sensor": {
        "Co2": { "Val": 536 },
        "IaqCo2": { "Val": 100 }
      }
    }
  ]
}
```

> **Let op:** Nodes zonder sensordata worden niet geretourneerd wanneer `module=Sensor`.

---

### GET /info/nodes/{node}

Retourneert informatie over een specifieke node.

**Path Parameters:**

| Parameter | Type    | Beschrijving |
|-----------|---------|-------------|
| `node`    | integer | Node ID     |

**Query Parameters:** `module`, `parameter`

**Beschikbare Modules:** `General`, `NetworkDuco`, `Sensor`

**Voorbeeld:** `GET /info/nodes/2`

---

### GET /info/zones

Retourneert informatie over alle zones en hun groepen.

**Query Parameters:** `from`, `zone`, `group`, `module`, `submodule`, `parameter`

**Beschikbare Modules:** `DeviceGroupConfig`

**Response:**

```json
{
  "Zones": [
    {
      "Zone": 1,
      "DeviceGroupConfig": {
        "General": {
          "Name": { "Val": "VentEtaCentral" }
        }
      },
      "Groups": [
        {
          "Group": 1,
          "DeviceGroupConfig": {
            "General": {
              "Nodes": [2, 113]
            }
          }
        }
      ]
    }
  ]
}
```

#### Zone Parameters

| Parameter                          | Type   | Beschrijving                        |
|------------------------------------|--------|-------------------------------------|
| `DeviceGroupConfig.General.Name`   | string | Naam van de zone                    |

#### Group Parameters

| Parameter                          | Type  | Beschrijving                         |
|------------------------------------|-------|--------------------------------------|
| `DeviceGroupConfig.General.Nodes`  | array | Lijst van node IDs in de groep       |

---

### GET /info/zones/{zone}

Retourneert informatie over een specifieke zone.

**Path Parameters:**

| Parameter | Type    | Beschrijving |
|-----------|---------|-------------|
| `zone`    | integer | Zone ID     |

**Query Parameters:** `group`, `module`, `submodule`, `parameter`

---

### GET /info/zones/{zone}/groups/{group}

Retourneert informatie over een specifieke groep binnen een zone.

**Path Parameters:**

| Parameter | Type    | Beschrijving |
|-----------|---------|-------------|
| `zone`    | integer | Zone ID     |
| `group`   | integer | Groep ID    |

**Query Parameters:** `module`, `submodule`, `parameter`

**Voorbeeld:** `GET /info/zones/1/groups/1`

```json
{
  "Zone": 1,
  "Group": 1,
  "DeviceGroupConfig": {
    "General": {
      "Nodes": [2, 113]
    }
  }
}
```

---

### GET /nodes

Retourneert een simpele lijst van alle beschikbare node IDs.

**Response:**

```json
{
  "value": [
    { "Node": 1 },
    { "Node": 2 },
    { "Node": 113 }
  ],
  "Count": 3
}
```

---

### GET /config

Retourneert de configuratie van de box. Configureerbare waarden bevatten `Min`, `Max` en `Inc` velden.

**Query Parameters:** `module`, `submodule`, `parameter`

**Beschikbare Modules:** `General`

**Response:**

```json
{
  "General": {
    "Time": {
      "TimeZone": { "Val": 1, "Min": -11, "Inc": 1, "Max": 12 },
      "Dst": { "Val": 1, "Min": 0, "Inc": 1, "Max": 1 }
    },
    "Modbus": {
      "Addr": { "Val": 1, "Min": 1, "Inc": 1, "Max": 254 },
      "Offset": { "Val": 1, "Min": 0, "Inc": 1, "Max": 1 }
    },
    "Lan": {
      "Mode": { "Val": 1, "Min": 1, "Inc": 1, "Max": 1 },
      "Dhcp": { "Val": 1, "Min": 0, "Inc": 1, "Max": 1 },
      "StaticIp": { "Val": "0.0.0.0" },
      "StaticNetMask": { "Val": "255.255.255.0" },
      "StaticDefaultGateway": { "Val": "0.0.0.0" },
      "StaticDns": { "Val": "8.8.8.8" },
      "WifiClientSsid": { "Val": "IoT Wi-Fi" },
      "WifiClientKey": { "Val": "" }
    },
    "AutoRebootComm": {
      "Period": { "Val": 7, "Min": 0, "Inc": 1, "Max": 365 },
      "Time": { "Val": 0, "Min": 0, "Inc": 1, "Max": 1439 }
    }
  }
}
```

#### Config Parameters

| Pad                                | Type    | Bereik       | Beschrijving                                   |
|------------------------------------|---------|-------------|------------------------------------------------|
| `General.Time.TimeZone`            | integer | -11 tot 12  | UTC offset in uren                             |
| `General.Time.Dst`                 | boolean | 0-1         | Zomertijd aan/uit                              |
| `General.Modbus.Addr`              | integer | 1-254       | Modbus adres                                   |
| `General.Modbus.Offset`            | boolean | 0-1         | Modbus offset aan/uit                          |
| `General.Lan.Mode`                 | integer | 1-1         | Netwerkmodus                                   |
| `General.Lan.Dhcp`                 | boolean | 0-1         | DHCP aan/uit                                   |
| `General.Lan.StaticIp`             | string  | —           | Statisch IP-adres                              |
| `General.Lan.StaticNetMask`        | string  | —           | Statisch subnetmasker                          |
| `General.Lan.StaticDefaultGateway` | string  | —           | Statische gateway                              |
| `General.Lan.StaticDns`            | string  | —           | Statische DNS server                           |
| `General.Lan.WifiClientSsid`      | string  | —           | SSID van het WiFi-netwerk                      |
| `General.Lan.WifiClientKey`        | string  | —           | Wachtwoord van het WiFi-netwerk                |
| `General.AutoRebootComm.Period`    | integer | 0-365       | Auto-reboot periode in dagen (0 = uitgeschakeld) |
| `General.AutoRebootComm.Time`     | integer | 0-1439      | Tijdstip auto-reboot in minuten vanaf middernacht |

---

### PATCH /config

Wijzig Box-configuratie. Stuur een JSON body met de te wijzigen parameters.

**Request Body (voorbeeld):**

```json
{
  "General": {
    "Time": {
      "TimeZone": 2
    }
  }
}
```

> **Let op:** Er geldt een schrijflimiet. Controleer `WriteReqCntRemain` via `/info`.

---

### GET /config/nodes

Retourneert configuratie van alle nodes.

**Query Parameters:** `from`, `parameter`

**Response:**

```json
{
  "Nodes": [
    { "Node": 1, "Name": { "Val": "" } },
    { "Node": 2, "Name": { "Val": "" } },
    { "Node": 113, "Name": { "Val": "" } }
  ]
}
```

---

### GET /config/nodes/{node}

Retourneert configuratie van een specifieke node.

**Path Parameters:**

| Parameter | Type    | Beschrijving |
|-----------|---------|-------------|
| `node`    | integer | Node ID     |

**Query Parameters:** `parameter`

**Response:**

```json
{
  "Node": 1,
  "Name": { "Val": "" }
}
```

---

### PATCH /config/nodes/{node}

Wijzig configuratie van een specifieke node (bijv. naam instellen).

**Request Body (voorbeeld):**

```json
{
  "Name": "Woonkamer"
}
```

---

### GET /config/zones

Retourneert configuratie van alle zones.

**Query Parameters:** `from`, `zone`, `group`, `module`, `submodule`, `parameter`

**Beschikbare Modules:** `DeviceGroupConfig`

**Response:**

```json
{
  "Zones": [
    {
      "Zone": 1,
      "DeviceGroupConfig": {
        "General": {
          "Name": { "Val": "VentEtaCentral" }
        }
      }
    }
  ]
}
```

---

### GET /config/zones/{zone}

Retourneert configuratie van een specifieke zone.

**Methoden:** `GET`, `PATCH`

---

### PATCH /config/zones/{zone}

Wijzig configuratie van een zone.

---

### GET /config/zones/{zone}/groups/{group}

Retourneert configuratie van een specifieke groep binnen een zone.

**Methoden:** `GET`, `PATCH`

---

### GET /action

Retourneert een lijst van beschikbare globale acties.

**Query Parameters:** `action`

**Response:**

```json
{
  "value": [
    { "Action": "SetTime", "ValType": "Integer" },
    { "Action": "SetIdentify", "ValType": "Boolean" },
    { "Action": "SetIdentifyAll", "ValType": "Boolean" },
    { "Action": "ReconnectWifi", "ValType": "None" },
    { "Action": "ScanWifi", "ValType": "None" },
    { "Action": "SetWifiApMode", "ValType": "Boolean" }
  ],
  "Count": 6
}
```

#### Globale Acties

| Actie             | ValType   | Beschrijving                                       |
|-------------------|-----------|----------------------------------------------------|
| `SetTime`         | Integer   | Stel de systeemtijd in (Unix timestamp)            |
| `SetIdentify`     | Boolean   | Activeer identificatiemodus op de box              |
| `SetIdentifyAll`  | Boolean   | Activeer identificatiemodus op alle apparaten      |
| `ReconnectWifi`   | None      | Herverbind WiFi                                    |
| `ScanWifi`        | None      | Start een WiFi-scan                                |
| `SetWifiApMode`   | Boolean   | Schakel access point modus in/uit                  |

---

### POST /action

Voer een globale actie uit.

**Request Body (voorbeeld):**

```json
{
  "Action": "ScanWifi"
}
```

```json
{
  "Action": "SetTime",
  "Val": 1775082497
}
```

---

### GET /action/nodes

Retourneert beschikbare acties per node.

**Query Parameters:** `from`, `action`

**Response:**

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
            "AUTO", "AUT1", "AUT2", "AUT3",
            "MAN1", "MAN2", "MAN3",
            "EMPT",
            "CNT1", "CNT2", "CNT3",
            "MAN1x2", "MAN2x2", "MAN3x2",
            "MAN1x3", "MAN2x3", "MAN3x3"
          ]
        },
        {
          "Action": "SetIdentify",
          "ValType": "Boolean"
        }
      ]
    }
  ]
}
```

---

### GET /action/nodes/{node}

Retourneert beschikbare acties voor een specifieke node.

**Path Parameters:**

| Parameter | Type    | Beschrijving |
|-----------|---------|-------------|
| `node`    | integer | Node ID     |

---

### POST /action/nodes/{node}

Voer een actie uit op een specifieke node.

**Request Body (voorbeeld — ventilatie op stand 2 zetten):**

```json
{
  "Action": "SetVentilationState",
  "Val": "MAN2"
}
```

**Request Body (voorbeeld — terug naar automatisch):**

```json
{
  "Action": "SetVentilationState",
  "Val": "AUTO"
}
```

---

## Datamodellen

### Apparaat Hiërarchie

```
Box (Node 1, VIRT)
├── CO2 Sensor (Node 2, RF) — Parent: 1, Asso: 1
└── RH Sensor (Node 113, VIRT) — Parent: 1, Asso: 1
```

### Zone Hiërarchie

```
Zone 1: "VentEtaCentral"
└── Group 1
    ├── Node 2 (CO2 Sensor)
    └── Node 113 (RH Sensor)
```

---

## Ventilatie States

| State   | Beschrijving                                      |
|---------|---------------------------------------------------|
| `AUTO`  | Volledig automatisch — sensoren bepalen de stand   |
| `AUT1`  | Automatisch, stand 1 (laag)                        |
| `AUT2`  | Automatisch, stand 2 (middel)                      |
| `AUT3`  | Automatisch, stand 3 (hoog)                        |
| `MAN1`  | Handmatig stand 1 (laag)                           |
| `MAN2`  | Handmatig stand 2 (middel)                         |
| `MAN3`  | Handmatig stand 3 (hoog)                           |
| `EMPT`  | Afwezig / minimale ventilatie                      |
| `CNT1`  | Continu stand 1                                    |
| `CNT2`  | Continu stand 2                                    |
| `CNT3`  | Continu stand 3                                    |
| `MAN1x2`| Handmatig stand 1, duur x2                         |
| `MAN2x2`| Handmatig stand 2, duur x2                         |
| `MAN3x2`| Handmatig stand 3, duur x2                         |
| `MAN1x3`| Handmatig stand 1, duur x3                         |
| `MAN2x3`| Handmatig stand 2, duur x3                         |
| `MAN3x3`| Handmatig stand 3, duur x3                         |

---

## Node Types

| Type    | Beschrijving                                         |
|---------|------------------------------------------------------|
| `BOX`   | De ventilatiebox zelf (hoofdunit)                    |
| `UCCO2` | CO2 sensor (User Control met CO2-meting)             |
| `BSRH`  | Relatieve vochtigheid sensor (Base Station RH)       |

### Network Types

| Type   | Beschrijving                                        |
|--------|-----------------------------------------------------|
| `VIRT` | Virtueel/intern — onderdeel van de box zelf          |
| `RF`   | RF (radio frequency) — draadloos verbonden sensor    |

---

## Foutcodes

| Code | Result   | Beschrijving                                         |
|------|----------|------------------------------------------------------|
| 3    | `FAILED` | Verzoek mislukt (ongeldige module, parameter, etc.)  |

---

## Voorbeelden

### CO2-waarde uitlezen

```bash
curl http://192.168.3.94/info/nodes/2?module=Sensor&parameter=Co2
```

### Ventilatie op handmatig stand 3 zetten

```bash
curl -X POST http://192.168.3.94/action/nodes/1 \
  -H "Content-Type: application/json" \
  -d '{"Action": "SetVentilationState", "Val": "MAN3"}'
```

### Box-informatie ophalen

```bash
curl http://192.168.3.94/info?module=General&submodule=Board
```

### WiFi-scan starten

```bash
curl -X POST http://192.168.3.94/action \
  -H "Content-Type: application/json" \
  -d '{"Action": "ScanWifi"}'
```

### Diagnostiek controleren

```bash
curl http://192.168.3.94/info?module=Diag
```
