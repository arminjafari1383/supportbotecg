from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Eco Smart Bot Running")

def run_health():
    server = HTTPServer(("0.0.0.0", 9000), Handler)
    server.serve_forever()

threading.Thread(target=run_health, daemon=True).start()
