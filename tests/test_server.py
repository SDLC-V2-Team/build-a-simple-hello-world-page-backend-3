"""Tests for server.py — static Hello World HTTP server."""
from __future__ import annotations

import os
import pytest
from http.server import ThreadingHTTPServer
from unittest.mock import patch

from server import (
    HelloWorldRequestHandler,
    build_server,
    parse_args,
    PUBLIC_DIR,
    DEFAULT_HOST,
    DEFAULT_PORT,
)


def test_default_constants():
    """DEFAULT_HOST and DEFAULT_PORT should have expected values."""
    assert DEFAULT_HOST == "0.0.0.0"
    assert DEFAULT_PORT == 8000


def test_public_dir_exists():
    """PUBLIC_DIR must point to an existing directory (the project root)."""
    assert os.path.isdir(PUBLIC_DIR)


def test_build_server_returns_threading_http_server():
    """build_server should return a ThreadingHTTPServer bound to host/port."""
    server = build_server("127.0.0.1", 0)  # port 0 → OS picks a free port
    try:
        assert isinstance(server, ThreadingHTTPServer)
        host, port = server.server_address
        assert host == "127.0.0.1"
        assert port > 0
    finally:
        server.server_close()


def test_parse_args_defaults():
    """parse_args with no arguments should return DEFAULT_HOST and DEFAULT_PORT."""
    # Make sure env vars don't interfere
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("HOST", None)
        os.environ.pop("PORT", None)
        args = parse_args([])
    assert args.host == DEFAULT_HOST
    assert args.port == DEFAULT_PORT


def test_parse_args_custom_host_and_port():
    """parse_args should honour explicit --host and --port flags."""
    args = parse_args(["--host", "127.0.0.1", "--port", "9090"])
    assert args.host == "127.0.0.1"
    assert args.port == 9090


def test_parse_args_invalid_port_raises_system_exit():
    """parse_args should raise SystemExit when --port is not an integer."""
    with pytest.raises(SystemExit):
        parse_args(["--port", "not_a_number"])