<br/>
<p align="center">
<a href="https://github.com/razllivan/django-florist-app">
    <img src="https://s3.amazonaws.com/media-p.slid.es/uploads/708405/images/4005243/django_rest_500x500.png" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">Online Store API</h3>

  <p align="center">
    Django Rest Framework (DRF) API for an online store. The API allows frontend developers to interact with the store's data, including products, categories, sizes, and images.
    <br/>
    <br/>
  </p>

![![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://img.shields.io/badge/code_style-black-black)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue)

## Table Of Contents

* [Key Features](#key-features)
* [Technology Stack](#technology-stack)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
        * [Local Development](#local-development)
* [API Documentation](#api-documentation)

## Key Features

- **Category Management**: Organize your products with a flexible category
  system.
- **Product Management**: Create, update, and delete products along with their
  images and sizes.
- **Product Filtering**: Retrieve products through filters to streamline
  customer experience.

## Technology Stack

- **Django & Django REST Framework**
- **Poetry**
- **PostgreSQL**
- **Docker & Docker Compose**

## Getting Started

### Prerequisites

* docker

### Installation

### Local Development

To get started with local development:

1. Clone the repository:

```bash
git clone https://github.com/razllivan/django-florist-app.git &&
cd django-florist-app
```

2. Copy the example .env file and set the necessary environment variables:

```bash
cp .envs/.local/.env.example .envs/.local/.env
```

3. Launch the development services using Docker Compose:

```bash
docker-compose -f local.yml up -d --build
```

After the containers start, the project will be available
at http://localhost:8000.

## API Documentation

After starting the project, the API documentation will be available
at http://localhost:8000/api/docs.


