import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from trend_buddy_shared.contracts.health import HealthResponse
from trend_buddy_shared.config.env import getenv


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path not in {"/health", "/api/v1/health"}:
            self.send_response(404)
            self.end_headers()
            return

        payload = HealthResponse(
            service="portfolio-analytics",
            status="ok",
            details={"runtime": "python", "role": "portfolio-metrics"},
        )
        body = json.dumps(payload.__dict__).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    port = int(getenv("PORTFOLIO_ANALYTICS_PORT", "8092"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
