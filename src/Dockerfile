FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --no-install-project

COPY ./src /app/src

WORKDIR /app/src

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 80

CMD ["uv", "run", "flask", "--app", "main:app", "run", "--host", "0.0.0.0", "--port", "80"]