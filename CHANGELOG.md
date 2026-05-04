# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-05-04

### Added

- Expose typed API metadata via `ApiEndpointInfo` and the expanded `ApiInfo`
  model. `/api` responses now include `public_api_version`, optional
  `reported_api_version`, and typed endpoint inventory data.

### Enhanced

- Extend `BoardInfo` with optional `public_api_version` and `software_version`
  fields.
- Parse optional version metadata defensively so older and newer firmware
  variants remain compatible.
- Expand unit and focused live integration coverage for API and board metadata.
- Update the published package description so PyPI includes both `README.md`
  and `CHANGELOG.md`.

## [0.3.10] - 2026-05-03

### Fixed

- `_ensure_api_key`: `DucoConnectionError` is no longer wrapped as
  `DucoAuthenticationError`. Previously, a connection failure during API key
  generation was caught by the generic `except DucoError` handler and re-raised
  as `DucoAuthenticationError`, bypassing callers that correctly handle
  `DucoConnectionError`. The exception is now re-raised unchanged; only genuine
  API failures are wrapped as `DucoAuthenticationError`.

### Enhanced

- Fixed ruff code quality warnings across `src/` and `tests/`: sorted `__all__`
  (RUF022), removed unused `noqa` directive (RUF100), combined `elif` branches
  (SIM114), replaced EN dashes with hyphens in docstrings/comments (RUF002,
  RUF003), used `next(iter(...))` instead of list slice (RUF015), combined
  nested `with` statements (SIM117).
- Fixed ruff docstring style (D413, COM812) across `src/duco/`. Added
  per-file-ignore for T201 in `cli.py` — `print()` is intentional CLI output.

## [0.3.9] - 2026-04-26

### Added

- `build_ssl_context()` is now part of the public API (exported from `duco`).
- `DucoClient.__init__` accepts an optional `ssl_context` parameter.  When
  provided the caller controls when the context is built (e.g. in an executor
  so blocking I/O stays off the asyncio event loop).  When omitted the
  behaviour is identical to previous releases.
- `build_ssl_context()` now caches its result so repeated calls are free of
  blocking I/O.

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

[0.4.0]: https://github.com/ronaldvdmeer/python-duco-client/compare/v0.3.10...v0.4.0
[0.3.8]: https://github.com/ronaldvdmeer/python-duco-client/compare/v0.3.7...v0.3.8
[0.3.7]: https://github.com/ronaldvdmeer/python-duco-client/compare/v0.3.6...v0.3.7
[0.3.6]: https://github.com/ronaldvdmeer/python-duco-client/compare/v0.3.5...v0.3.6
[0.3.5]: https://github.com/ronaldvdmeer/python-duco-client/releases/tag/v0.3.5
