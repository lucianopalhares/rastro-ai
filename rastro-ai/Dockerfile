FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir "psycopg[binary]>=3.2,<4" "tiktoken>=0.9,<1" "langchain-text-splitters>=0.3,<1" "langchain-openai>=1,<2" "langchain-postgres>=0.0.19,<1" "langgraph>=1,<2" "langfuse>=5,<6"

COPY src ./src

ENV PYTHONPATH=/app/src
CMD ["python", "-m", "rastro_ai.service"]
