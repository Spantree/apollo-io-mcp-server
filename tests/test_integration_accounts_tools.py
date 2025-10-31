"""
Integration tests for Apollo.io account MCP tools using FastMCP's call_tool.

These tests use the proper MCP testing pattern: mcp.call_tool(name, arguments)
This tests the complete integration: registration, argument parsing, execution, and response.

Tests make real API calls and record them with VCR.py.
Cassettes are stored in .scratch/http-tests/ (not committed).

To run these tests:
    pytest -m integration tests/test_integration_accounts_tools.py

By default, these tests are skipped (see pyproject.toml).
"""
import pytest
import vcr
from server import mcp


# VCR configuration for all tests
vcr_config = vcr.VCR(
    cassette_library_dir=".scratch/http-tests",
    record_mode="once",  # Record once, then replay
    match_on=["method", "uri"],
    filter_headers=[("x-api-key", "REDACTED")],
    decode_compressed_response=True,
)


@pytest.mark.integration
async def test_mcp_account_search_no_results():
    """
    Test the account_search MCP tool via mcp.call_tool with no results.

    This tests the full MCP stack including:
    - Tool registration
    - Argument parsing and validation
    - Tool execution
    - Response formatting
    """
    with vcr_config.use_cassette("mcp_accounts_search_no_results.yaml"):
        # Call the MCP tool using the proper testing pattern
        result = await mcp.call_tool(
            "account_search",
            {
                "query": "nonexistentaccount12345.com",
                "page": 1,
                "per_page": 25
            }
        )

        # Should return successful response even with no results
        assert result is not None
        assert "accounts" in result
        assert "pagination" in result
        assert isinstance(result["accounts"], list)
        assert result["pagination"]["page"] == 1


@pytest.mark.integration
async def test_mcp_account_search_with_results():
    """
    Test the account_search MCP tool with results.
    """
    with vcr_config.use_cassette("mcp_accounts_search_with_results.yaml"):
        result = await mcp.call_tool(
            "account_search",
            {
                "page": 1,
                "per_page": 5
            }
        )

        # Validate response structure
        assert result is not None
        assert "accounts" in result
        assert "pagination" in result
        assert isinstance(result["accounts"], list)


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and creates real data")
async def test_mcp_account_create():
    """
    Test the account_create MCP tool.

    IMPORTANT: This test creates real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("mcp_account_create.yaml"):
        result = await mcp.call_tool(
            "account_create",
            {
                "name": "MCP Tool Test Account",
                "domain": "mcptooltest.example.com",
                "label_names": ["MCP Tool Test"]
            }
        )

        # Validate response
        assert result is not None
        assert "account" in result
        assert result["account"]["name"] == "MCP Tool Test Account"


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and modifies real data")
async def test_mcp_account_add_to_list():
    """
    Test the account_add_to_list MCP tool helper.

    This validates the full workflow through the MCP layer:
    1. MCP receives request and parses arguments
    2. Tool fetches current account labels
    3. Tool merges new label with existing labels
    4. Tool performs bulk update
    5. MCP returns formatted response

    IMPORTANT: This test modifies real data in your Apollo account.
    """
    with vcr_config.use_cassette("mcp_account_add_to_list.yaml"):
        # First, search for some accounts
        search_result = await mcp.call_tool(
            "account_search",
            {"query": "MCP", "page": 1, "per_page": 2}
        )

        if len(search_result["accounts"]) > 0:
            account_ids = [acc["id"] for acc in search_result["accounts"][:2]]

            # Add accounts to a test list via MCP
            result = await mcp.call_tool(
                "account_add_to_list",
                {
                    "account_ids": account_ids,
                    "label_name": "MCP Integration Test"
                }
            )

            # Validate response structure
            assert result is not None
            assert "found_ids" in result
            assert "not_found_ids" in result
            assert "updated_accounts" in result
            assert len(result["found_ids"]) > 0

            # Validate accounts have the new label
            for account in result["updated_accounts"]:
                assert "MCP Integration Test" in account.get("label_names", [])


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and modifies real data")
async def test_mcp_account_remove_from_list():
    """
    Test the account_remove_from_list MCP tool helper.

    IMPORTANT: This test modifies real data in your Apollo account.
    """
    with vcr_config.use_cassette("mcp_account_remove_from_list.yaml"):
        # First, search for some accounts
        search_result = await mcp.call_tool(
            "account_search",
            {"query": "MCP", "page": 1, "per_page": 2}
        )

        if len(search_result["accounts"]) > 0:
            account_ids = [acc["id"] for acc in search_result["accounts"][:2]]

            # Remove accounts from test list via MCP
            result = await mcp.call_tool(
                "account_remove_from_list",
                {
                    "account_ids": account_ids,
                    "label_name": "MCP Integration Test"
                }
            )

            # Validate response structure
            assert result is not None
            assert "found_ids" in result
            assert "not_found_ids" in result
            assert "updated_accounts" in result

            # Validate label was removed
            for account in result["updated_accounts"]:
                assert "MCP Integration Test" not in account.get("label_names", [])
