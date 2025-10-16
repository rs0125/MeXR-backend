"""
Test configuration and fixtures for pytest
"""

import pytest
import os
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()

# Ensure we have a test API key (you can use a fake one for unit tests)
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "sk-test-fake-key-for-testing"


@pytest.fixture
def sample_organ_data():
    """Fixture providing sample organ data."""
    return {
        "displayName": "Test Organ",
        "socketID": "socket_test",
        "description": "A test organ for unit tests",
        "function": "Testing purposes"
    }


@pytest.fixture
def sample_vr_request():
    """Fixture providing sample VR query request."""
    return {
        "sessionID": "test_session_123",
        "context": {"heldObject": "heart"},
        "query": "Where does this go?"
    }
