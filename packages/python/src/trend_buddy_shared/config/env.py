import os


def getenv(name: str, default: str) -> str:
    return os.getenv(name, default)


def service_url(env_var: str, service_name: str, default_port: int) -> str:
    return os.getenv(env_var, f"http://{service_name}:{default_port}")
