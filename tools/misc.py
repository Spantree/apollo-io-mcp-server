"""
Miscellaneous tools (usage stats and labels) for Apollo.io MCP server.
"""
from typing import Optional


def register_tools(mcp, apollo_client):
    """Register miscellaneous tools with the MCP server."""

    @mcp.tool()
    async def usage_stats() -> Optional[dict]:
        """
        Get API usage statistics and rate limits for your Apollo account.
    
        Returns rate limits per endpoint showing:
        - Minute limits (limit, consumed, left_over)
        - Hour limits (limit, consumed, left_over)
        - Day limits (limit, consumed, left_over)
    
        This is useful for monitoring your API usage and avoiding rate limit errors.
    
        IMPORTANT: This endpoint requires a master API key. Regular API keys will
        receive a 403 Forbidden error.
    
        Returns:
            Dict with rate limit stats keyed by endpoint identifier, or None on error
    
        Reference:
            https://docs.apollo.io/reference/get-usage-stats
        """
        result = await apollo_client.usage_stats()
        return result.model_dump() if result else None
    
    @mcp.tool()
    async def labels_list(modality: Optional[str] = None) -> Optional[dict]:
        """
        List all labels/lists in your Apollo account.
    
        Labels (called "Lists" in Apollo UI) are used to organize contacts,
        accounts, and emailer campaigns. Each label has a modality field
        indicating what type of entity it contains.
    
        This endpoint requires a master API key. Regular API keys will fail.
    
        Args:
            modality: Filter by modality type. Options:
                     - "contacts": Lists of contacts/people
                     - "accounts": Lists of companies/organizations
                     - "emailer_campaigns": Lists for email campaigns
                     If None, returns all labels across all modalities.
    
        Returns:
            Dict with 'labels' list containing label objects (id, name, modality,
            cached_count, etc.), or None on error
    
        Reference:
            https://docs.apollo.io/reference/get-a-list-of-all-lists
        """
        result = await apollo_client.labels_list(modality=modality)
        return result.model_dump() if result else None
