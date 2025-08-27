FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN mkdir -p /app/

# Install dependencies
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/venv/
ENV VIRTUAL_ENV=/venv/
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,from=root,source=uv.lock,target=/app/uv.lock \
    --mount=type=bind,from=root,source=pyproject.toml,target=/app/pyproject.toml \
    cd /app/ && \
    uv sync --locked --no-install-project --compile-bytecode --group openapi_conversion

# Ensure UV don't check dependencies or lock file, since we installed everything before
ENV UV_FROZEN=1


ADD . /app
WORKDIR /app

ENTRYPOINT ["uv","run", "convert_openapi_to_implicitdict.py"]
