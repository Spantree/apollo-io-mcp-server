"""
Unit tests for Apollo.io contact operations using mocked responses.

These tests use respx to mock httpx requests and anonymized fixtures.
They run by default without requiring API credentials.
"""
import pytest
import respx
from httpx import Response
from apollo_client import ApolloClient
from tests.fixtures import (
    CONTACTS_SEARCH_NO_RESULTS,
    CONTACTS_SEARCH_WITH_RESULTS,
    CONTACT_CREATE_RESPONSE,
    CONTACT_UPDATE_RESPONSE,
)


@respx.mock
async def test_contact_search_no_results_unit():
    """
    Test searching for contacts with no results (unit test with mocked response).

    Validates that the client correctly handles empty search results.
    """
    # Mock the API response
    respx.get("https://api.apollo.io/api/v1/contacts/search").mock(
        return_value=Response(200, json=CONTACTS_SEARCH_NO_RESULTS)
    )

    client = ApolloClient(api_key="test_api_key")

    # Search for contacts
    result = await client.contact_search(
        query="nonexistentcontact@example.com",
        page=1,
        per_page=10
    )

    # Validate response structure
    assert result is not None
    assert hasattr(result, 'contacts')
    assert hasattr(result, 'pagination')
    assert isinstance(result.contacts, list)
    assert len(result.contacts) == 0
    assert result.pagination.page == 1
    assert result.pagination.per_page == 10
    assert result.pagination.total_entries == 0
    assert result.pagination.total_pages == 0


@respx.mock
async def test_contact_search_with_results_unit():
    """
    Test searching for contacts with results (unit test with mocked response).

    Validates that the client correctly parses contact data and pagination.
    """
    # Mock the API response
    respx.get("https://api.apollo.io/api/v1/contacts/search").mock(
        return_value=Response(200, json=CONTACTS_SEARCH_WITH_RESULTS)
    )

    client = ApolloClient(api_key="test_api_key")

    # Search for contacts
    result = await client.contact_search(
        query="test",
        page=1,
        per_page=5
    )

    # Validate response structure
    assert result is not None
    assert hasattr(result, 'contacts')
    assert hasattr(result, 'pagination')
    assert isinstance(result.contacts, list)
    assert len(result.contacts) == 2

    # Validate first contact
    first_contact = result.contacts[0]
    assert first_contact.get('id') == 'test_contact_1'
    assert first_contact.get('first_name') == 'Jane'
    assert first_contact.get('last_name') == 'Doe'
    assert first_contact.get('email') == 'jane.doe@example.com'
    assert first_contact.get('title') == 'Senior Product Manager'
    assert first_contact.get('organization_name') == 'Example Corp'

    # Validate pagination
    pagination = result.pagination
    assert pagination.page == 1
    assert pagination.per_page == 5
    assert pagination.total_entries == 42
    assert pagination.total_pages == 9


@respx.mock
async def test_contact_create_unit():
    """
    Test creating a new contact (unit test with mocked response).

    Validates that the client correctly sends contact creation data
    and parses the response.
    """
    # Mock the API response
    respx.post("https://api.apollo.io/api/v1/contacts").mock(
        return_value=Response(200, json=CONTACT_CREATE_RESPONSE)
    )

    client = ApolloClient(api_key="test_api_key")

    # Create a test contact
    result = await client.contact_create(
        first_name="Test",
        last_name="Contact",
        email="test.contact@example.com",
        organization_name="Test Organization",
        title="Test Engineer",
        label_names=["MCP Test"]
    )

    # Validate response structure
    assert result is not None
    assert hasattr(result, 'contact')

    contact = result.contact
    assert 'id' in contact
    assert contact.get('id') == 'created_contact_123'
    assert contact.get('first_name') == 'Test'
    assert contact.get('last_name') == 'Contact'
    assert contact.get('email') == 'test.contact@example.com'
    assert contact.get('title') == 'Test Engineer'
    assert contact.get('organization_name') == 'Test Organization'
    assert contact.get('source') == 'api'
    assert 'test_label_123' in contact.get('label_ids', [])


@respx.mock
async def test_contact_update_unit():
    """
    Test updating an existing contact (unit test with mocked response).

    Validates that the client correctly sends update data and parses
    the updated contact response.
    """
    contact_id = "created_contact_123"

    # Mock the API response
    respx.put(f"https://api.apollo.io/api/v1/contacts/{contact_id}").mock(
        return_value=Response(200, json=CONTACT_UPDATE_RESPONSE)
    )

    client = ApolloClient(api_key="test_api_key")

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
    assert contact.get('id') == contact_id
    assert contact.get('title') == 'Senior Test Engineer'
    assert contact.get('first_name') == 'Test'
    assert contact.get('last_name') == 'Contact'
    assert contact.get('email') == 'test.contact@example.com'

    # Verify updated labels
    label_ids = contact.get('label_ids', [])
    assert 'test_label_123' in label_ids
    assert 'test_label_456' in label_ids


@respx.mock
async def test_contact_search_pagination_unit():
    """
    Test contact search with pagination parameters (unit test with mocked response).

    Validates that pagination structure is correctly handled.
    """
    # Mock the API response
    respx.get("https://api.apollo.io/api/v1/contacts/search").mock(
        return_value=Response(200, json=CONTACTS_SEARCH_WITH_RESULTS)
    )

    client = ApolloClient(api_key="test_api_key")

    # Search with pagination
    result = await client.contact_search(
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
    assert pagination.total_entries == 42
    assert pagination.total_pages == 9
