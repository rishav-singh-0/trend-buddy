FROM python:3.12-slim AS runtime
ARG SERVICE_PACKAGE
ARG SERVICE_MODULE

WORKDIR /workspace
ENV SERVICE_PACKAGE=${SERVICE_PACKAGE}
ENV SERVICE_MODULE=${SERVICE_MODULE}

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
COPY packages/python ./packages/python
COPY services ./services

RUN uv sync --package ${SERVICE_PACKAGE}

CMD ["/bin/sh", "-lc", "exec uv run --package ${SERVICE_PACKAGE} python -m ${SERVICE_MODULE}"]
