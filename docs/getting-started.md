## Development workflow

The tracked base configuration lives in `config/dev.env`.

Developer-specific overrides can be added in `config/.env.local` by copying `config/.env.local.example`.

Generate the shared env file from the tracked base env and local overrides:
```bash
make generate-env
```

Start the default local stack with Docker Compose:
```bash
make up
```

Stop the local stack:
```bash
make down
```

Tail service logs:
```bash
make logs
```

Show running containers:
```bash
make ps
```

Build service images:
```bash
make build-images
```

Run Go tests:
```bash
make test-go
```

Run Python tests with `uv`:
```bash
make test-python
```

Validate the compose integration wiring:
```bash
make test-integration
```
