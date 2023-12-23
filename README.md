# Product Catalog API

This project is a Product Catalog API that provides a RESTful interface for managing a product catalog in an online store.

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)

## Table of Contents
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Local Development](#local-development)
- [API Documentation](#api-documentation)
## Key Features

- Manage product categories
- Manage products, their images, and sizes
- Product filtering
- Serialization of product data for read and write operations

## Technology Stack

- Django & Django REST Framework
- Poetry for dependency management
- PostgreSQL
- Docker and Docker Compose for containerization and easy setup

## Getting Started

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/razllivan/django-florist-app.git &&
cd django-florist-app
```

2. Copy the example .env file and set the necessary environment variables:

```bash
cp .envs/.local/.env.example .envs/.local/.env
```

4. Launch the development services using Docker Compose:

```bash
docker-compose -f local.yml up -d --build
```

After the containers start, the project will be available at http://localhost:8000.

## API Documentation

After starting the project, the API documentation will be available at http://localhost:8000/api/docs.
