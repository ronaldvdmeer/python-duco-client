"""Tests for SSL context behaviour in DucoClient."""

from __future__ import annotations

import ssl
import time
from unittest.mock import MagicMock, patch

import aiohttp
from aioresponses import aioresponses

from duco._ssl import build_ssl_context
from duco.client import DucoClient

_PRELOADED_API_KEY = "test-api-key-preloaded-for-unit-tests"


# ---------------------------------------------------------------------------
# build_ssl_context
# ---------------------------------------------------------------------------


def test_build_ssl_context_returns_ssl_context():
    ctx = build_ssl_context()
    assert isinstance(ctx, ssl.SSLContext)


def test_build_ssl_context_hostname_check_disabled():
    ctx = build_ssl_context()
    assert ctx.check_hostname is False


def test_build_ssl_context_cert_verification_enabled():
    ctx = build_ssl_context()
    assert ctx.verify_mode == ssl.CERT_REQUIRED


def test_build_ssl_context_loads_duco_ca():
    # Loading the context must not raise — the bundled PEM is valid.
    ctx = build_ssl_context()
    assert ctx is not None


# ---------------------------------------------------------------------------
# DucoClient SSL wiring
# ---------------------------------------------------------------------------


def test_client_http_has_no_ssl_context():
    session = MagicMock(spec=aiohttp.ClientSession)
    client = DucoClient(session=session, host="192.168.3.94", scheme="http")
    assert client._ssl_context is None


def test_client_https_has_ssl_context():
    session = MagicMock(spec=aiohttp.ClientSession)
    client = DucoClient(session=session, host="192.168.3.94", scheme="https")
    assert isinstance(client._ssl_context, ssl.SSLContext)


def test_client_default_scheme_has_no_ssl_context():
    session = MagicMock(spec=aiohttp.ClientSession)
    client = DucoClient(session=session, host="192.168.3.94")
    assert client._ssl_context is None


# ---------------------------------------------------------------------------
# _request passes ssl kwarg to the underlying session
# ---------------------------------------------------------------------------


async def test_request_passes_ssl_true_for_http(api_info_data):
    async with aiohttp.ClientSession() as session:
        client = DucoClient(session=session, host="192.168.3.94", scheme="http")
        client._api_key = _PRELOADED_API_KEY
        client._api_key_day = int(time.time()) // 86400

        with aioresponses() as m:
            m.get("http://192.168.3.94/api", payload=api_info_data)
            with patch.object(session, "request", wraps=session.request) as mock_req:
                await client.async_get_api_info()
                _, kwargs = mock_req.call_args
                assert kwargs.get("ssl") is True


async def test_request_passes_ssl_context_for_https(api_info_data):
    async with aiohttp.ClientSession() as session:
        with patch("duco.client.build_ssl_context") as mock_build:
            fake_ctx = MagicMock(spec=ssl.SSLContext)
            mock_build.return_value = fake_ctx

            client = DucoClient(session=session, host="192.168.3.94", scheme="https")
            client._api_key = _PRELOADED_API_KEY
            client._api_key_day = int(time.time()) // 86400

            with aioresponses() as m:
                m.get("https://192.168.3.94/api", payload=api_info_data)
                with patch.object(session, "request", wraps=session.request) as mock_req:
                    await client.async_get_api_info()
                    _, kwargs = mock_req.call_args
                    assert kwargs.get("ssl") is fake_ctx
