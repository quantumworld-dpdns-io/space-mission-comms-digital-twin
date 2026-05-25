FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

FROM base AS builder
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential
COPY pyproject.toml setup.cfg ./
COPY src/python/ src/python/
RUN pip install --user build && python -m build --wheel

FROM base AS production
COPY --from=builder /app/dist/*.whl /tmp/
RUN pip install /tmp/*.whl && rm /tmp/*.whl
EXPOSE 8000
CMD ["uvicorn", "space_comms_digital_twin.api.rest.app:app", "--host", "0.0.0.0", "--port", "8000"]
