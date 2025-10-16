# Testing Guide for MeXR Backend

## Setup

1. **Install test dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure you have a `.env` file with your API key** (or the tests will use a fake key for unit tests)

## Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run a specific test file:
```bash
pytest tests/test_app.py -v
```

### Run a specific test class:
```bash
pytest tests/test_app.py::TestKnowledgeBase -v
```

### Run a specific test function:
```bash
pytest tests/test_app.py::TestKnowledgeBase::test_get_organ_info_valid -v
```

### Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

### Run with verbose output and show print statements:
```bash
pytest tests/ -v -s
```

## Test Structure

The test suite is organized into the following test classes:

- **TestKnowledgeBase**: Tests for the anatomy knowledge base
- **TestTools**: Tests for LangChain tools (highlight_object, play_sound)
- **TestSessionManager**: Tests for session and chat history management
- **TestModels**: Tests for Pydantic model validation
- **TestAPIEndpoints**: Tests for FastAPI endpoints
- **TestIntegration**: End-to-end integration tests

## Test Coverage

Current test coverage includes:
- ✅ Knowledge base operations
- ✅ LangChain tool invocations
- ✅ Session management and history
- ✅ Model validation
- ✅ API endpoint responses
- ✅ Error handling
- ✅ Integration flows

## Writing New Tests

To add new tests, follow this pattern:

```python
class TestYourFeature:
    """Tests for your new feature."""
    
    def test_feature_works(self):
        """Test that the feature works correctly."""
        # Arrange
        input_data = "test"
        
        # Act
        result = your_function(input_data)
        
        # Assert
        assert result == expected_output
```

## CI/CD Integration

You can add these tests to your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ -v --cov=app
```

## Troubleshooting

**Issue: Import errors**
- Make sure you're in the project root directory
- Verify all dependencies are installed: `pip install -r requirements.txt`

**Issue: Tests failing due to API key**
- The tests use mocks for agent calls, so they shouldn't need a real API key
- Check that `conftest.py` is setting the test API key

**Issue: Async test warnings**
- Make sure `pytest-asyncio` is installed
- Tests using `async` functions are properly decorated with `@pytest.mark.asyncio`
