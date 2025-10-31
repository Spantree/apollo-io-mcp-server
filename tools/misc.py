"""
Miscellaneous tools (usage stats and labels) for Apollo.io MCP server.
"""
from typing import Optional


def register_tools(mcp, apollo_client):
    """Register miscellaneous tools with the MCP server."""

    @mcp.tool()
    async def usage_stats() -> Optional[dict]:
        """
        Get API usage and rate limits per endpoint. Master API key required.
        Shows minute/hour/day limits with consumed and left_over counts.

        Reference:
            https://docs.apollo.io/reference/get-usage-stats
        """
        result = await apollo_client.usage_stats()
        return result.model_dump() if result else None
    
    @mcp.tool()
    async def labels_list(modality: Optional[str] = None) -> Optional[dict]:
        """
        List all labels/lists in your Apollo account. Master API key required.

        Args:
            modality: Filter by "contacts", "accounts", or "emailer_campaigns" (default: all)

        Returns:
            {labels: [{id, name, modality, cached_count, ...}]}

        Reference:
            https://docs.apollo.io/reference/get-a-list-of-all-lists
        """
        result = await apollo_client.labels_list(modality=modality)
        return result.model_dump() if result else None
