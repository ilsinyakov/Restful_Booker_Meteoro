# Test task for Meteoro Platform - AQA Engineer

## Project structure

```text
Restful_Booker_Meteoro/
├── schemas/                # Pydantic schemas for JSON validation
    ├── booking.py
├── tests/                  # Tests
    ├── test_booking.py
├── util/                   # Utils
    ├── allure_attach.py
├── config.py               # Configuration (URLs, credentials e.g.)
├── conftest.py             # Pytest fixtures
├── pyproject.toml          # Dependencies, uv project, ruff and pytest configuration
├── requirements.txt        # Dependencies list
```

## Run tests

### Install uv

[Документация uv](https://github.com/astral-sh/uv)

```sh
pip install uv
```

### 2. Create and activate virtual environment

```sh
uv venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

### 3. Install dependencies

```sh
uv sync
```

### 4. Run all tests

```sh
pytest
```

### 5. Allure Report

Allure must be installed on the system

[Документация Allure](https://allurereport.org/docs/)

```sh
allure serve allure-results
```
