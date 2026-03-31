import os


def getenv(name: str, default: str) -> str:
    return os.getenv(name, default)
