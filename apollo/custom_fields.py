from typing import Optional, List, Any
from pydantic import BaseModel, Field, ConfigDict


class CustomField(BaseModel):
    """Custom field definition from Apollo CRM."""

    model_config = ConfigDict(extra='allow')

    id: str = Field()
    name: str = Field()
    # Apollo API uses 'type' field
    type: Optional[str] = Field(
        default=None,
        description="Type: string, textarea, number, date, datetime, boolean, picklist"
    )
    modality: Optional[str] = Field(
        default=None,
        description="Entity type: contact, account, or opportunity"
    )
    # Picklist options
    picklist_options: Optional[List[Any]] = Field(
        default=None,
        description="Available options for picklist fields"
    )
    picklist_values: Optional[List[Any]] = Field(
        default=None,
        description="Picklist values with IDs"
    )
    # Other optional fields
    text_field_max_length: Optional[int] = Field(default=None)
    is_readonly_mapped_crm_field: Optional[bool] = Field(default=None)
    mirrored: Optional[bool] = Field(default=None)
    is_local: Optional[bool] = Field(default=None)
    mapped_crm_field: Optional[str] = Field(default=None)
    system_name: Optional[str] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)


class CustomFieldListResponse(BaseModel):
    """Response from list custom fields endpoint."""

    model_config = ConfigDict(extra='allow')

    typed_custom_fields: List[CustomField] = Field(
        description="Array of custom field definitions"
    )


class CustomFieldCreateRequest(BaseModel):
    """Request data for creating a new custom field."""

    label: str = Field(
        description="Display name for the custom field"
    )
    type: str = Field(
        description="Type: string, textarea, number, date, datetime, boolean, picklist"
    )
    modality: str = Field(
        description="Entity type: contact, account, or opportunity"
    )
    meta: Optional[dict] = Field(
        default=None,
        description="Metadata object. For picklist type, use {'picklist_options': ['opt1', 'opt2']}"
    )


class CustomFieldCreateResponse(BaseModel):
    """Response from create custom field endpoint."""

    typed_custom_field: CustomField = Field(
        description="Created custom field definition"
    )
