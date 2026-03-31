from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE_ENV_PATH = ROOT / "config" / "dev.env"
LOCAL_ENV_PATH = ROOT / "config" / ".env.local"
OUTPUT_PATH = ROOT / "config" / "generated" / "dev.env"


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

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{key}={value}" for key, value in sorted(env.items())]
    OUTPUT_PATH.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
