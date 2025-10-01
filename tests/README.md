# Repository-Level Test Implementation

## Overview

This directory contains **repository-level tests** for fast feedback during development. For comprehensive testing and performance validation, see the external CI/CD testing strategy in `TESTING_STRATEGY.md`.

## Quick Start

### 1. Unit Tests (Python + pytest)
```bash
# Install dependencies
pip install pytest pytest-cov pytest-flask requests faker

# Run tests
pytest tests/unit/ -v --cov=app

# Run with coverage report
pytest tests/unit/ -v --cov=app --cov-report=html
```

### 2. Basic Integration Tests (Python + requests)
```bash
# Run integration tests
pytest tests/integration/ -v

# Run with specific test
pytest tests/integration/test_api_endpoints.py::test_user_location_endpoint -v
```

### 3. Quick Performance Tests (Python + pytest-benchmark)
```bash
# Install benchmark tools
pip install pytest-benchmark

# Run performance benchmarks
pytest tests/performance/ -v --benchmark-only

# Run with benchmark comparison
pytest tests/performance/ -v --benchmark-compare
```

## Test Structure
```
tests/
├── unit/           # Unit tests (pytest) - Fast, isolated
├── integration/    # Basic integration tests (pytest + requests)
├── performance/    # Quick performance benchmarks (pytest-benchmark)
├── fixtures/       # Test data and fixtures
└── utils/          # Test utilities and helpers
```

## Environment Setup
```bash
# Create virtual environment
python -m venv test-env
source test-env/bin/activate  # Linux/Mac
# test-env\Scripts\activate   # Windows

# Install test dependencies
pip install -r requirements-test.txt

# Set up test environment variables
export TEST_API_KEY="test-api-key"
export TEST_BASE_URL="http://localhost:5001"
```

## External Testing

For comprehensive testing, performance validation, and CI/CD integration, use your external test framework with the test scenarios outlined in `TESTING_STRATEGY.md`.

### External Test Scenarios
- **Advanced API Testing**: High-concurrency, cross-browser testing
- **Performance Testing**: Load testing with Locust, K6, or Artillery
- **Stress Testing**: Beyond normal capacity testing
- **Endurance Testing**: Long-running stability tests

### Framework Options
- **Python**: Locust, pytest + requests
- **JavaScript**: K6, Artillery, Jest + Supertest
- **Go**: Vegeta, Hey, custom tools
