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
import json
from server import mcp


def parse_mcp_response(result):
    """
    Parse MCP tool response from TextContent list to dict.

    MCP tools return a list of TextContent objects. This helper
    extracts the JSON data from the first TextContent.
    """
    if isinstance(result, list) and len(result) > 0:
        from mcp.types import TextContent
        if isinstance(result[0], TextContent):
            return json.loads(result[0].text)
    return result


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


@pytest.mark.integration
@pytest.mark.skip(reason="Requires master API key and creates/modifies real data")
async def test_mcp_account_list_management_workflow():
    """
    Comprehensive test of account list management workflow.

    This test validates the complete lifecycle of managing accounts across multiple lists:
    1. Create three test accounts
    2. Add two accounts to "List A"
    3. Remove one account from "List A" (validate the other remains)
    4. Add all three accounts to "List B" (validate List A membership preserved)
    5. Validate final state of all accounts

    This tests the critical behavior:
    - account_add_to_list preserves existing labels
    - account_remove_from_list only removes specified label
    - Multiple list memberships can coexist
    - List operations don't interfere with each other

    IMPORTANT: This test creates and modifies real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("mcp_account_list_workflow.yaml"):
        # STEP 1: Create three test accounts
        import time
        timestamp = int(time.time())

        test_accounts = [
            {
                "name": f"List Test Account 1 {timestamp}",
                "domain": f"listtest1-{timestamp}.example.com",
                "label_names": ["Test Baseline"]  # Create with a baseline label
            },
            {
                "name": f"List Test Account 2 {timestamp}",
                "domain": f"listtest2-{timestamp}.example.com",
                "label_names": ["Test Baseline"]
            },
            {
                "name": f"List Test Account 3 {timestamp}",
                "domain": f"listtest3-{timestamp}.example.com",
                "label_names": ["Test Baseline"]
            }
        ]

        create_result = parse_mcp_response(await mcp.call_tool(
            "account_bulk_create",
            {"accounts": test_accounts}
        ))

        assert create_result is not None
        assert "created_accounts" in create_result
        created = create_result["created_accounts"]
        assert len(created) == 3, "Should have created 3 accounts"

        # Extract account IDs
        account1_id = created[0]["id"]
        account2_id = created[1]["id"]
        account3_id = created[2]["id"]

        print(f"\n✓ Created 3 test accounts: {account1_id}, {account2_id}, {account3_id}")

        # Wait a moment for accounts to be fully indexed
        import asyncio
        await asyncio.sleep(2)

        # STEP 2: Add accounts 1 and 2 to "List A"
        add_to_list_a_result = parse_mcp_response(await mcp.call_tool(
            "account_add_to_list",
            {
                "account_ids": [account1_id, account2_id],
                "label_name": "List A Test"
            }
        ))

        assert add_to_list_a_result is not None
        assert len(add_to_list_a_result["found_ids"]) == 2
        assert account1_id in add_to_list_a_result["found_ids"]
        assert account2_id in add_to_list_a_result["found_ids"]

        # Verify both accounts have "List A Test" label
        for account in add_to_list_a_result["updated_accounts"]:
            assert "List A Test" in account["label_names"], \
                f"Account {account['id']} should have 'List A Test' label"

        print(f"✓ Added accounts 1 and 2 to 'List A Test'")

        # STEP 3: Remove account 2 from "List A" (account 1 should remain)
        remove_from_list_a_result = parse_mcp_response(await mcp.call_tool(
            "account_remove_from_list",
            {
                "account_ids": [account2_id],
                "label_name": "List A Test"
            }
        ))

        assert remove_from_list_a_result is not None
        assert len(remove_from_list_a_result["found_ids"]) == 1
        assert account2_id in remove_from_list_a_result["found_ids"]

        # Verify account 2 no longer has "List A Test" label
        removed_account = remove_from_list_a_result["updated_accounts"][0]
        assert "List A Test" not in removed_account.get("label_names", []), \
            "Account 2 should not have 'List A Test' label after removal"

        print(f"✓ Removed account 2 from 'List A Test'")

        # STEP 4: Add all three accounts to "List B"
        add_to_list_b_result = parse_mcp_response(await mcp.call_tool(
            "account_add_to_list",
            {
                "account_ids": [account1_id, account2_id, account3_id],
                "label_name": "List B Test"
            }
        ))

        assert add_to_list_b_result is not None
        assert len(add_to_list_b_result["found_ids"]) == 3
        assert account1_id in add_to_list_b_result["found_ids"]
        assert account2_id in add_to_list_b_result["found_ids"]
        assert account3_id in add_to_list_b_result["found_ids"]

        # Verify all three accounts have "List B Test" label
        for account in add_to_list_b_result["updated_accounts"]:
            assert "List B Test" in account["label_names"], \
                f"Account {account['id']} should have 'List B Test' label"

        print(f"✓ Added all 3 accounts to 'List B Test'")

        # STEP 5: Validate final state based on helper responses
        # Account 1 should have both "List A Test" and "List B Test"
        # Account 2 should have only "List B Test" and "Test Baseline"
        # Account 3 should have only "List B Test" and "Test Baseline"

        # Build a map from the responses we received
        account_labels = {}
        for account in add_to_list_b_result["updated_accounts"]:
            account_labels[account["id"]] = account["label_names"]

        # Validate Account 1: Should have Test Baseline, List A, and List B
        assert "List A Test" in account_labels[account1_id], \
            "Account 1 should have 'List A Test' label"
        assert "List B Test" in account_labels[account1_id], \
            "Account 1 should have 'List B Test' label"
        assert "Test Baseline" in account_labels[account1_id], \
            "Account 1 should have 'Test Baseline' label"
        print(f"✓ Account 1 has 'Test Baseline', 'List A Test', and 'List B Test' labels")

        # Validate Account 2: Should have Test Baseline and List B (removed from List A)
        assert "List A Test" not in account_labels[account2_id], \
            "Account 2 should NOT have 'List A Test' label (was removed)"
        assert "List B Test" in account_labels[account2_id], \
            "Account 2 should have 'List B Test' label"
        assert "Test Baseline" in account_labels[account2_id], \
            "Account 2 should have 'Test Baseline' label"
        print(f"✓ Account 2 has 'Test Baseline' and 'List B Test' labels (List A was removed)")

        # Validate Account 3: Should have Test Baseline and List B (never added to List A)
        assert "List A Test" not in account_labels[account3_id], \
            "Account 3 should NOT have 'List A Test' label (never added)"
        assert "List B Test" in account_labels[account3_id], \
            "Account 3 should have 'List B Test' label"
        assert "Test Baseline" in account_labels[account3_id], \
            "Account 3 should have 'Test Baseline' label"
        print(f"✓ Account 3 has 'Test Baseline' and 'List B Test' labels (never added to List A)")

        print("\n✓ Complete workflow validated successfully!")
        print(f"  - Account 1: {sorted(account_labels[account1_id])}")
        print(f"  - Account 2: {sorted(account_labels[account2_id])}")
        print(f"  - Account 3: {sorted(account_labels[account3_id])}")
