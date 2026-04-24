"""SSL context helper for the Duco API client."""

from __future__ import annotations

import importlib.resources
import ssl


def build_ssl_context() -> ssl.SSLContext:
    """Return an SSL context that trusts the Duco CA bundle.

    The Duco device uses a self-signed certificate chain issued by the
    Duco Root Certificate Authority.  This context loads the bundled CA
    chain (ServerDeviceCert, Duco Intermediate COM CA, Duco Root CA) so
    the connection is verified without disabling SSL entirely.

    Hostname verification is disabled because device certificates have the
    factory-default IP (192.168.4.1) in their SAN, which does not match
    the actual IP address assigned by the user's router.
    """
    ctx = ssl.create_default_context()
    cert_path = importlib.resources.files("duco.certs").joinpath("duco_ca.pem")
    with importlib.resources.as_file(cert_path) as path:
        ctx.load_verify_locations(cafile=path)
    ctx.check_hostname = False
    return ctx
