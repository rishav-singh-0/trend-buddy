
## Technology Stack

- Go (version `1.26.1`) for microservices and apis
- Vue js for frontend
- `npm` use RUN npm this proxy registry `https://artifactory.arm.com/artifactory/api/npm/mirrors.npmjs_org`
- For Python (version `3.12`) strictly use `uv` package manager
- Any python module should be run using uv (`uv run xyz`)
- Use `make` for building or running docker
- Project overall uses both go and python for making services/modules
- All commands should be run inside Docker environment (run using `make up`)

## Architecture Rules
Must read following files:
1. README.md
2. docs/architecture.md
