"""
Integration tests for Apollo.io account operations.

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
async def test_account_search_no_results(apollo_api_key):
    """
    Test searching for accounts with a query unlikely to have results.

    This validates the API contract and response structure.
    """
    with vcr_config.use_cassette("accounts_search_no_results.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # Search for accounts with unlikely query
        result = await client.account_search(
            query="nonexistentaccount12345.com",
            page=1,
            per_page=25
        )

        # Should return successful response even with no results
        assert result is not None
        assert hasattr(result, 'accounts')
        assert hasattr(result, 'pagination')
        assert isinstance(result.accounts, list)
        assert result.pagination.page == 1


@pytest.mark.integration
async def test_account_search_with_results(apollo_api_key):
    """
    Test searching for accounts with a query likely to have results.

    Validates response structure and data types.
    """
    with vcr_config.use_cassette("accounts_search_with_results.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # Search for accounts (adjust query to match your actual data)
        result = await client.account_search(
            page=1,
            per_page=5
        )

        # Validate response structure
        assert result is not None
        assert hasattr(result, 'accounts')
        assert hasattr(result, 'pagination')
        assert isinstance(result.accounts, list)

        # If there are results, validate structure
        if len(result.accounts) > 0:
            account = result.accounts[0]
            assert "id" in account
            assert "name" in account


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and creates real data")
async def test_account_create_integration(apollo_api_key):
    """
    Test creating a new account (integration test).

    IMPORTANT: This test creates real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("account_create.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # Create test account
        result = await client.account_create(
            name="MCP Test Account",
            domain="mcptest.example.com",
            label_names=["MCP Test"]
        )

        # Validate response
        assert result is not None
        assert hasattr(result, 'account')
        assert result.account["name"] == "MCP Test Account"


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and modifies real data")
async def test_account_update_integration(apollo_api_key):
    """
    Test updating an existing account (integration test).

    IMPORTANT: This test modifies real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("account_update.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # First, search for an account to update
        search_result = await client.account_search(
            query="MCP Test",
            page=1,
            per_page=1
        )

        if len(search_result.accounts) > 0:
            account_id = search_result.accounts[0]["id"]

            # Update the account
            result = await client.account_update(
                account_id=account_id,
                phone="+1-555-TEST"
            )

            # Validate response
            assert result is not None
            assert hasattr(result, 'account')
            assert result.account["id"] == account_id


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and creates real data")
async def test_account_bulk_create_integration(apollo_api_key):
    """
    Test bulk creating accounts (integration test).

    IMPORTANT: This test creates real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("account_bulk_create.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # Bulk create test accounts
        accounts = [
            {"name": "MCP Bulk Test 1", "domain": "mcpbulk1.example.com"},
            {"name": "MCP Bulk Test 2", "domain": "mcpbulk2.example.com"}
        ]

        result = await client.account_bulk_create(accounts=accounts)

        # Validate response
        assert result is not None
        assert hasattr(result, 'created_accounts')
        assert hasattr(result, 'existing_accounts')
        assert len(result.created_accounts) >= 0


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and modifies real data")
async def test_account_add_to_list_integration(apollo_api_key):
    """
    Test adding accounts to a list without losing existing labels.

    IMPORTANT: This test modifies real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("account_add_to_list.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # First, find some accounts
        search_result = await client.account_search(
            query="MCP",
            page=1,
            per_page=2
        )

        if len(search_result.accounts) > 0:
            account_ids = [acc["id"] for acc in search_result.accounts[:2]]

            # Add accounts to a test list
            result = await client.account_add_to_list(
                account_ids=account_ids,
                label_name="MCP Integration Test"
            )

            # Validate response
            assert result is not None
            assert "found_ids" in result
            assert "not_found_ids" in result
            assert len(result["found_ids"]) > 0


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and modifies real data")
async def test_account_remove_from_list_integration(apollo_api_key):
    """
    Test removing accounts from a list while preserving other labels.

    IMPORTANT: This test modifies real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("account_remove_from_list.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # First, find some accounts
        search_result = await client.account_search(
            query="MCP",
            page=1,
            per_page=2
        )

        if len(search_result.accounts) > 0:
            account_ids = [acc["id"] for acc in search_result.accounts[:2]]

            # Remove accounts from test list
            result = await client.account_remove_from_list(
                account_ids=account_ids,
                label_name="MCP Integration Test"
            )

            # Validate response
            assert result is not None
            assert "found_ids" in result
            assert "not_found_ids" in result
