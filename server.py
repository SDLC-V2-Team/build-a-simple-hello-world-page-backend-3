"""Static HTTP Server.

Serves the static Hello World page using Python's built-in http.server module,
as decided in ADR-001. Zero external dependencies (Python standard library only).
"""
from __future__ import annotations

import argparse
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# Directory containing the static assets (this file's directory).
PUBLIC_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000


class HelloWorldRequestHandler(SimpleHTTPRequestHandler):
    """Request handler that serves files from the project directory.

    The root path ("/") maps to index.html via SimpleHTTPRequestHandler's
    default behaviour, which renders the simple Hello World page (ADR-001).
    No additional routing is required; the existing static-serving behaviour
    fully satisfies the 'display hello world' requirement.
    """

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        # Keep concise, structured-ish logging.
        print(f"[server] {self.address_string()} - {fmt % args}")


def build_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    """Create (but do not start) the HTTP server."""
    handler = partial(HelloWorldRequestHandler, directory=PUBLIC_DIR)
    return ThreadingHTTPServer((host, port), handler)


def run(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """Start the HTTP server and serve forever."""
    httpd = build_server(host, port)
    print(f"Serving Hello World on http://{host}:{port} (Ctrl+C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        httpd.server_close()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve the static Hello World page.")
    parser.add_argument("--host", default=os.environ.get("HOST", DEFAULT_HOST))
    parser.add_argument(
        "--port", type=int, default=int(os.environ.get("PORT", DEFAULT_PORT))
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    run(args.host, args.port)
