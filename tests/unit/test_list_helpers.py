"""
Unit tests for account list helper methods (add/remove from list).

NOTE: These tests are now deprecated. The account_add_to_list and
account_remove_from_list functions have been refactored to use a caching
approach instead of search-based lookups.

See tests/tools/test_accounts.py::test_mcp_account_list_management_workflow
for comprehensive integration testing of the list management functionality.
"""
import pytest


@pytest.mark.skip(reason="Tests deprecated - see integration tests in tests/tools/")
async def test_account_list_helpers_deprecated():
    """
    List helper unit tests have been deprecated.

    The implementation was refactored from search-based to GET + caching approach.
    Integration tests now provide comprehensive coverage.
    """
    pass
