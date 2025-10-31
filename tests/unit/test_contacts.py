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
    CONTACT_BULK_CREATE_RESPONSE,
    CONTACT_BULK_UPDATE_RESPONSE,
    USAGE_STATS_RESPONSE,
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


@respx.mock
async def test_contact_bulk_create_unit():
    """
    Test bulk creating contacts (unit test with mocked response).

    Validates that the client correctly sends bulk create data
    and parses the response with created_contacts and existing_contacts.
    """
    # Mock the API response
    respx.post("https://api.apollo.io/api/v1/contacts/bulk_create").mock(
        return_value=Response(200, json=CONTACT_BULK_CREATE_RESPONSE)
    )

    client = ApolloClient(api_key="test_api_key")

    # Bulk create contacts
    contacts = [
        {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com",
            "title": "Product Manager",
            "organization_name": "Test Corp",
            "label_names": ["MCP Test"]
        },
        {
            "first_name": "Bob",
            "last_name": "Jones",
            "email": "bob.jones@testco.com",
            "title": "Engineer",
            "organization_name": "Test Company",
            "label_names": ["MCP Test"]
        },
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"  # Existing contact
        }
    ]

    result = await client.contact_bulk_create(contacts=contacts)

    # Validate response structure
    assert result is not None
    assert hasattr(result, 'created_contacts')
    assert hasattr(result, 'existing_contacts')

    # Validate created contacts
    assert isinstance(result.created_contacts, list)
    assert len(result.created_contacts) == 2
    assert result.created_contacts[0].get('id') == 'bulk_created_1'
    assert result.created_contacts[0].get('first_name') == 'Alice'
    assert result.created_contacts[1].get('id') == 'bulk_created_2'
    assert result.created_contacts[1].get('first_name') == 'Bob'

    # Validate existing contacts
    assert isinstance(result.existing_contacts, list)
    assert len(result.existing_contacts) == 1
    assert result.existing_contacts[0].get('id') == 'existing_contact_1'
    assert result.existing_contacts[0].get('email') == 'jane.doe@example.com'


@respx.mock
async def test_contact_bulk_update_unit():
    """
    Test bulk updating contacts (unit test with mocked response).

    Validates that the client correctly sends bulk update data
    and parses the updated contacts response.
    """
    # Mock the API response
    respx.post("https://api.apollo.io/api/v1/contacts/bulk_update").mock(
        return_value=Response(200, json=CONTACT_BULK_UPDATE_RESPONSE)
    )

    client = ApolloClient(api_key="test_api_key")

    # Bulk update contacts
    contacts = [
        {
            "id": "bulk_created_1",
            "title": "Senior Product Manager",
            "label_names": ["MCP Test", "Updated"]
        },
        {
            "id": "bulk_created_2",
            "email": "bob.jones.new@testco.com"
        }
    ]

    result = await client.contact_bulk_update(contacts=contacts)

    # Validate response structure
    assert result is not None
    assert hasattr(result, 'contacts')
    assert isinstance(result.contacts, list)
    assert len(result.contacts) == 2

    # Validate first updated contact
    first_contact = result.contacts[0]
    assert first_contact.get('id') == 'bulk_created_1'
    assert first_contact.get('title') == 'Senior Product Manager'
    assert 'test_label_123' in first_contact.get('label_ids', [])
    assert 'test_label_456' in first_contact.get('label_ids', [])

    # Validate second updated contact
    second_contact = result.contacts[1]
    assert second_contact.get('id') == 'bulk_created_2'
    assert second_contact.get('email') == 'bob.jones.new@testco.com'


@respx.mock
async def test_usage_stats_unit():
    """
    Test retrieving API usage statistics (unit test with mocked response).

    Validates that the client correctly retrieves and parses
    rate limit information per endpoint.
    """
    # Mock the API response
    respx.post("https://api.apollo.io/api/v1/usage_stats/api_usage_stats").mock(
        return_value=Response(200, json=USAGE_STATS_RESPONSE)
    )

    client = ApolloClient(api_key="test_api_key")

    # Get usage stats
    result = await client.usage_stats()

    # Validate response structure
    assert result is not None

    # Note: The response is a dict with dynamic keys for each endpoint
    # We need to access the raw dict data
    result_dict = result.model_dump()

    # Validate people search endpoint stats
    assert "api/v1/mixed_people/search" in result_dict
    people_search_stats = result_dict["api/v1/mixed_people/search"]
    assert "minute" in people_search_stats
    assert people_search_stats["minute"]["limit"] == 60
    assert people_search_stats["minute"]["consumed"] == 12
    assert people_search_stats["minute"]["left_over"] == 48

    # Validate contacts search endpoint stats
    assert "api/v1/contacts/search" in result_dict
    contacts_search_stats = result_dict["api/v1/contacts/search"]
    assert contacts_search_stats["day"]["limit"] == 5000
    assert contacts_search_stats["day"]["consumed"] == 234
    assert contacts_search_stats["day"]["left_over"] == 4766

    # Validate bulk create endpoint stats
    assert "api/v1/contacts/bulk_create" in result_dict
    bulk_create_stats = result_dict["api/v1/contacts/bulk_create"]
    assert bulk_create_stats["hour"]["limit"] == 100
    assert bulk_create_stats["hour"]["consumed"] == 15
    assert bulk_create_stats["hour"]["left_over"] == 85
