"""
MCP tool tests for Apollo.io contact tools.

These tests validate the complete MCP tool integration for contact list management:
1. contact_add_to_list - Add contacts to list (helper)
2. contact_remove_from_list - Remove contacts from list (helper)

Testing pattern: mcp.call_tool(name, arguments)
This tests: registration → argument parsing → execution → response formatting

Tests make real API calls and record them with VCR.py.
Cassettes are stored in .scratch/http-tests/ (not committed).

To run these tests:
    pytest tests/tools/test_contacts.py -m integration

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
@pytest.mark.skip(reason="Requires master API key and creates/modifies real data")
async def test_mcp_contact_list_management_workflow():
    """
    Comprehensive test of contact list management workflow.

    This test validates the complete lifecycle of managing contacts across multiple lists:
    1. Create three test contacts
    2. Add two contacts to "List A"
    3. Remove one contact from "List A" (validate the other remains)
    4. Add all three contacts to "List B" (validate List A membership preserved)
    5. Validate final state of all contacts

    This tests the critical behavior:
    - contact_add_to_list preserves existing labels
    - contact_remove_from_list only removes specified label
    - Multiple list memberships can coexist
    - List operations don't interfere with each other

    IMPORTANT: This test creates and modifies real data in your Apollo account.
    Only run with a test account and master API key.
    """
    with vcr_config.use_cassette("mcp_contact_list_workflow.yaml"):
        # STEP 1: Create three test contacts
        import time
        timestamp = int(time.time())

        test_contacts = [
            {
                "first_name": "List",
                "last_name": f"TestContact1 {timestamp}",
                "email": f"listtest1-{timestamp}@example.com",
                "label_names": ["Test Baseline"]  # Create with a baseline label
            },
            {
                "first_name": "List",
                "last_name": f"TestContact2 {timestamp}",
                "email": f"listtest2-{timestamp}@example.com",
                "label_names": ["Test Baseline"]
            },
            {
                "first_name": "List",
                "last_name": f"TestContact3 {timestamp}",
                "email": f"listtest3-{timestamp}@example.com",
                "label_names": ["Test Baseline"]
            }
        ]

        create_result = parse_mcp_response(await mcp.call_tool(
            "contact_bulk_create",
            {"contacts": test_contacts}
        ))

        assert create_result is not None
        assert "created_contacts" in create_result
        created = create_result["created_contacts"]
        assert len(created) == 3, "Should have created 3 contacts"

        # Extract contact IDs
        contact1_id = created[0]["id"]
        contact2_id = created[1]["id"]
        contact3_id = created[2]["id"]

        print(f"\n✓ Created 3 test contacts: {contact1_id}, {contact2_id}, {contact3_id}")

        # Wait a moment for contacts to be fully indexed
        import asyncio
        await asyncio.sleep(2)

        # STEP 2: Add contacts 1 and 2 to "List A"
        add_to_list_a_result = parse_mcp_response(await mcp.call_tool(
            "contact_add_to_list",
            {
                "contact_ids": [contact1_id, contact2_id],
                "label_name": "List A Test"
            }
        ))

        assert add_to_list_a_result is not None
        assert len(add_to_list_a_result["found_ids"]) == 2
        assert contact1_id in add_to_list_a_result["found_ids"]
        assert contact2_id in add_to_list_a_result["found_ids"]

        # Verify both contacts have "List A Test" label
        for contact in add_to_list_a_result["updated_contacts"]:
            assert "List A Test" in contact["label_names"], \
                f"Contact {contact['id']} should have 'List A Test' label"

        print(f"✓ Added contacts 1 and 2 to 'List A Test'")

        # STEP 3: Remove contact 2 from "List A" (contact 1 should remain)
        remove_from_list_a_result = parse_mcp_response(await mcp.call_tool(
            "contact_remove_from_list",
            {
                "contact_ids": [contact2_id],
                "label_name": "List A Test"
            }
        ))

        assert remove_from_list_a_result is not None
        assert len(remove_from_list_a_result["found_ids"]) == 1
        assert contact2_id in remove_from_list_a_result["found_ids"]

        # Verify contact 2 no longer has "List A Test" label
        removed_contact = remove_from_list_a_result["updated_contacts"][0]
        assert "List A Test" not in removed_contact.get("label_names", []), \
            "Contact 2 should not have 'List A Test' label after removal"

        print(f"✓ Removed contact 2 from 'List A Test'")

        # STEP 4: Add all three contacts to "List B"
        add_to_list_b_result = parse_mcp_response(await mcp.call_tool(
            "contact_add_to_list",
            {
                "contact_ids": [contact1_id, contact2_id, contact3_id],
                "label_name": "List B Test"
            }
        ))

        assert add_to_list_b_result is not None
        assert len(add_to_list_b_result["found_ids"]) == 3
        assert contact1_id in add_to_list_b_result["found_ids"]
        assert contact2_id in add_to_list_b_result["found_ids"]
        assert contact3_id in add_to_list_b_result["found_ids"]

        # Verify all three contacts have "List B Test" label
        for contact in add_to_list_b_result["updated_contacts"]:
            assert "List B Test" in contact["label_names"], \
                f"Contact {contact['id']} should have 'List B Test' label"

        print(f"✓ Added all 3 contacts to 'List B Test'")

        # STEP 5: Validate final state based on helper responses
        # Contact 1 should have both "List A Test" and "List B Test"
        # Contact 2 should have only "List B Test" and "Test Baseline"
        # Contact 3 should have only "List B Test" and "Test Baseline"

        # Build a map from the responses we received
        contact_labels = {}
        for contact in add_to_list_b_result["updated_contacts"]:
            contact_labels[contact["id"]] = contact["label_names"]

        # Validate Contact 1: Should have Test Baseline, List A, and List B
        assert "List A Test" in contact_labels[contact1_id], \
            "Contact 1 should have 'List A Test' label"
        assert "List B Test" in contact_labels[contact1_id], \
            "Contact 1 should have 'List B Test' label"
        assert "Test Baseline" in contact_labels[contact1_id], \
            "Contact 1 should have 'Test Baseline' label"
        print(f"✓ Contact 1 has 'Test Baseline', 'List A Test', and 'List B Test' labels")

        # Validate Contact 2: Should have Test Baseline and List B (removed from List A)
        assert "List A Test" not in contact_labels[contact2_id], \
            "Contact 2 should NOT have 'List A Test' label (was removed)"
        assert "List B Test" in contact_labels[contact2_id], \
            "Contact 2 should have 'List B Test' label"
        assert "Test Baseline" in contact_labels[contact2_id], \
            "Contact 2 should have 'Test Baseline' label"
        print(f"✓ Contact 2 has 'Test Baseline' and 'List B Test' labels (List A was removed)")

        # Validate Contact 3: Should have Test Baseline and List B (never added to List A)
        assert "List A Test" not in contact_labels[contact3_id], \
            "Contact 3 should NOT have 'List A Test' label (never added)"
        assert "List B Test" in contact_labels[contact3_id], \
            "Contact 3 should have 'List B Test' label"
        assert "Test Baseline" in contact_labels[contact3_id], \
            "Contact 3 should have 'Test Baseline' label"
        print(f"✓ Contact 3 has 'Test Baseline' and 'List B Test' labels (never added to List A)")

        print("\n✓ Complete workflow validated successfully!")
        print(f"  - Contact 1: {sorted(contact_labels[contact1_id])}")
        print(f"  - Contact 2: {sorted(contact_labels[contact2_id])}")
        print(f"  - Contact 3: {sorted(contact_labels[contact3_id])}")
