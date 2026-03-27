from apps.api.main import app


def main() -> None:
    print(
        "Run the API with: "
        "uv run --with uvicorn uvicorn main:app --reload --host 0.0.0.0 --port 3000"
    )


if __name__ == "__main__":
    main()
