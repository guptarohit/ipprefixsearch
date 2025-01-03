# IP Prefix Lookup Service

A high-performance service for looking up cloud provider information based on IP addresses.

## Overview

REST APIs provided to:

- Look up provider information for a single IP address
- Batch lookup for multiple IP addresses

## Features

- Support for both IPv4 and IPv6 addresses
- Multiple subnet matches per IP address
- In-memory prefix storage for optimal performance
- Radix tree based prefix lookup which is ~100x faster than linear search

## Setup

### Requirements

- Python 3.11 or higher
- Poetry for dependency management

### Installation

| Step                                                                      | Command                         |
| ------------------------------------------------------------------------- | ------------------------------- |
| 1. Create a virtual environment                                           | `python3.11 -m venv .venv`      |
| 2. Activate the virtual environment                                       | `source .venv/bin/activate`     |
| 3. Upgrade pip and setuptools                                             | `pip install -U pip setuptools` |
| 4. Install [poetry](https://python-poetry.org/) for dependency management | `pip install poetry`            |
| 5. Install dependencies                                                   | `poetry install`                |

### Start the service

```bash
poetry run uvicorn src.api.main:app --reload
```

## API Usage

### API Documentation

Once the server is running, Swagger UI documentation can be accessed from http://localhost:8000/docs

### Single IP Lookup

```bash
GET /api/v1/ips/199.83.128.1
```

### Multiple IP Lookup

```bash
GET /api/v1/ips?ips=192.168.1.100&ips=172.16.1.1
```

## Development

### Run tests

Run the test cases using `pytest`

```bash
poetry run pytest
```

### Run benchmarks

Run the benchmark tests using `pytest`

```bash
poetry run pytest tests/benchmarks/
```
