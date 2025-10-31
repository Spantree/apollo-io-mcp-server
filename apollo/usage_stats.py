from typing import Dict, Any
from pydantic import BaseModel, Field


class RateLimitPeriod(BaseModel):
    """Rate limit information for a specific time period."""

    limit: int = Field()
    consumed: int = Field()
    left_over: int = Field()


class EndpointRateLimit(BaseModel):
    """Rate limit information for an API endpoint."""

    day: RateLimitPeriod = Field()
    hour: RateLimitPeriod = Field()
    minute: RateLimitPeriod = Field()


class UsageStatsResponse(BaseModel):
    """
    Response from usage stats endpoint.

    Returns rate limits per endpoint with minute, hour, and day limits.
    Requires master API key.
    """

    # Dynamic keys are endpoint identifiers like:
    # ["api/v1/contacts", "search"]
    # ["api/v1/contacts", "create"]
    # etc.
    # Using Dict[str, Any] to handle the dynamic response structure
    stats: Dict[str, Any] = Field(
        default_factory=dict,
        description="Rate limit stats keyed by endpoint identifier"
    )

    class Config:
        # Allow extra fields for dynamic endpoint keys
        extra = "allow"
