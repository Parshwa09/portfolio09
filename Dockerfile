# Use Python slim image
FROM python:3.11-slim

# Install system dependencies needed for dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Create virtual environment
RUN python -m venv /opt/venv

# Activate venv and install Python dependencies
RUN /bin/bash -c "source /opt/venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"

# Use virtual environment by default
ENV PATH="/opt/venv/bin:$PATH"

# Expose port if needed (e.g., Django default)
EXPOSE 8000

# Run your app (example Django command)
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
