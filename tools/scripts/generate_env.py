from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE_ENV_PATH = ROOT / "config" / "dev.env"
LOCAL_ENV_PATH = ROOT / "config" / ".env.local"
OUTPUT_PATH = ROOT / "config" / "generated" / "dev.env"

SERVICE_ENDPOINTS = {
    "API_GATEWAY": ("api-gateway", "API_GATEWAY_PORT", 8080),
    "DATABASE_SERVICE": ("database-service", "DATABASE_SERVICE_PORT", 8083),
    "DATA_INGESTION": ("data-ingestion", "DATA_INGESTION_PORT", 8084),
    "BROKER_GATEWAY": ("broker-gateway", "BROKER_GATEWAY_PORT", 8085),
    "INDICATOR_ENGINE": ("indicator-engine", "INDICATOR_ENGINE_PORT", 8086),
    "LIVE_RUNNER": ("live-runner", "LIVE_RUNNER_PORT", 8087),
    "BACKTESTING": ("backtesting", "BACKTESTING_PORT", 8090),
    "STRATEGY_ENGINE": ("strategy-engine", "STRATEGY_ENGINE_PORT", 8091),
    "PORTFOLIO_ANALYTICS": ("portfolio-analytics", "PORTFOLIO_ANALYTICS_PORT", 8092),
    "FRONTEND": ("web", "FRONTEND_PORT", 5173),
}


def parse_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    pairs: dict[str, str] = {}
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        pairs[key.strip()] = value.strip()
    return pairs


def main() -> None:
    env = parse_env_file(BASE_ENV_PATH)
    env.update(parse_env_file(LOCAL_ENV_PATH))

    for prefix, (service_name, port_key, default_port) in SERVICE_ENDPOINTS.items():
        env.setdefault(f"{prefix}_URL", f"http://{service_name}:{env.get(port_key, default_port)}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{key}={value}" for key, value in sorted(env.items())]
    OUTPUT_PATH.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
