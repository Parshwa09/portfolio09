FROM python:3.11-bullseye

# Install only minimal system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN python -m venv /opt/venv
RUN /bin/bash -c "source /opt/venv/bin/activate && pip install --upgrade pip setuptools wheel && pip install -r requirements.txt"

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000
CMD ["gunicorn", "portfolio.wsgi:application", "--bind", "0.0.0.0:8000"]
