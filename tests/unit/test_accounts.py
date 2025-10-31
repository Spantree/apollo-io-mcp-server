"""
Unit tests for Apollo.io account operations using mocked responses.

These tests use respx to mock httpx requests and anonymized fixtures.
They run by default without requiring API credentials.
"""
import pytest
import respx
from httpx import Response
from apollo_client import ApolloClient
from tests.fixtures import (
    ACCOUNTS_SEARCH_NO_RESULTS,
    ACCOUNTS_SEARCH_WITH_RESULTS,
    ACCOUNT_CREATE_RESPONSE,
    ACCOUNT_UPDATE_RESPONSE,
    ACCOUNT_BULK_CREATE_RESPONSE,
    ACCOUNT_BULK_UPDATE_RESPONSE,
)


@respx.mock
async def test_account_search_no_results_unit():
    """
    Test searching for accounts with no results (unit test with mocked response).

    Validates that the client correctly handles empty search results.
    """
    # Mock the API response
    respx.get("https://api.apollo.io/api/v1/accounts/search").mock(
        return_value=Response(200, json=ACCOUNTS_SEARCH_NO_RESULTS)
    )

    client = ApolloClient(api_key="test_api_key")

    # Search for accounts
    result = await client.account_search(
        query="nonexistentaccount.com",
        page=1,
        per_page=25
    )

    # Validate response structure
    assert result is not None
    assert hasattr(result, 'accounts')
    assert hasattr(result, 'pagination')
    assert isinstance(result.accounts, list)
    assert len(result.accounts) == 0
    assert result.pagination.page == 1
    assert result.pagination.per_page == 25
    assert result.pagination.total_entries == 0
    assert result.pagination.total_pages == 0


@respx.mock
async def test_account_search_with_results_unit():
    """
    Test searching for accounts with results (unit test with mocked response).

    Validates that the client correctly parses account data and pagination.
    """
    # Mock the API response
    respx.get("https://api.apollo.io/api/v1/accounts/search").mock(
        return_value=Response(200, json=ACCOUNTS_SEARCH_WITH_RESULTS)
    )

    client = ApolloClient(api_key="test_api_key")

    # Search for accounts
    result = await client.account_search(
        query="example",
        page=1,
        per_page=25
    )

    # Validate response structure
    assert result is not None
    assert hasattr(result, 'accounts')
    assert hasattr(result, 'pagination')
    assert isinstance(result.accounts, list)
    assert len(result.accounts) == 2
    assert result.pagination.page == 1
    assert result.pagination.per_page == 25
    assert result.pagination.total_entries == 2
    assert result.pagination.total_pages == 1

    # Validate first account
    account = result.accounts[0]
    assert account["id"] == "account_123"
    assert account["name"] == "Example Corp"
    assert account["domain"] == "example.com"
    assert "Enterprise Clients" in account["label_names"]


@respx.mock
async def test_account_create_unit():
    """
    Test creating a new account (unit test with mocked response).

    Validates that the client correctly handles account creation.
    """
    # Mock the API response
    respx.post("https://api.apollo.io/api/v1/accounts").mock(
        return_value=Response(200, json=ACCOUNT_CREATE_RESPONSE)
    )

    client = ApolloClient(api_key="test_api_key")

    # Create account
    result = await client.account_create(
        name="New Corp",
        domain="newcorp.com",
        phone="+1-555-0300",
        label_names=["New Accounts"]
    )

    # Validate response
    assert result is not None
    assert hasattr(result, 'account')
    assert result.account["id"] == "account_789"
    assert result.account["name"] == "New Corp"
    assert result.account["domain"] == "newcorp.com"
    assert "New Accounts" in result.account["label_names"]


@respx.mock
async def test_account_update_unit():
    """
    Test updating an existing account (unit test with mocked response).

    Validates that the client correctly handles account updates.
    """
    # Mock the API response
    respx.patch("https://api.apollo.io/api/v1/accounts/account_123").mock(
        return_value=Response(200, json=ACCOUNT_UPDATE_RESPONSE)
    )

    client = ApolloClient(api_key="test_api_key")

    # Update account
    result = await client.account_update(
        account_id="account_123",
        name="Example Corp Updated",
        label_names=["Enterprise Clients", "High Priority"]
    )

    # Validate response
    assert result is not None
    assert hasattr(result, 'account')
    assert result.account["id"] == "account_123"
    assert result.account["name"] == "Example Corp Updated"
    assert "High Priority" in result.account["label_names"]


@respx.mock
async def test_account_bulk_create_unit():
    """
    Test bulk creating accounts (unit test with mocked response).

    Validates that the client correctly handles bulk account creation.
    """
    # Mock the API response
    respx.post("https://api.apollo.io/api/v1/accounts/bulk_create").mock(
        return_value=Response(200, json=ACCOUNT_BULK_CREATE_RESPONSE)
    )

    client = ApolloClient(api_key="test_api_key")

    # Bulk create accounts
    accounts_data = [
        {"name": "Bulk Corp 1", "domain": "bulkcorp1.com"},
        {"name": "Bulk Corp 2", "domain": "bulkcorp2.com"},
        {"name": "Example Corp", "domain": "example.com"}  # Existing
    ]

    result = await client.account_bulk_create(accounts=accounts_data)

    # Validate response
    assert result is not None
    assert hasattr(result, 'created_accounts')
    assert hasattr(result, 'existing_accounts')
    assert len(result.created_accounts) == 2
    assert len(result.existing_accounts) == 1
    assert result.created_accounts[0]["name"] == "Bulk Corp 1"
    assert result.existing_accounts[0]["id"] == "account_123"


@respx.mock
async def test_account_bulk_update_unit():
    """
    Test bulk updating accounts (unit test with mocked response).

    Validates that the client correctly handles bulk account updates.
    """
    # Mock the API response
    respx.post("https://api.apollo.io/api/v1/accounts/bulk_update").mock(
        return_value=Response(200, json=ACCOUNT_BULK_UPDATE_RESPONSE)
    )

    client = ApolloClient(api_key="test_api_key")

    # Bulk update accounts
    updates = [
        {
            "id": "account_123",
            "label_names": ["Enterprise Clients", "Q1 Targets"]
        },
        {
            "id": "account_456",
            "label_names": ["Target Accounts", "Q1 Targets"]
        }
    ]

    result = await client.account_bulk_update(accounts=updates)

    # Validate response
    assert result is not None
    assert hasattr(result, 'accounts')
    assert len(result.accounts) == 2
    assert "Q1 Targets" in result.accounts[0]["label_names"]
    assert "Q1 Targets" in result.accounts[1]["label_names"]
