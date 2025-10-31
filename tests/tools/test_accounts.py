"""
MCP tool tests for Apollo.io account tools.

These tests validate the complete MCP tool integration for all 7 account tools:
1. account_search - Search saved accounts
2. account_create - Create new account
3. account_update - Update existing account
4. account_bulk_create - Bulk create accounts
5. account_bulk_update - Bulk update accounts
6. account_add_to_list - Add accounts to list (helper)
7. account_remove_from_list - Remove accounts from list (helper)

Testing pattern: mcp.call_tool(name, arguments)
This tests: registration → argument parsing → execution → response formatting

Tests make real API calls and record them with VCR.py.
Cassettes are stored in .scratch/http-tests/ (not committed).

To run these tests:
    pytest tests/tools/test_accounts.py -m integration

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

    Validates:
    - MCP argument parsing for account creation
    - Account creation with name, domain, and labels
    - Response structure with created account

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
        assert result["account"]["domain"] == "mcptooltest.example.com"


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and modifies real data")
async def test_mcp_account_update():
    """
    Test the account_update MCP tool.

    Validates:
    - MCP argument parsing for account updates
    - Account update with partial data (phone number)
    - Response structure with updated account

    IMPORTANT: This test modifies real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("mcp_account_update.yaml"):
        # First, search for an account to update
        search_result = await mcp.call_tool(
            "account_search",
            {"query": "MCP Tool Test", "page": 1, "per_page": 1}
        )

        if len(search_result["accounts"]) > 0:
            account_id = search_result["accounts"][0]["id"]

            # Update the account via MCP tool
            result = await mcp.call_tool(
                "account_update",
                {
                    "account_id": account_id,
                    "phone": "+1-555-MCP-TOOL"
                }
            )

            # Validate response
            assert result is not None
            assert "account" in result
            assert result["account"]["id"] == account_id
            assert result["account"]["phone"] == "+1-555-MCP-TOOL"


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and creates real data")
async def test_mcp_account_bulk_create():
    """
    Test the account_bulk_create MCP tool.

    Validates:
    - MCP argument parsing for bulk account creation
    - Bulk creation of multiple accounts (2-3 accounts)
    - Response structure with created_accounts and existing_accounts arrays
    - Proper handling of duplicate domains

    IMPORTANT: This test creates real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("mcp_account_bulk_create.yaml"):
        # Create multiple accounts via MCP tool
        accounts = [
            {
                "name": "MCP Bulk Test 1",
                "domain": "mcpbulk1.example.com",
                "label_names": ["Bulk Test"]
            },
            {
                "name": "MCP Bulk Test 2",
                "domain": "mcpbulk2.example.com",
                "label_names": ["Bulk Test"]
            }
        ]

        result = await mcp.call_tool(
            "account_bulk_create",
            {"accounts": accounts}
        )

        # Validate response structure
        assert result is not None
        assert "created_accounts" in result
        assert "existing_accounts" in result
        assert isinstance(result["created_accounts"], list)
        assert isinstance(result["existing_accounts"], list)


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and modifies real data")
async def test_mcp_account_bulk_update():
    """
    Test the account_bulk_update MCP tool.

    Validates:
    - MCP argument parsing for bulk account updates
    - Bulk update of multiple accounts
    - Response structure with updated accounts array
    - Label updates across multiple accounts

    IMPORTANT: This test modifies real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("mcp_account_bulk_update.yaml"):
        # First, search for some accounts to update
        search_result = await mcp.call_tool(
            "account_search",
            {"query": "MCP", "page": 1, "per_page": 2}
        )

        if len(search_result["accounts"]) >= 2:
            # Prepare bulk updates
            updates = [
                {
                    "id": search_result["accounts"][0]["id"],
                    "label_names": search_result["accounts"][0].get("label_names", []) + ["Bulk Updated"]
                },
                {
                    "id": search_result["accounts"][1]["id"],
                    "label_names": search_result["accounts"][1].get("label_names", []) + ["Bulk Updated"]
                }
            ]

            # Perform bulk update via MCP tool
            result = await mcp.call_tool(
                "account_bulk_update",
                {"accounts": updates}
            )

            # Validate response
            assert result is not None
            assert "accounts" in result
            assert len(result["accounts"]) == 2
            for account in result["accounts"]:
                assert "Bulk Updated" in account.get("label_names", [])


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
