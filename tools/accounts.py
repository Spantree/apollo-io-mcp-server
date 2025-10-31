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
        """
        Search accounts saved to YOUR CRM (not global search). Returns account_id for updates.
        Use organization_search for prospecting.

        Args:
            query: Matches name, domain, etc.
            label_ids: Filter by list IDs
            page: Page number (default: 1)
            per_page: Results per page (default: 25, max: 100)

        Reference:
            https://docs.apollo.io/reference/search-for-accounts
        """
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
        """
        Create new account in Apollo CRM. Master API key required.

        Provide name (required), domain recommended for deduplication.
        Lists auto-created if they don't exist.

        Args:
            name: Account name (required)
            domain: Domain without www (e.g., "example.com")
            owner_id: Apollo user ID for account owner
            account_stage_id: Apollo ID for account stage
            phone: Primary phone number
            raw_address: Corporate location
            label_names: List names to add account to

        Returns:
            Dict with created account including account_id, or None on error

        Reference:
            https://docs.apollo.io/reference/create-an-account
        """
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
        """
        Update existing account in Apollo CRM. Master API key required.

        Only provided fields are updated. IMPORTANT: label_names REPLACES all lists.
        Use account_add_to_list/account_remove_from_list to preserve existing labels.

        Args:
            account_id: Account ID (from account_search or account_create)
            name: Update account name
            domain: Update domain
            owner_id: Update account owner
            account_stage_id: Update account stage
            phone: Update phone number
            raw_address: Update address
            label_names: REPLACES existing lists entirely

        Returns:
            Dict with updated account, or None on error

        Reference:
            https://docs.apollo.io/reference/update-an-account
        """
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
        """
        Bulk create up to 100 accounts. Master API key required.

        More efficient than one-by-one creation. Existing accounts (matched by domain)
        returned in existing_accounts but NOT updated.

        Args:
            accounts: List of account dicts (max 100), each with:
                     - name (required)
                     - domain (optional, recommended for deduplication)
                     - owner_id, account_stage_id, phone, raw_address, label_names (optional)

        Returns:
            {created_accounts, existing_accounts} or None on error

        Reference:
            https://docs.apollo.io/reference/bulk-create-accounts
        """
        result = await apollo_client.account_bulk_create(accounts=accounts)
        return result.model_dump() if result else None
    
    @mcp.tool()
    async def account_bulk_update(accounts: List[dict]) -> Optional[dict]:
        """
        Bulk update up to 100 accounts. Master API key required.

        More efficient than one-by-one updates. Only provided fields updated.
        IMPORTANT: label_names REPLACES all lists for each account.

        Args:
            accounts: List of account dicts (max 100), each with:
                     - id (required) - Apollo account ID
                     - Any fields to update (name, domain, owner_id, etc.)

        Returns:
            {accounts: [updated accounts]} or None on error

        Reference:
            https://docs.apollo.io/reference/bulk-update-accounts
        """
        result = await apollo_client.account_bulk_update(accounts=accounts)
        return result.model_dump() if result else None
    
    @mcp.tool()
    async def account_add_to_list(
        account_ids: List[str],
        label_name: str
    ) -> Optional[dict]:
        """
        Add accounts to a list without losing existing labels (max 10). Master API key required.

        Helper tool that safely merges new label with current labels. Solves label replacement
        problem - account_update/account_bulk_update REPLACE all labels, this tool preserves them.

        See docs/tools/accounts.md for workflow details and examples.

        Args:
            account_ids: Account IDs to add (max 10)
            label_name: List name (auto-created if doesn't exist)

        Returns:
            {updated_accounts, found_ids, not_found_ids, total_requested}
        """
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
        """
        Remove accounts from a list without affecting other labels (max 10). Master API key required.

        Helper tool that safely removes specified label while preserving all other labels.
        Solves label replacement problem by fetching current labels, removing target label,
        and updating with remaining labels.

        See docs/tools/accounts.md for workflow details and examples.

        Args:
            account_ids: Account IDs to remove (max 10)
            label_name: List name to remove accounts from

        Returns:
            {updated_accounts, found_ids, not_found_ids, total_requested}
        """
        result = await apollo_client.account_remove_from_list(
            account_ids=account_ids,
            label_name=label_name
        )
        return result
