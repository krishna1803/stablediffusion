FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy all files
COPY . /app

# Install Python dependencies
RUN pip3 install --upgrade pip && \
    if [ -f requirements.txt ]; then pip3 install -r requirements.txt; fi 

# Expose port
EXPOSE 8080

# Run the FastAPI app
CMD ["python3", "app.py"]
