FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Install system dependencies and Python 3.12
RUN apt-get update && \
    apt-get install -y \
        software-properties-common \
        && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
        python3.12 \
        python3.12-dev \
        python3.12-venv \
        git \
        wget \
        curl \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libgomp1 \
        libgl1-mesa-glx \
        && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Python 3.12 as default python3 and python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1

# Create Python 3.12 virtual environment
RUN python3.12 -m venv /opt/venv

# Activate virtual environment and upgrade pip
RUN /opt/venv/bin/python -m pip install --upgrade pip setuptools wheel

# Set environment variables to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV="/opt/venv"

# Set workdir
WORKDIR /app

# Copy all application files first (so requirements file exists regardless of location)
COPY . /app

COPY config/requirements.txt /app/


# Install Python dependencies in the virtual environment
RUN pip install --no-cache-dir -r /app/requirements.txt

# Create output directories
RUN mkdir -p /app/final_outputs /app/upscaled_outputs /app/scheduler_outputs && \
    chmod 777 /app/final_outputs /app/upscaled_outputs /app/scheduler_outputs

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Health check (FastAPI)
HEALTHCHECK --interval=30s --timeout=30s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run both FastAPI and Streamlit services
CMD ["./scripts/start_studio.sh"]
