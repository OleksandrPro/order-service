FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --no-install-project

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ src/

EXPOSE 80

CMD ["uv", "run", "flask", "--app", "src.main:app", "run", "--host", "0.0.0.0", "--port", "80"]