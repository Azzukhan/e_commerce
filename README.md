# E-commerce Microservices Application

This is an e-commerce application built using Django and Docker. The application is divided into multiple microservices: Authentication Service, Product Service, Order Service, and Payment Service. Each service is Dockerized and managed using Docker Compose.

## Table of Contents
- [Project Overview](#project-overview)
- [Microservices](#microservices)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring](#monitoring)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project aims to provide a scalable and maintainable architecture for an e-commerce application using Django and Docker. The application is composed of the following microservices:

1. **Authentication Service**: Manages user authentication and authorization.
2. **Product Service**: Manages product information and inventory.
3. **Order Service**: Manages customer orders and order items.
4. **Payment Service**: Handles payment processing and updates order status.

## Microservices

### Authentication Service
- **Port**: 8000
- **Description**: Handles user authentication and authorization.
- **Tech Stack**: Django, PostgreSQL

### Product Service
- **Port**: 8001
- **Description**: Manages products and inventory.
- **Tech Stack**: Django, PostgreSQL

### Order Service
- **Port**: 8002
- **Description**: Manages customer orders and order items.
- **Tech Stack**: Django, PostgreSQL

### Payment Service
- **Port**: 8003
- **Description**: Handles payment processing and updates order status.
- **Tech Stack**: Django, PostgreSQL

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Azzukhan/e_commerce_app.git
    cd e_commerce_app
    ```

2. Build and start the Docker containers:
    ```sh
    docker-compose up --build
    ```

### Running the Application

The application will be available at the following ports:

- Authentication Service: http://localhost:8000
- Product Service: http://localhost:8001
- Order Service: http://localhost:8002
- Payment Service: http://localhost:8003

## CI/CD Pipeline

This project uses GitHub Actions for CI/CD. The pipeline is triggered on every push to the `main` branch. It performs the following steps:

1. **Checkout code**: Retrieves the latest code from the repository.
2. **Set up Docker Buildx**: Configures Docker Buildx for multi-platform builds.
3. **Log in to Docker Hub**: Authenticates with Docker Hub using credentials stored in GitHub Secrets.
4. **Build and push Docker image**: Builds the Docker image and pushes it to Docker Hub.
5. **Deploy with Docker Compose**: Deploys the application using Docker Compose.

### GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: Log in to Docker Hub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push Docker image
        run: |
          docker build -t yourdockerhubusername/e_commerce_app:latest .
          docker push yourdockerhubusername/e_commerce_app:latest

      - name: Deploy with Docker Compose
        run: |
          docker-compose up -d
        env:
          POSTGRES_DB: ${{ secrets.POSTGRES_DB }}
          POSTGRES_USER: ${{ secrets.POSTGRES_USER }}
          POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
```

### Monitoring
This project includes monitoring using Prometheus and Grafana. Prometheus collects metrics from the services, and Grafana is used for visualizing the metrics.

  #### Prometheus
    Port: 9090
    Configuration: Located at monitoring/prometheus/prometheus.yml
  #### Grafana
    Port: 4000
    Configuration: Dashboards and datasources configured in monitoring/grafana/provisioning/

### Contributing
Contributions are welcome! Please follow the guidelines below:

  - Fork the repository.
  - Create a new branch for your feature or bugfix.
  - Make your changes and commit them with descriptive messages.
  - Push your changes to your fork and submit a pull request.
