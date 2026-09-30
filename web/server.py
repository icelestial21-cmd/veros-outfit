import http.server
import socketserver
import os

PORT = 8090
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

class ThreadingServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == '__main__':
    with ThreadingServer(("", PORT), Handler) as httpd:
        print(f"Marko Baku Digital Flagship serving at http://localhost:{PORT}")
        httpd.serve_forever()
