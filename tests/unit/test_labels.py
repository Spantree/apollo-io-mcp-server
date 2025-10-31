"""
Unit tests for Apollo.io labels operations using mocked responses.

These tests use respx to mock httpx requests and anonymized fixtures.
They run by default without requiring API credentials.
"""
import pytest
import respx
from httpx import Response
from apollo_client import ApolloClient
from tests.fixtures import (
    LABELS_LIST_ALL,
    LABELS_LIST_CONTACTS,
    LABELS_LIST_ACCOUNTS,
)


@respx.mock
async def test_labels_list_all_unit():
    """
    Test listing all labels (unit test with mocked response).

    Validates that the client correctly handles labels from all modalities.
    """
    # Mock the API response - API returns array directly
    respx.get("https://api.apollo.io/api/v1/labels").mock(
        return_value=Response(200, json=LABELS_LIST_ALL)
    )

    client = ApolloClient(api_key="test_api_key")

    # List all labels
    result = await client.labels_list()

    # Validate response structure
    assert result is not None
    assert hasattr(result, 'labels')
    assert isinstance(result.labels, list)
    assert len(result.labels) == 4

    # Verify we have mixed modalities
    modalities = [label.modality for label in result.labels]
    assert "contacts" in modalities
    assert "accounts" in modalities

    # Validate first label structure
    first_label = result.labels[0]
    assert hasattr(first_label, 'id')
    assert hasattr(first_label, 'name')
    assert hasattr(first_label, 'modality')
    assert hasattr(first_label, 'cached_count')
    assert first_label.id == "label_contact_1"
    assert first_label.name == "Sales Prospects"
    assert first_label.modality == "contacts"


@respx.mock
async def test_labels_list_contacts_only_unit():
    """
    Test listing only contacts labels (unit test with mocked response).

    Validates that client-side filtering by modality works correctly.
    """
    # Mock the API response - API returns all labels
    respx.get("https://api.apollo.io/api/v1/labels").mock(
        return_value=Response(200, json=LABELS_LIST_ALL)
    )

    client = ApolloClient(api_key="test_api_key")

    # List only contacts labels
    result = await client.labels_list(modality="contacts")

    # Validate response structure
    assert result is not None
    assert hasattr(result, 'labels')
    assert isinstance(result.labels, list)

    # Should only have contacts labels (filtered client-side)
    assert len(result.labels) == 2
    for label in result.labels:
        assert label.modality == "contacts"

    # Verify label names
    label_names = [label.name for label in result.labels]
    assert "Sales Prospects" in label_names
    assert "MCP Test" in label_names


@respx.mock
async def test_labels_list_accounts_only_unit():
    """
    Test listing only accounts labels (unit test with mocked response).

    Validates that client-side filtering by modality works correctly.
    """
    # Mock the API response - API returns all labels
    respx.get("https://api.apollo.io/api/v1/labels").mock(
        return_value=Response(200, json=LABELS_LIST_ALL)
    )

    client = ApolloClient(api_key="test_api_key")

    # List only accounts labels
    result = await client.labels_list(modality="accounts")

    # Validate response structure
    assert result is not None
    assert hasattr(result, 'labels')
    assert isinstance(result.labels, list)

    # Should only have accounts labels (filtered client-side)
    assert len(result.labels) == 2
    for label in result.labels:
        assert label.modality == "accounts"

    # Verify label names
    label_names = [label.name for label in result.labels]
    assert "Enterprise Clients" in label_names
    assert "Target Accounts" in label_names


@respx.mock
async def test_labels_empty_list_unit():
    """
    Test handling of empty labels list (unit test with mocked response).

    Validates that the client correctly handles accounts with no labels.
    """
    # Mock the API response - empty array
    respx.get("https://api.apollo.io/api/v1/labels").mock(
        return_value=Response(200, json=[])
    )

    client = ApolloClient(api_key="test_api_key")

    # List all labels
    result = await client.labels_list()

    # Validate response structure
    assert result is not None
    assert hasattr(result, 'labels')
    assert isinstance(result.labels, list)
    assert len(result.labels) == 0


@respx.mock
async def test_labels_list_error_unit():
    """
    Test handling of API errors (unit test with mocked response).

    Validates that the client correctly handles 403 errors for non-master keys.
    """
    # Mock the API response - 403 Forbidden
    respx.get("https://api.apollo.io/api/v1/labels").mock(
        return_value=Response(
            403,
            json={
                "error": "api/v1/labels/index is not accessible with this api_key",
                "error_code": "API_INACCESSIBLE"
            }
        )
    )

    client = ApolloClient(api_key="test_api_key")

    # List all labels
    result = await client.labels_list()

    # Should return None on error
    assert result is None


@respx.mock
async def test_labels_response_fields_unit():
    """
    Test that all expected label fields are present (unit test with mocked response).

    Validates complete label structure from fixtures.
    """
    # Mock the API response
    respx.get("https://api.apollo.io/api/v1/labels").mock(
        return_value=Response(200, json=LABELS_LIST_ALL)
    )

    client = ApolloClient(api_key="test_api_key")

    # List all labels
    result = await client.labels_list()

    # Validate first label has all fields
    first_label = result.labels[0]

    # Required fields
    assert first_label.id == "label_contact_1"
    assert first_label.name == "Sales Prospects"
    assert first_label.modality == "contacts"

    # Optional fields
    assert first_label.cached_count == 42
    assert first_label.team_id == "team_123"
    assert first_label.user_id == "user_123"
    assert first_label.created_at == "2024-01-15T10:00:00.000Z"
    assert first_label.updated_at == "2024-01-20T15:30:00.000Z"
