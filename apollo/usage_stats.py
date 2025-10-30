from typing import Dict, Any
from pydantic import BaseModel, Field


class RateLimitPeriod(BaseModel):
    """Rate limit information for a specific time period."""

    limit: int = Field(description="Maximum requests allowed in this period")
    consumed: int = Field(description="Requests consumed in this period")
    left_over: int = Field(description="Requests remaining in this period")


class EndpointRateLimit(BaseModel):
    """Rate limit information for an API endpoint."""

    day: RateLimitPeriod = Field(description="Daily rate limit")
    hour: RateLimitPeriod = Field(description="Hourly rate limit")
    minute: RateLimitPeriod = Field(description="Per-minute rate limit")


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
