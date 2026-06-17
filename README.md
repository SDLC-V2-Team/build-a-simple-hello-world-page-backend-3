# Hello World — Static HTTP Server

A minimal web application that displays **Hello World**. It serves a static
HTML page using Python's built-in [`http.server`](https://docs.python.org/3/library/http.server.html)
module — **zero external runtime dependencies**.

> Implements **ADR-001**: "Serve Hello World Page via Static HTML and Python
> Built-in HTTP Server".

## Architecture

| Component | Role |
|-----------|------|
| **Static HTTP Server** (`server.py`) | Serves `index.html` (`Hello World`) over HTTP using the Python standard library. |
| **Web Browser** (client) | Requests and renders the Hello World page. |

## Requirements

- Python 3.10+ (standard library only)
- `pytest` for running tests (dev only)

## Quick start

```bash
# Run the server (defaults to 0.0.0.0:8000)
python server.py

# Then open in your browser:
#   http://localhost:8000
```

Customise host/port via flags or environment variables:

```bash
python server.py --host 127.0.0.1 --port 9000
# or
HOST=127.0.0.1 PORT=9000 python server.py
```

## Project layout

```
.
├── index.html              # The Hello World page
├── style.css               # Page styling
├── server.py               # HTTP server entry point
├── requirements.txt        # Dev/test dependencies (no runtime deps)
├── Dockerfile              # Container image
├── tests/
│   └── test_server.py      # Integration tests
└── .github/workflows/ci.yml
```

## Running tests

```bash
pip install -r requirements.txt
pytest -v
```

## Docker

```bash
docker build -t hello-world-server .
docker run --rm -p 8000:8000 hello-world-server
# open http://localhost:8000
```

## Notes & trade-offs

- ✅ Zero external dependencies, minimal setup, easily testable.
- ⚠️ Static content only — dynamic behaviour would require additional code
  (see ADR-001 negative consequences).
