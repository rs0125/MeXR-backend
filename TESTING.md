# Quick Test Commands Reference

## Run All Tests
```bash
pytest tests/ -v
```

## Run Specific Test Files
```bash
pytest tests/test_app.py -v
```

## Run Specific Test Classes
```bash
# Knowledge Base tests
pytest tests/test_app.py::TestKnowledgeBase -v

# Tools tests
pytest tests/test_app.py::TestTools -v

# Session Manager tests
pytest tests/test_app.py::TestSessionManager -v

# API Endpoint tests
pytest tests/test_app.py::TestAPIEndpoints -v

# Integration tests
pytest tests/test_app.py::TestIntegration -v
```

## Run Specific Test Functions
```bash
pytest tests/test_app.py::TestKnowledgeBase::test_get_organ_info_valid -v
```

## Useful Options
```bash
# Show print statements
pytest tests/ -v -s

# Stop at first failure
pytest tests/ -x

# Run last failed tests
pytest tests/ --lf

# Show test coverage
pytest tests/ --cov=app --cov-report=term-missing

# Generate HTML coverage report
pytest tests/ --cov=app --cov-report=html
# Then open htmlcov/index.html in browser

# Run with minimal output
pytest tests/ -q

# Run with more detailed output
pytest tests/ -vv
```

## Test Results Summary
✅ **21 tests passing**
- 3 Knowledge Base tests
- 4 Tools tests  
- 5 Session Manager tests
- 3 Model tests
- 5 API Endpoint tests
- 1 Integration test
