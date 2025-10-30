"""
Integration tests for Apollo.io contact operations.

These tests make real API calls and record them with VCR.py.
Cassettes are stored in .scratch/http-tests/ (not committed).

To run these tests:
    pytest -m integration

By default, these tests are skipped (see pyproject.toml).
"""
import pytest
import vcr
from pathlib import Path
from apollo_client import ApolloClient


# VCR configuration for all tests
vcr_config = vcr.VCR(
    cassette_library_dir=".scratch/http-tests",
    record_mode="once",  # Record once, then replay
    match_on=["method", "uri"],
    filter_headers=[("x-api-key", "REDACTED")],
    decode_compressed_response=True,
)


@pytest.mark.integration
async def test_contacts_search_no_results(apollo_api_key):
    """
    Test searching for contacts with a query unlikely to have results.

    This validates the API contract and response structure.
    """
    with vcr_config.use_cassette("contacts_search_no_results.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # Search for contacts with unlikely query
        result = await client.contacts_search(
            query="nonexistentcontact12345@example.com",
            page=1,
            per_page=10
        )

        # Should return successful response even with no results
        assert result is not None
        assert hasattr(result, 'contacts')
        assert hasattr(result, 'pagination')
        assert isinstance(result.contacts, list)
        assert result.pagination.page == 1


@pytest.mark.integration
async def test_contact_create(apollo_api_key):
    """
    Test creating a new contact.

    Creates a test contact for validation purposes.
    Note: This will create a real contact in your Apollo CRM.
    """
    with vcr_config.use_cassette("contact_create_test_contact.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # Create a test contact
        result = await client.contact_create(
            first_name="Test",
            last_name="Contact",
            email=f"test-mcp-{pytest.test_id}@example.com",
            organization_name="Test Organization",
            title="Test Engineer",
            label_names=["MCP Test"]
        )

        # Validate response structure
        assert result is not None
        assert hasattr(result, 'contact')
        contact = result.contact

        # Verify contact data
        assert 'id' in contact
        assert contact.get('first_name') == "Test"
        assert contact.get('last_name') == "Contact"
        assert "test-mcp-" in contact.get('email', '')

        # Store contact ID for update test
        pytest.test_contact_id = contact.get('id')


@pytest.mark.integration
async def test_contact_update(apollo_api_key):
    """
    Test updating an existing contact.

    Updates the contact created in test_contact_create.
    Requires test_contact_create to run first.
    """
    # Skip if no contact ID from create test
    if not hasattr(pytest, 'test_contact_id'):
        pytest.skip("No test contact ID available (test_contact_create must run first)")

    with vcr_config.use_cassette("contact_update_test_contact.yaml"):
        client = ApolloClient(api_key=apollo_api_key)
        contact_id = pytest.test_contact_id

        # Update the test contact
        result = await client.contact_update(
            contact_id=contact_id,
            title="Senior Test Engineer",
            label_names=["MCP Test", "Updated"]
        )

        # Validate response structure
        assert result is not None
        assert hasattr(result, 'contact')
        contact = result.contact

        # Verify updated data
        assert contact.get('id') == contact_id
        assert contact.get('title') == "Senior Test Engineer"
        # Note: label_names might be returned as label_ids or not at all


@pytest.mark.integration
async def test_contacts_search_pagination(apollo_api_key):
    """
    Test contacts search with pagination parameters.

    Validates pagination structure even if no results.
    """
    with vcr_config.use_cassette("contacts_search_pagination.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # Search with pagination
        result = await client.contacts_search(
            query="test",
            page=1,
            per_page=5
        )

        # Validate pagination structure
        assert result is not None
        assert hasattr(result, 'pagination')
        pagination = result.pagination

        assert hasattr(pagination, 'page')
        assert hasattr(pagination, 'per_page')
        assert hasattr(pagination, 'total_entries')
        assert hasattr(pagination, 'total_pages')

        assert pagination.page == 1
        assert pagination.per_page == 5


# Add unique test ID for creating unique contacts
@pytest.fixture(scope="session", autouse=True)
def set_test_id():
    """Generate unique test ID for this test run."""
    import time
    pytest.test_id = int(time.time())
