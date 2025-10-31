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

    id: str = Field()
    name: str = Field()
    modality: str = Field(description='Label modality: "contacts", "accounts", or "emailer_campaigns"')
    cached_count: Optional[int] = Field(default=None)
    team_id: Optional[str] = Field(default=None)
    user_id: Optional[str] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)


class LabelListResponse(BaseModel):
    """Response from labels list endpoint."""

    labels: List[Label] = Field()
