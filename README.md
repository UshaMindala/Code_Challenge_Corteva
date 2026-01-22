# Weather & Crop Yield Coding Challenge

## Overview
This project implements a small data platform for historical weather data and derived statistics, exposed via a REST API. It covers:
- Ingesting raw weather files into a relational database
- Computing yearly per-station weather statistics
- Serving both raw and aggregated data via a FastAPI REST API with automatic documentation

## Tech stack
- **Language**: Python 3.x
- **Framework**: FastAPI (with automatic OpenAPI/Swagger docs)
- **Database**: SQLite (via SQLAlchemy ORM)
- **HTTP server**: Uvicorn
- **Dev tools**:
  - Black / isort (code formatting)
  - flake8 / ruff (linting)
  - pytest (unit tests)

## Project structure
```text
code-challenge-template/
  wx_data/
  yld_data/
  app/
    __init__.py
    database.py
    models.py
    schemas.py
    ingestion.py
    analysis.py
    main.py
    tests/
      test_api.py
  requirements.txt
  README.md
