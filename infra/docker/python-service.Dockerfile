FROM python:3.9-slim AS runtime
ARG SERVICE_PACKAGE
ARG SERVICE_MODULE

WORKDIR /workspace

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
COPY packages/python ./packages/python
COPY services ./services

RUN uv sync --package ${SERVICE_PACKAGE}

CMD ["/bin/sh", "-lc", "exec uv run --package ${SERVICE_PACKAGE} python -m ${SERVICE_MODULE}"]
