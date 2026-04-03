#!/usr/bin/env python3
"""Local server that serves the dashboard and proxies FRED API requests to avoid CORS."""

import http.server
import urllib.request
import urllib.error
import json
import os

PORT = 8000

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/fred-proxy?"):
            self.proxy_fred()
        else:
            super().do_GET()

    def proxy_fred(self):
        query = self.path.split("?", 1)[1]
        url = f"https://api.stlouisfed.org/fred/series/observations?{query}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with http.server.HTTPServer(("", PORT), DashboardHandler) as httpd:
        print(f"Dashboard running at http://localhost:{PORT}/global_economics_dashboard.html")
        httpd.serve_forever()
