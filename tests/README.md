# Tests for Mergington High School Activities API

This directory contains comprehensive tests for the FastAPI-based Activities API.

## Test Structure

### Test Files

- **`conftest.py`** - Test configuration and shared fixtures
- **`test_main_endpoints.py`** - Tests for basic API endpoints (root redirect, get activities)
- **`test_signup.py`** - Tests for student registration functionality
- **`test_unregister.py`** - Tests for student unregistration functionality  
- **`test_integration.py`** - End-to-end integration tests and workflows

### Test Coverage

The test suite provides **100% code coverage** of the main application (`src/app.py`).

## Running Tests

### Basic Test Execution

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run a specific test file
python -m pytest tests/test_signup.py -v
```

### Coverage Reports

```bash
# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing

# Generate HTML coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

### Using the Test Runner Script

```bash
# Basic run
python run_tests.py

# With coverage and verbose output
python run_tests.py --coverage --verbose

# Run specific test file
python run_tests.py --test test_signup.py
```

## Test Categories

### Unit Tests
- Individual endpoint functionality
- Input validation
- Error handling
- Data structure validation

### Integration Tests
- Complete user workflows
- Multi-step operations
- Cross-endpoint interactions
- End-to-end scenarios

## Test Data Management

Tests use the `reset_activities` fixture to ensure test isolation by restoring the original activities data after each test that modifies the database.

## Key Test Scenarios

### Registration Tests
- ✅ Successful student registration
- ✅ Duplicate registration prevention
- ✅ Non-existent activity registration
- ✅ URL encoding handling
- ✅ Email format validation

### Unregistration Tests  
- ✅ Successful student unregistration
- ✅ Unregistration of non-registered students
- ✅ Non-existent activity unregistration
- ✅ URL encoding handling

### Integration Tests
- ✅ Complete registration/unregistration workflows
- ✅ Multiple students per activity
- ✅ Single student across multiple activities
- ✅ Capacity constraint testing
- ✅ Error handling scenarios

## Dependencies

The tests require the following packages (included in `requirements.txt`):

- `pytest` - Test framework
- `httpx` - HTTP client for FastAPI testing
- `pytest-cov` - Coverage reporting

## Running Tests in CI/CD

The test suite is designed to be run in continuous integration environments. All tests are isolated and can run in parallel.

```bash
# Example CI command
python -m pytest tests/ --cov=src --cov-report=xml --junitxml=junit.xml
```