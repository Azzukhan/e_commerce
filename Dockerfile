# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install PostgreSQL development libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Set the environment variable for Django settings
ENV DJANGO_SETTINGS_MODULE=e_commerce_app.settings

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
