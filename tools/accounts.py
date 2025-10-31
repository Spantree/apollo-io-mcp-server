"""
Account CRUD and list management tools for Apollo.io MCP server.
"""
from typing import Optional, List


def register_tools(mcp, apollo_client):
    """Register all account-related tools with the MCP server."""

    @mcp.tool()
    async def account_search(
        query: Optional[str] = None,
        label_ids: Optional[List[str]] = None,
        page: int = 1,
        per_page: int = 25
    ) -> Optional[dict]:
        """Search accounts saved to YOUR Apollo CRM (not global organization search).

See docs/tools/accounts.md for detailed documentation and examples.

Args:
            query: Search query - matches name, domain, etc.
            label_ids: Filter by list IDs (lists are called 'labels' in Apollo API)
            page: Page number (default: 1)
            per_page: Results per page (default: 25, max: 100)

Returns:
            Dict with 'accounts' list and 'pagination' info, or None on error
    
        Reference:
            https://docs.apollo.io/reference/search-for-accounts"""
        result = await apollo_client.account_search(
            query=query,
            label_ids=label_ids,
            page=page,
            per_page=per_page
        )
        return result.model_dump() if result else None
    
    @mcp.tool()
    async def account_create(
        name: str,
        domain: Optional[str] = None,
        owner_id: Optional[str] = None,
        account_stage_id: Optional[str] = None,
        phone: Optional[str] = None,
        raw_address: Optional[str] = None,
        label_names: Optional[List[str]] = None
    ) -> Optional[dict]:
        """Create a new account in your Apollo CRM and optionally add to lists.

See docs/tools/accounts.md for detailed documentation and examples.

Args:
            name: Account name (required, e.g., "Example Corp")
            domain: Domain name without www (e.g., "example.com")
            owner_id: Apollo user ID for account owner
            account_stage_id: Apollo ID for account stage
            phone: Primary phone number
            raw_address: Corporate location (e.g., "Dallas, United States")
            label_names: List names to add account to (e.g., ["Target Accounts", "Q1 2024"])
                        Lists are called 'labels' in Apollo API but appear as 'Lists' in UI.

Returns:
            Dict with created 'account' including account_id, or None on error
    
        Reference:
            https://docs.apollo.io/reference/create-an-account"""
        result = await apollo_client.account_create(
            name=name,
            domain=domain,
            owner_id=owner_id,
            account_stage_id=account_stage_id,
            phone=phone,
            raw_address=raw_address,
            label_names=label_names
        )
        return result.model_dump() if result else None
    
    @mcp.tool()
    async def account_update(
        account_id: str,
        name: Optional[str] = None,
        domain: Optional[str] = None,
        owner_id: Optional[str] = None,
        account_stage_id: Optional[str] = None,
        phone: Optional[str] = None,
        raw_address: Optional[str] = None,
        label_names: Optional[List[str]] = None
    ) -> Optional[dict]:
        """Update an existing account in your Apollo CRM.

See docs/tools/accounts.md for detailed documentation and examples.

Args:
            account_id: Account ID from Apollo (get from account_search or account_create)
            name: Update account name
            domain: Update domain
            owner_id: Update account owner
            account_stage_id: Update account stage
            phone: Update phone number
            raw_address: Update address
            label_names: Update list membership - REPLACES existing lists entirely
                        (e.g., ["Target Accounts", "Q2 2024"])
                        Lists are called 'labels' in Apollo API but appear as 'Lists' in UI.

Returns:
            Dict with updated 'account', or None on error
    
        Reference:
            https://docs.apollo.io/reference/update-an-account"""
        # Build fields dict with only non-None values
        fields = {}
        if name is not None:
            fields["name"] = name
        if domain is not None:
            fields["domain"] = domain
        if owner_id is not None:
            fields["owner_id"] = owner_id
        if account_stage_id is not None:
            fields["account_stage_id"] = account_stage_id
        if phone is not None:
            fields["phone"] = phone
        if raw_address is not None:
            fields["raw_address"] = raw_address
        if label_names is not None:
            fields["label_names"] = label_names
    
        result = await apollo_client.account_update(account_id=account_id, **fields)
        return result.model_dump() if result else None
    
    @mcp.tool()
    async def account_bulk_create(accounts: List[dict]) -> Optional[dict]:
        """Bulk create up to 100 accounts in your Apollo CRM.

See docs/tools/accounts.md for detailed documentation and examples.

Args:
            accounts: List of account dictionaries (max 100), each containing:
                     - name (required)
                     - domain (optional but recommended for deduplication)
                     - owner_id, account_stage_id, phone, raw_address, label_names (optional)
    
                     Example:
                     [
                       {
                         "name": "Example Corp",
                         "domain": "example.com",
                         "phone": "555-1234",
                         "raw_address": "San Francisco, CA",
                         "label_names": ["Target Accounts"]
                       },
                       ...
                     ]

Returns:
            Dict with:
            - 'created_accounts': Array of newly created accounts
            - 'existing_accounts': Array of accounts that already existed
            Or None on error..."""
        result = await apollo_client.account_bulk_create(accounts=accounts)
        return result.model_dump() if result else None
    
    @mcp.tool()
    async def account_bulk_update(accounts: List[dict]) -> Optional[dict]:
        """Bulk update up to 100 accounts in your Apollo CRM.

See docs/tools/accounts.md for detailed documentation and examples.

Args:
            accounts: List of account dictionaries (max 100), each containing:
                     - id (required) - Apollo account ID
                     - Any fields to update (name, domain, owner_id, etc.)
    
                     Example:
                     [
                       {
                         "id": "account_id_1",
                         "phone": "+1-555-5678",
                         "label_names": ["Target Accounts", "Q1 2024"]
                       },
                       {
                         "id": "account_id_2",
                         "domain": "newdomain.com"
                       },
                       ...
                     ]

Returns:
            Dict with 'accounts' array of updated accounts, or None on error
    
        Reference:
            https://docs.apollo.io/reference/bulk-update-accounts"""
        result = await apollo_client.account_bulk_update(accounts=accounts)
        return result.model_dump() if result else None
    
    @mcp.tool()
    async def account_add_to_list(
        account_ids: List[str],
        label_name: str
    ) -> Optional[dict]:
        """Add multiple accounts to a list without losing their existing labels (up to 10 accounts).

See docs/tools/accounts.md for detailed documentation and examples.

Args:
            account_ids: List of Apollo account IDs (up to 10)
                        Get these from account_search or organization_search results
                        Example: ["account_123", "account_456"]
            label_name: Name of list to add accounts to
                       List will be created automatically if it doesn't exist
                       Example: "Target Accounts Q1 2024"

Returns:
            Dict with:
            - updated_accounts: Array of successfully updated account objects
            - found_ids: Array of account IDs that were found and updated
            - no..."""
        result = await apollo_client.account_add_to_list(
            account_ids=account_ids,
            label_name=label_name
        )
        return result
    
    @mcp.tool()
    async def account_remove_from_list(
        account_ids: List[str],
        label_name: str
    ) -> Optional[dict]:
        """Remove multiple accounts from a list without affecting their other labels (up to 10 accounts).

See docs/tools/accounts.md for detailed documentation and examples.

Args:
            account_ids: List of Apollo account IDs (up to 10)
                        Get these from account_search results
                        Example: ["account_123", "account_456"]
            label_name: Name of list to remove accounts from
                       Example: "Disqualified Leads"

Returns:
            Dict with:
            - updated_accounts: Array of successfully updated account objects
            - found_ids: Array of account IDs that were found and updated
            - no..."""
        result = await apollo_client.account_remove_from_list(
            account_ids=account_ids,
            label_name=label_name
        )
        return result
