"""Tests for server.py – static Hello World HTTP server."""
from __future__ import annotations

import os
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from unittest.mock import patch

import pytest

import server
from server import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    PUBLIC_DIR,
    HelloWorldRequestHandler,
    build_server,
    parse_args,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _free_port() -> int:
    """Return an ephemeral free port on localhost."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestBuildServer:
    def test_returns_threading_http_server(self):
        """build_server returns a ThreadingHTTPServer instance."""
        port = _free_port()
        httpd = build_server("127.0.0.1", port)
        try:
            assert isinstance(httpd, ThreadingHTTPServer)
        finally:
            httpd.server_close()

    def test_custom_host_and_port(self):
        """build_server binds to the supplied host and port."""
        port = _free_port()
        httpd = build_server("127.0.0.1", port)
        try:
            assert httpd.server_address == ("127.0.0.1", port)
        finally:
            httpd.server_close()


class TestHandlerServesIndex:
    def test_root_path_returns_200(self, tmp_path):
        """GET / returns HTTP 200 when index.html exists in the served directory."""
        # Create a minimal index.html in a temp dir so the handler can find it.
        index = tmp_path / "index.html"
        index.write_text("<html><body>Hello World</body></html>")

        from functools import partial

        port = _free_port()
        handler = partial(HelloWorldRequestHandler, directory=str(tmp_path))
        httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            response = urllib.request.urlopen(f"http://127.0.0.1:{port}/")
            assert response.status == 200
            body = response.read().decode()
            assert "Hello World" in body
        finally:
            httpd.shutdown()
            httpd.server_close()


class TestParseArgs:
    def test_defaults(self):
        """parse_args with no arguments returns built-in defaults."""
        # Clear any interfering env vars.
        env = {k: v for k, v in os.environ.items() if k not in ("HOST", "PORT")}
        with patch.dict(os.environ, env, clear=True):
            args = parse_args([])
        assert args.host == DEFAULT_HOST
        assert args.port == DEFAULT_PORT

    def test_explicit_host_and_port(self):
        """parse_args honours --host and --port flags."""
        args = parse_args(["--host", "127.0.0.1", "--port", "9090"])
        assert args.host == "127.0.0.1"
        assert args.port == 9090

    def test_env_var_overrides(self):
        """parse_args picks up HOST and PORT from environment variables."""
        with patch.dict(os.environ, {"HOST": "192.168.1.1", "PORT": "7777"}):
            args = parse_args([])
        assert args.host == "192.168.1.1"
        assert args.port == 7777


class TestParseArgsErrorPath:
    def test_non_integer_port_raises_system_exit(self):
        """parse_args raises SystemExit when --port is not an integer."""
        with pytest.raises(SystemExit):
            parse_args(["--port", "not_a_number"])


class TestPublicDir:
    def test_public_dir_is_absolute(self):
        """PUBLIC_DIR is an absolute path."""
        assert os.path.isabs(PUBLIC_DIR)