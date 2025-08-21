FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Install system dependencies and Python 3.12
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        curl \
        git \
        ca-certificates \
        python3.12 \
        python3.12-venv \
        python3.12-distutils \
        && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Create Python 3.12 virtual environment
RUN python3.12 -m venv /opt/venv

# Activate virtual environment and upgrade pip
RUN /opt/venv/bin/python -m pip install --upgrade pip setuptools wheel

# Set environment variables to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV="/opt/venv"

# Install Python dependencies in virtual environment
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    && pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cu118 \
        torch torchvision

# Copy all application files
COPY . /app

# Start script (FastAPI + optional Streamlit)
COPY docker/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Health check (FastAPI)
HEALTHCHECK --interval=30s --timeout=30s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run both FastAPI and Streamlit services
CMD ["/app/start.sh"]
