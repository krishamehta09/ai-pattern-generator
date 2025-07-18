FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Prevent Rust-related build errors
ENV CARGO_NET_GIT_FETCH_WITH_CLI=true
ENV PIP_NO_CACHE_DIR=1

# Create working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY server.py .
COPY index.html .

# Install Python dependencies first
RUN pip install --upgrade pip setuptools wheel
RUN pip install --prefer-binary -r requirements.txt

# Expose the app on port 5000
EXPOSE 5000

# Run the app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
