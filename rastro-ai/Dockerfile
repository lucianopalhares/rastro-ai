FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir "psycopg[binary]>=3.2,<4" "tiktoken>=0.9,<1"

COPY src ./src

ENV PYTHONPATH=/app/src
CMD ["python", "-m", "rastro_ai.service"]
