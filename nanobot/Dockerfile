# Nanobot gateway Dockerfile
# Multi-stage build with uv
# Build context: ./nanobot (with additional_contexts: workspace: .)

# ---
# Stage 1: build the application
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy everything from workspace context first
COPY --from=workspace . /app/

# Copy nanobot source (build context)
COPY . /app/nanobot/

# Sync nanobot package with all dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot

# ---
# Stage 2: final image
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Accept APP_UID and APP_GID as build args for consistent user IDs
ARG APP_UID=1000
ARG APP_GID=1000

# Create user with specified IDs
RUN groupadd --system --gid ${APP_GID} appgroup && \
    useradd --system --gid ${APP_GID} --uid ${APP_UID} appuser

# Copy the application from builder
COPY --from=builder --chown=appuser:appgroup /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Use appuser to run the application
USER appuser

WORKDIR /app/nanobot

# Run the entrypoint script
CMD ["python", "/app/nanobot/entrypoint.py"]
