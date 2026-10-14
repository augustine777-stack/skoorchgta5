import os
import sys
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Monkey-patch serve_local before import
PORT = int(os.environ.get("PORT", 10000))
HOST = "0.0.0.0"

# Try to import and override server config
try:
    import serve_local
    # Common patterns to override
    if hasattr(serve_local, 'HOST'):
        serve_local.HOST = HOST
    if hasattr(serve_local, 'PORT'):
        serve_local.PORT = PORT
    if hasattr(serve_local, 'server_address'):
        serve_local.server_address = (HOST, PORT)
    serve_local.main()
except Exception as e:
    print(f"[FALLBACK] Could not patch serve_local: {e}")
    print(f"[FALLBACK] Starting basic server on {HOST}:{PORT}")
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer((HOST, PORT), handler)
    print(f"Serving on http://{HOST}:{PORT}")
    httpd.serve_forever()
