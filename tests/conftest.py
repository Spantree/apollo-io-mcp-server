"""
Test configuration and fixtures for Apollo.io MCP Server tests.
"""
import os
import pytest
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv('.env.secrets')


@pytest.fixture(scope="session")
def apollo_api_key():
    """Get Apollo API key from environment."""
    api_key = os.getenv("APOLLO_IO_API_KEY") or os.getenv("APOLLO_API_KEY")
    if not api_key:
        pytest.skip("No Apollo API key found in environment")
    return api_key


@pytest.fixture(scope="session")
def vcr_cassette_dir():
    """Directory for VCR cassettes."""
    cassette_dir = Path(".scratch/http-tests")
    cassette_dir.mkdir(parents=True, exist_ok=True)
    return str(cassette_dir)


@pytest.fixture(scope="module")
def vcr_config(vcr_cassette_dir):
    """
    VCR.py configuration for recording HTTP interactions.

    Cassettes are stored in .scratch/http-tests/ and NOT committed to git.
    This allows us to record real API interactions for validation without
    exposing sensitive data in the repository.
    """
    return {
        "cassette_library_dir": vcr_cassette_dir,
        "record_mode": "once",  # Record once, then replay
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        "filter_headers": [
            ("x-api-key", "REDACTED"),  # Hide API key in cassettes
        ],
        "decode_compressed_response": True,
    }
