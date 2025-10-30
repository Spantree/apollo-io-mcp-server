from typing import Optional, List, Any
from pydantic import BaseModel, Field


class LabelListQuery(BaseModel):
    """
    Query parameters for listing labels.

    Note: The Apollo API endpoint /api/v1/labels does not accept any parameters.
    All labels are returned and must be filtered client-side.
    """

    modality: Optional[str] = Field(
        default=None,
        description='Filter labels by modality. Options: "contacts", "accounts", "emailer_campaigns". If not provided, returns all labels.'
    )


class Label(BaseModel):
    """A label/list in Apollo."""

    id: str = Field(description="Label ID")
    name: str = Field(description="Label name")
    modality: str = Field(description='Label modality: "contacts", "accounts", or "emailer_campaigns"')
    cached_count: Optional[int] = Field(default=None, description="Number of items with this label")
    team_id: Optional[str] = Field(default=None, description="Team ID")
    user_id: Optional[str] = Field(default=None, description="User ID who created the label")
    created_at: Optional[str] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[str] = Field(default=None, description="Last update timestamp")


class LabelListResponse(BaseModel):
    """Response from labels list endpoint."""

    labels: List[Label] = Field(description="List of labels")
