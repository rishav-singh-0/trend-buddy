COMPOSE_CMD := $(shell if docker compose version >/dev/null 2>&1; then echo "docker compose"; else echo "docker-compose"; fi)
COMPOSE_FILES := -f docker-compose.yml -f infra/compose/dev.yml
ENV_FILE := config/generated/dev.env
UV_CACHE_DIR ?= /tmp/trend-buddy-uv-cache
GOCACHE ?= /tmp/trend-buddy-go-build

all: test-go test-python

run: up logs

generate-env:
	@UV_CACHE_DIR=$(UV_CACHE_DIR) uv run --no-project python tools/scripts/generate_env.py

up: generate-env
	@$(COMPOSE_CMD) $(COMPOSE_FILES) up --build -d

down:
	@$(COMPOSE_CMD) $(COMPOSE_FILES) down

logs:
	@$(COMPOSE_CMD) $(COMPOSE_FILES) logs -f

ps:
	@$(COMPOSE_CMD) $(COMPOSE_FILES) ps

build-images: generate-env
	@$(COMPOSE_CMD) $(COMPOSE_FILES) build

test-go:
	@GOCACHE=$(GOCACHE) go test ./...

test-python:
	@PYTHONPATH=packages/python/src UV_CACHE_DIR=$(UV_CACHE_DIR) uv run --no-project python -m unittest discover packages/python/tests
	@PYTHONPATH=packages/python/src:services/backtesting/src UV_CACHE_DIR=$(UV_CACHE_DIR) uv run --no-project python -m unittest discover services/backtesting/tests
	@PYTHONPATH=packages/python/src:services/strategy-engine/src UV_CACHE_DIR=$(UV_CACHE_DIR) uv run --no-project python -m unittest discover services/strategy-engine/tests
	@PYTHONPATH=packages/python/src:services/portfolio-analytics/src UV_CACHE_DIR=$(UV_CACHE_DIR) uv run --no-project python -m unittest discover services/portfolio-analytics/tests

test-integration: generate-env
	@$(COMPOSE_CMD) $(COMPOSE_FILES) config >/dev/null

clean:
	@rm -f $(ENV_FILE)

.PHONY: all run generate-env up down logs ps build-images test-go test-python test-integration clean
