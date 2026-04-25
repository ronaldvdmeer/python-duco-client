# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.8] - 2026-04-26

### Changed

- `DucoClient.__init__`: default `scheme` changed from `"http"` to `"https"`.
  All Duco Connectivity Board 2.0 boxes use HTTPS, and since v0.3.7 the client
  automatically constructs a valid SSL context using the bundled Duco CA
  certificate chain. Callers that need plain HTTP must now pass `scheme="http"`
  explicitly.

### Breaking change

Code that instantiates `DucoClient` without a `scheme=` argument and expects
HTTP behaviour must now pass `scheme="http"` explicitly.

## [0.3.7] - 2026-04-25

### Added

- Bundle the Duco device CA certificate chain so HTTPS connections are verified
  without requiring `verify_ssl=False` in callers. The bundled chain contains
  ServerDeviceCert + Duco Intermediate COM CA + Duco Root CA.
- `build_ssl_context()` helper in `duco._ssl` builds a ready-to-use
  `ssl.SSLContext` with certificate verification enabled and hostname
  verification disabled (device cert SAN contains factory IP `192.168.4.1`,
  not the user-assigned IP).
- `DucoClient` automatically uses the SSL context for HTTPS connections and
  passes `ssl=True` (default behaviour) for plain HTTP connections.
- CLI: add `--https` flag (and `DUCO_HTTPS=1` env var) to select HTTPS; add
  `temp` and `RH` columns to `nodes` output; require `--host` (removed
  hardcoded default IP).

### Fixed

- Fix missing `if __name__ == "__main__":` guard in `cli.py`.

### Internal

- Add `tests/test_ssl.py` with 7 unit tests covering SSL context construction
  and wiring in `DucoClient`.

## [0.3.6] - 2026-04-25

### Added

- Add temperature reading support for room nodes (`NodeTemperatureData`).
- New `DucoClient.get_node_temperature()` method.

## [0.3.5] - 2026-04-21

### Added

- Initial release with basic node info retrieval and action control.

[0.3.8]: https://github.com/ronaldvdmeer/python-duco-client/compare/v0.3.7...v0.3.8
[0.3.7]: https://github.com/ronaldvdmeer/python-duco-client/compare/v0.3.6...v0.3.7
[0.3.6]: https://github.com/ronaldvdmeer/python-duco-client/compare/v0.3.5...v0.3.6
[0.3.5]: https://github.com/ronaldvdmeer/python-duco-client/releases/tag/v0.3.5
