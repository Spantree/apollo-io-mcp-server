"""
Integration tests for Apollo.io account MCP tools.

These tests call the MCP tool functions directly from server.py
to validate the full tool behavior (not just the client).

Tests make real API calls and record them with VCR.py.
Cassettes are stored in .scratch/http-tests/ (not committed).

To run these tests:
    pytest -m integration tests/test_integration_accounts_tools.py

By default, these tests are skipped (see pyproject.toml).
"""
import pytest
import vcr
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment before importing server
load_dotenv()
load_dotenv('.env.secrets')

# Import MCP tool functions from server
from server import (
    account_search,
    account_create,
    account_update,
    account_bulk_create,
    account_bulk_update,
    account_add_to_list,
    account_remove_from_list,
)


# VCR configuration for all tests
vcr_config = vcr.VCR(
    cassette_library_dir=".scratch/http-tests",
    record_mode="once",  # Record once, then replay
    match_on=["method", "uri"],
    filter_headers=[("x-api-key", "REDACTED")],
    decode_compressed_response=True,
)


@pytest.mark.integration
async def test_tool_account_search_no_results():
    """
    Test the account_search MCP tool with a query unlikely to have results.

    This validates the full MCP tool behavior including:
    - Parameter handling
    - API client interaction
    - Response structure
    """
    with vcr_config.use_cassette("tool_accounts_search_no_results.yaml"):
        # Call the MCP tool directly
        result = await account_search(
            query="nonexistentaccount12345.com",
            page=1,
            per_page=25
        )

        # Should return successful response even with no results
        assert result is not None
        assert "accounts" in result
        assert "pagination" in result
        assert isinstance(result["accounts"], list)
        assert result["pagination"]["page"] == 1


@pytest.mark.integration
async def test_tool_account_search_with_results():
    """
    Test the account_search MCP tool with results.

    Validates response structure and data types from the tool.
    """
    with vcr_config.use_cassette("tool_accounts_search_with_results.yaml"):
        # Call the MCP tool directly
        result = await account_search(
            page=1,
            per_page=5
        )

        # Validate response structure
        assert result is not None
        assert "accounts" in result
        assert "pagination" in result
        assert isinstance(result["accounts"], list)

        # If there are results, validate structure
        if len(result["accounts"]) > 0:
            account = result["accounts"][0]
            assert "id" in account
            assert "name" in account


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and creates real data")
async def test_tool_account_create():
    """
    Test the account_create MCP tool (integration test).

    IMPORTANT: This test creates real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("tool_account_create.yaml"):
        # Call the MCP tool directly
        result = await account_create(
            name="MCP Tool Test Account",
            domain="mcptooltest.example.com",
            label_names=["MCP Tool Test"]
        )

        # Validate response
        assert result is not None
        assert "account" in result
        assert result["account"]["name"] == "MCP Tool Test Account"


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and modifies real data")
async def test_tool_account_update():
    """
    Test the account_update MCP tool (integration test).

    IMPORTANT: This test modifies real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("tool_account_update.yaml"):
        # First, search for an account to update
        search_result = await account_search(
            query="MCP Tool Test",
            page=1,
            per_page=1
        )

        if len(search_result["accounts"]) > 0:
            account_id = search_result["accounts"][0]["id"]

            # Update the account using the tool
            result = await account_update(
                account_id=account_id,
                phone="+1-555-TOOL-TEST"
            )

            # Validate response
            assert result is not None
            assert "account" in result
            assert result["account"]["id"] == account_id


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and creates real data")
async def test_tool_account_bulk_create():
    """
    Test the account_bulk_create MCP tool (integration test).

    IMPORTANT: This test creates real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("tool_account_bulk_create.yaml"):
        # Call the MCP tool directly
        accounts = [
            {"name": "MCP Tool Bulk Test 1", "domain": "mcptoolbulk1.example.com"},
            {"name": "MCP Tool Bulk Test 2", "domain": "mcptoolbulk2.example.com"}
        ]

        result = await account_bulk_create(accounts=accounts)

        # Validate response
        assert result is not None
        assert "created_accounts" in result
        assert "existing_accounts" in result
        assert len(result["created_accounts"]) >= 0


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and modifies real data")
async def test_tool_account_bulk_update():
    """
    Test the account_bulk_update MCP tool (integration test).

    IMPORTANT: This test modifies real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("tool_account_bulk_update.yaml"):
        # First, find some accounts
        search_result = await account_search(
            query="MCP",
            page=1,
            per_page=2
        )

        if len(search_result["accounts"]) > 0:
            updates = [
                {
                    "id": acc["id"],
                    "label_names": acc.get("label_names", []) + ["Bulk Updated"]
                }
                for acc in search_result["accounts"][:2]
            ]

            # Perform bulk update using the tool
            result = await account_bulk_update(accounts=updates)

            # Validate response
            assert result is not None
            assert "accounts" in result
            assert len(result["accounts"]) > 0


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and modifies real data")
async def test_tool_account_add_to_list():
    """
    Test the account_add_to_list MCP tool helper (integration test).

    This validates the full workflow:
    1. Tool fetches current account labels
    2. Tool merges new label with existing labels
    3. Tool performs bulk update
    4. Tool returns detailed results

    IMPORTANT: This test modifies real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("tool_account_add_to_list.yaml"):
        # First, find some accounts
        search_result = await account_search(
            query="MCP",
            page=1,
            per_page=2
        )

        if len(search_result["accounts"]) > 0:
            account_ids = [acc["id"] for acc in search_result["accounts"][:2]]

            # Add accounts to a test list using the tool
            result = await account_add_to_list(
                account_ids=account_ids,
                label_name="MCP Tool Integration Test"
            )

            # Validate response structure
            assert result is not None
            assert "found_ids" in result
            assert "not_found_ids" in result
            assert "updated_accounts" in result
            assert "total_requested" in result
            assert len(result["found_ids"]) > 0

            # Validate accounts have the new label
            for account in result["updated_accounts"]:
                assert "MCP Tool Integration Test" in account.get("label_names", [])


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and modifies real data")
async def test_tool_account_remove_from_list():
    """
    Test the account_remove_from_list MCP tool helper (integration test).

    This validates the full workflow:
    1. Tool fetches current account labels
    2. Tool removes specified label while preserving others
    3. Tool performs bulk update
    4. Tool returns detailed results

    IMPORTANT: This test modifies real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("tool_account_remove_from_list.yaml"):
        # First, find some accounts
        search_result = await account_search(
            query="MCP",
            page=1,
            per_page=2
        )

        if len(search_result["accounts"]) > 0:
            account_ids = [acc["id"] for acc in search_result["accounts"][:2]]

            # Remove accounts from test list using the tool
            result = await account_remove_from_list(
                account_ids=account_ids,
                label_name="MCP Tool Integration Test"
            )

            # Validate response structure
            assert result is not None
            assert "found_ids" in result
            assert "not_found_ids" in result
            assert "updated_accounts" in result

            # Validate label was removed
            for account in result["updated_accounts"]:
                assert "MCP Tool Integration Test" not in account.get("label_names", [])


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and modifies real data")
async def test_tool_add_to_list_preserves_existing_labels():
    """
    Test that account_add_to_list preserves existing labels (critical behavior).

    This is the key functionality that makes this helper tool valuable:
    it prevents label loss when adding accounts to lists.
    """
    with vcr_config.use_cassette("tool_add_to_list_preserves_labels.yaml"):
        # Find an account with existing labels
        search_result = await account_search(page=1, per_page=1)

        if len(search_result["accounts"]) > 0:
            account = search_result["accounts"][0]
            account_id = account["id"]
            original_labels = set(account.get("label_names", []))

            # Add to a new list
            result = await account_add_to_list(
                account_ids=[account_id],
                label_name="Preservation Test List"
            )

            # Validate original labels are preserved
            updated_account = result["updated_accounts"][0]
            updated_labels = set(updated_account.get("label_names", []))

            # Original labels should still be present
            assert original_labels.issubset(updated_labels), \
                "Original labels were lost when adding to list!"

            # New label should be added
            assert "Preservation Test List" in updated_labels


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and modifies real data")
async def test_tool_remove_from_list_preserves_other_labels():
    """
    Test that account_remove_from_list preserves other labels (critical behavior).

    This validates that only the specified label is removed.
    """
    with vcr_config.use_cassette("tool_remove_from_list_preserves_labels.yaml"):
        # Find an account with multiple labels
        search_result = await account_search(page=1, per_page=10)

        # Find an account with at least 2 labels
        multi_label_account = None
        for account in search_result["accounts"]:
            if len(account.get("label_names", [])) >= 2:
                multi_label_account = account
                break

        if multi_label_account:
            account_id = multi_label_account["id"]
            original_labels = multi_label_account.get("label_names", [])
            label_to_remove = original_labels[0]
            labels_to_keep = set(original_labels[1:])

            # Remove one label
            result = await account_remove_from_list(
                account_ids=[account_id],
                label_name=label_to_remove
            )

            # Validate other labels are preserved
            updated_account = result["updated_accounts"][0]
            updated_labels = set(updated_account.get("label_names", []))

            # Removed label should be gone
            assert label_to_remove not in updated_labels, \
                "Label was not removed!"

            # Other labels should be preserved
            assert labels_to_keep.issubset(updated_labels), \
                "Other labels were lost when removing from list!"
