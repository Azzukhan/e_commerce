# Unified Dockerfile for all services
FROM python:3.9-slim

WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean

# Copy the source code
COPY . .

# Ensure gunicorn is installed
RUN pip install gunicorn

# Set the default command to run the Django server using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "e_commerce_app.wsgi:application"]
