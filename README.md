# Order Service

A small order management module built as a part of a test assignment.

The service provides basic ERP-like functionality for managing customers, products, and orders with automatic order total calculation and stock handling.

## Features

- Create customers
- Create products
- Create orders
- Retrieve orders by customer
- Automatic order total calculation based on product price snapshots
- Stock validation and update during order creation

---

## Requirements

Make sure you have installed:

- Python 3.12+
- Docker & Docker Compose
- UV

---

## Environment Setup

Clone this repository to your local machine:

```bash
git clone https://github.com/OleksandrPro/order-service.git
```

Change into the project directory:

```bash
cd order-service
```

Create `.env` file based on example:

```
cp .env.example .env
```

## Example configuration:

```bash
DB__HOST=db
DB__USER=user
DB__PASSWORD=password
DB__PORT=5430
DB__NAME=order_service_db
```

##  Running with Docker

Create `docker-compose.override.yml` file based on example:

```bash
cp docker-compose.override.yml.example docker-compose.override.yml
```

Build and start services:

```bash
docker compose up --build
```

Start already built services:

```bash
docker compose up
```

API will be available at:
http://localhost:8000


##  Running tests
1. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
2. Install dependencies
```bash
uv sync
```

3. Run tests
```bash
uv run pytest
```

or 

```bash
pytest
```

## Design Notes

- Unit of Work is used to ensure transactional consistency across multiple repositories
- Business logic is separated from the persistence layer
- Services are responsible for orchestrating business workflows
- Repositories act as the data access layer
- Order total is calculated from product price snapshots at the time of purchase
- Pydantic is used as a DTO layer for validation and data transfer
