FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder
RUN apk add --no-cache libpq
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv pip install --system -r pyproject.toml
COPY . .

# Run migrations and start server
ENTRYPOINT sh -c "alembic upgrade head && python -m gunicorn -w 4 -b 0.0.0.0:8080 main:server"
