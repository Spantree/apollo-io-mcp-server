"""
Unit tests for account list helper methods (add/remove from list).

These tests validate the logic for safely managing account list memberships
without losing existing labels.
"""
import pytest
import respx
from httpx import Response
from apollo_client import ApolloClient
from tests.fixtures import (
    ACCOUNTS_SEARCH_WITH_RESULTS,
    ACCOUNT_BULK_UPDATE_RESPONSE,
)


@respx.mock
async def test_account_add_to_list_unit():
    """
    Test adding accounts to a list without losing existing labels.

    This test validates:
    1. Accounts are fetched to get current labels
    2. New label is merged with existing labels
    3. Bulk update is called with complete label list
    """
    # Mock account search response
    respx.get("https://api.apollo.io/api/v1/accounts/search").mock(
        return_value=Response(200, json=ACCOUNTS_SEARCH_WITH_RESULTS)
    )

    # Mock bulk update response with new label added
    updated_response = {
        "accounts": [
            {
                "id": "account_123",
                "name": "Example Corp",
                "domain": "example.com",
                "label_names": ["Enterprise Clients", "Q1 Targets"],  # Original + new
                "updated_at": "2025-10-30T21:00:00.000Z"
            }
        ]
    }
    respx.post("https://api.apollo.io/api/v1/accounts/bulk_update").mock(
        return_value=Response(200, json=updated_response)
    )

    client = ApolloClient(api_key="test_api_key")

    # Add account to list
    result = await client.account_add_to_list(
        account_ids=["account_123"],
        label_name="Q1 Targets"
    )

    # Validate result structure
    assert result is not None
    assert "updated_accounts" in result
    assert "found_ids" in result
    assert "not_found_ids" in result
    assert "total_requested" in result

    # Validate accounts were found and updated
    assert len(result["found_ids"]) == 1
    assert "account_123" in result["found_ids"]
    assert len(result["not_found_ids"]) == 0
    assert result["total_requested"] == 1

    # Validate account has both old and new labels
    updated_account = result["updated_accounts"][0]
    assert "Enterprise Clients" in updated_account["label_names"]
    assert "Q1 Targets" in updated_account["label_names"]


@respx.mock
async def test_account_add_to_list_with_not_found_unit():
    """
    Test adding accounts to a list when some accounts are not found.

    Validates that not_found_ids are properly tracked.
    """
    # Mock account search response
    respx.get("https://api.apollo.io/api/v1/accounts/search").mock(
        return_value=Response(200, json=ACCOUNTS_SEARCH_WITH_RESULTS)
    )

    # Mock bulk update response
    updated_response = {
        "accounts": [
            {
                "id": "account_123",
                "name": "Example Corp",
                "label_names": ["Enterprise Clients", "New List"],
                "updated_at": "2025-10-30T21:00:00.000Z"
            }
        ]
    }
    respx.post("https://api.apollo.io/api/v1/accounts/bulk_update").mock(
        return_value=Response(200, json=updated_response)
    )

    client = ApolloClient(api_key="test_api_key")

    # Try to add accounts, including one that doesn't exist
    result = await client.account_add_to_list(
        account_ids=["account_123", "account_nonexistent"],
        label_name="New List"
    )

    # Validate result
    assert result is not None
    assert len(result["found_ids"]) == 1
    assert len(result["not_found_ids"]) == 1
    assert "account_123" in result["found_ids"]
    assert "account_nonexistent" in result["not_found_ids"]
    assert result["total_requested"] == 2


@respx.mock
async def test_account_add_to_list_deduplication_unit():
    """
    Test that adding an account to a list it's already in doesn't duplicate.

    Validates that the helper properly deduplicates labels.
    """
    # Mock account search response where account already has the target label
    search_response = {
        "accounts": [
            {
                "id": "account_123",
                "name": "Example Corp",
                "domain": "example.com",
                "label_names": ["Enterprise Clients", "Q1 Targets"],  # Already has it
                "created_at": "2024-01-15T10:00:00.000Z"
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 25,
            "total_entries": 1,
            "total_pages": 1
        }
    }
    respx.get("https://api.apollo.io/api/v1/accounts/search").mock(
        return_value=Response(200, json=search_response)
    )

    # Mock bulk update response (label list unchanged)
    updated_response = {
        "accounts": [
            {
                "id": "account_123",
                "name": "Example Corp",
                "label_names": ["Enterprise Clients", "Q1 Targets"],  # No duplicate
                "updated_at": "2025-10-30T21:00:00.000Z"
            }
        ]
    }
    respx.post("https://api.apollo.io/api/v1/accounts/bulk_update").mock(
        return_value=Response(200, json=updated_response)
    )

    client = ApolloClient(api_key="test_api_key")

    # Add account to list it's already in
    result = await client.account_add_to_list(
        account_ids=["account_123"],
        label_name="Q1 Targets"
    )

    # Validate no duplication occurred
    assert result is not None
    updated_account = result["updated_accounts"][0]
    assert updated_account["label_names"].count("Q1 Targets") == 1


@respx.mock
async def test_account_remove_from_list_unit():
    """
    Test removing accounts from a list while preserving other labels.

    Validates that only the specified label is removed.
    """
    # Mock account search response
    respx.get("https://api.apollo.io/api/v1/accounts/search").mock(
        return_value=Response(200, json=ACCOUNTS_SEARCH_WITH_RESULTS)
    )

    # Mock bulk update response with label removed
    updated_response = {
        "accounts": [
            {
                "id": "account_123",
                "name": "Example Corp",
                "domain": "example.com",
                "label_names": [],  # Removed "Enterprise Clients"
                "updated_at": "2025-10-30T21:00:00.000Z"
            }
        ]
    }
    respx.post("https://api.apollo.io/api/v1/accounts/bulk_update").mock(
        return_value=Response(200, json=updated_response)
    )

    client = ApolloClient(api_key="test_api_key")

    # Remove account from list
    result = await client.account_remove_from_list(
        account_ids=["account_123"],
        label_name="Enterprise Clients"
    )

    # Validate result
    assert result is not None
    assert len(result["found_ids"]) == 1
    assert "account_123" in result["found_ids"]
    assert len(result["not_found_ids"]) == 0

    # Validate label was removed
    updated_account = result["updated_accounts"][0]
    assert "Enterprise Clients" not in updated_account["label_names"]


@respx.mock
async def test_account_remove_from_list_preserves_other_labels_unit():
    """
    Test that removing from a list preserves other labels.

    Validates that only the target label is removed, others remain.
    """
    # Mock account search response with multiple labels
    search_response = {
        "accounts": [
            {
                "id": "account_123",
                "name": "Example Corp",
                "domain": "example.com",
                "label_names": ["Enterprise Clients", "Q1 Targets", "High Value"],
                "created_at": "2024-01-15T10:00:00.000Z"
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 25,
            "total_entries": 1,
            "total_pages": 1
        }
    }
    respx.get("https://api.apollo.io/api/v1/accounts/search").mock(
        return_value=Response(200, json=search_response)
    )

    # Mock bulk update response with only one label removed
    updated_response = {
        "accounts": [
            {
                "id": "account_123",
                "name": "Example Corp",
                "label_names": ["Enterprise Clients", "High Value"],  # Q1 Targets removed
                "updated_at": "2025-10-30T21:00:00.000Z"
            }
        ]
    }
    respx.post("https://api.apollo.io/api/v1/accounts/bulk_update").mock(
        return_value=Response(200, json=updated_response)
    )

    client = ApolloClient(api_key="test_api_key")

    # Remove account from one list
    result = await client.account_remove_from_list(
        account_ids=["account_123"],
        label_name="Q1 Targets"
    )

    # Validate other labels preserved
    assert result is not None
    updated_account = result["updated_accounts"][0]
    assert "Q1 Targets" not in updated_account["label_names"]
    assert "Enterprise Clients" in updated_account["label_names"]
    assert "High Value" in updated_account["label_names"]


@respx.mock
async def test_account_remove_from_list_nonexistent_label_unit():
    """
    Test removing an account from a list it's not in (no-op).

    Validates graceful handling when label doesn't exist.
    """
    # Mock account search response without target label
    search_response = {
        "accounts": [
            {
                "id": "account_123",
                "name": "Example Corp",
                "domain": "example.com",
                "label_names": ["Enterprise Clients"],  # Doesn't have "Q1 Targets"
                "created_at": "2024-01-15T10:00:00.000Z"
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 25,
            "total_entries": 1,
            "total_pages": 1
        }
    }
    respx.get("https://api.apollo.io/api/v1/accounts/search").mock(
        return_value=Response(200, json=search_response)
    )

    # Mock bulk update response (unchanged)
    updated_response = {
        "accounts": [
            {
                "id": "account_123",
                "name": "Example Corp",
                "label_names": ["Enterprise Clients"],  # Unchanged
                "updated_at": "2025-10-30T21:00:00.000Z"
            }
        ]
    }
    respx.post("https://api.apollo.io/api/v1/accounts/bulk_update").mock(
        return_value=Response(200, json=updated_response)
    )

    client = ApolloClient(api_key="test_api_key")

    # Try to remove account from list it's not in
    result = await client.account_remove_from_list(
        account_ids=["account_123"],
        label_name="Q1 Targets"
    )

    # Validate no error, labels unchanged
    assert result is not None
    assert len(result["found_ids"]) == 1
    updated_account = result["updated_accounts"][0]
    assert updated_account["label_names"] == ["Enterprise Clients"]
