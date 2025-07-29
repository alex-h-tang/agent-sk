FROM python:3.13-slim as builder

RUN pip install uv

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt requirements.txt

RUN uv pip install --system --no-cache -r requirements.txt

FROM python:3.13-slim

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY . .

EXPOSE 8000

# uvicorn fastmcp_server:app --host 0.0.0.0 --port 8000

CMD ["uvicorn", "fastmcp_server:app", "--host", "0.0.0.0", "--port", "8000"]