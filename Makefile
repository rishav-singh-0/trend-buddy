# Simple Makefile for a Go project

COMPOSE_CMD := $(shell if docker compose version >/dev/null 2>&1; then echo "docker compose"; else echo "docker-compose"; fi)

# Build the application
all: build test

build:
	@echo "Building..."

	@CGO_ENABLED=1 go build -o main cmd/api/main.go

# Build Docker images
docker-build:
	@$(COMPOSE_CMD) build

# Build only the frontend image
frontend-build:
	@$(COMPOSE_CMD) build frontend

# Run the application locally
run:
	@go run cmd/api/main.go &
	@npm install --prefer-offline --no-fund --prefix ./frontend
	@npm run dev --prefix ./frontend

# Start containers
docker-run:
	@$(COMPOSE_CMD) up --build

# Stop containers
docker-down:
	@$(COMPOSE_CMD) down

# Test the application
test:
	@echo "Testing..."
	@go test ./... -v

# Clean the binary
clean:
	@echo "Cleaning..."
	@rm -f main

# Live Reload
watch:
	@if command -v air > /dev/null; then \
            air; \
            echo "Watching...";\
        else \
            read -p "Go's 'air' is not installed on your machine. Do you want to install it? [Y/n] " choice; \
            if [ "$$choice" != "n" ] && [ "$$choice" != "N" ]; then \
                go install github.com/air-verse/air@latest; \
                air; \
                echo "Watching...";\
            else \
                echo "You chose not to install air. Exiting..."; \
                exit 1; \
            fi; \
        fi

.PHONY: all build docker-build frontend-build run docker-run docker-down test clean watch
