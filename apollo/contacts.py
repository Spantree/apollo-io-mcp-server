from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# Note: Contact model is defined in apollo/people.py and can be imported from apollo package


class PhoneNumber(BaseModel):
    """Phone number with type information for contact operations."""

    raw_number: str = Field(
        description="Phone number in international format (e.g., '+1-555-0123')"
    )
    type: Optional[str] = Field(
        default="mobile"
    )


class ContactSearchQuery(BaseModel):
    """Query parameters for searching saved contacts in your Apollo CRM."""

    q: Optional[str] = Field(
        default=None,
        description="Search query - matches name, email, company, title, etc.",
    )
    contact_label_ids: Optional[List[str]] = Field(
        default=None,
        description="Filter by list IDs (label IDs)"
    )
    page: int = Field(default=1)
    per_page: int = Field(
        default=25
    )


class ContactCreateRequest(BaseModel):
    """Request data for creating a new contact in your Apollo CRM."""

    first_name: str = Field()
    last_name: str = Field()
    email: Optional[str] = Field(
        default=None
    )
    organization_name: Optional[str] = Field(
        default=None
    )
    title: Optional[str] = Field(default=None)
    label_names: Optional[List[str]] = Field(
        default=None,
        description="List names to add contact to (lists are called 'labels' in Apollo API)",
    )
    phone_numbers: Optional[List[PhoneNumber]] = Field(
        default=None
    )
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    country: Optional[str] = Field(
        default=None
    )
    linkedin_url: Optional[str] = Field(
        default=None
    )

    class Config:
        # Exclude None values when serializing to avoid sending null fields
        exclude_none = True


class ContactUpdateRequest(BaseModel):
    """Request data for updating an existing contact in your Apollo CRM."""

    contact_id: str = Field()
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    organization_name: Optional[str] = Field(
        default=None
    )
    title: Optional[str] = Field(default=None)
    label_names: Optional[List[str]] = Field(
        default=None
    )
    phone_numbers: Optional[List[PhoneNumber]] = Field(
        default=None
    )
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    linkedin_url: Optional[str] = Field(
        default=None
    )

    class Config:
        # Exclude None values when serializing to only update provided fields
        exclude_none = True


class Pagination(BaseModel):
    """Pagination information for search results."""

    page: int = Field()
    per_page: int = Field()
    total_entries: int = Field()
    total_pages: int = Field()


class ContactSearchResponse(BaseModel):
    """Response from contacts search endpoint."""

    contacts: List[Any] = Field()
    pagination: Pagination = Field()


class ContactCreateResponse(BaseModel):
    """Response from contact create endpoint."""

    contact: Any = Field()


class ContactUpdateResponse(BaseModel):
    """Response from contact update endpoint."""

    contact: Any = Field()


class ContactBulkItem(BaseModel):
    """Contact data for bulk create operation."""

    first_name: str = Field()
    last_name: str = Field()
    email: Optional[str] = Field(default=None)
    organization_name: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    label_names: Optional[List[str]] = Field(
        default=None
    )
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    linkedin_url: Optional[str] = Field(default=None)


class ContactBulkCreateRequest(BaseModel):
    """Request for bulk create contacts endpoint (up to 100 contacts)."""

    contacts: List[ContactBulkItem] = Field(
        description="Array of contact objects to create (max 100)", max_length=100
    )


class ContactBulkCreateResponse(BaseModel):
    """Response from bulk create contacts endpoint."""

    created_contacts: List[Any] = Field(
        description="Array of newly created contacts"
    )
    existing_contacts: List[Any] = Field(
        description="Array of existing contacts that matched (not updated)"
    )


class ContactBulkUpdateItem(BaseModel):
    """Contact data for bulk update operation."""

    id: str = Field()
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    organization_name: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    label_names: Optional[List[str]] = Field(
        default=None
    )
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    linkedin_url: Optional[str] = Field(default=None)

    class Config:
        exclude_none = True


class ContactBulkUpdateRequest(BaseModel):
    """Request for bulk update contacts endpoint (up to 100 contacts)."""

    contacts: List[ContactBulkUpdateItem] = Field(
        description="Array of contact objects to update (max 100)", max_length=100
    )


class ContactBulkUpdateResponse(BaseModel):
    """Response from bulk update contacts endpoint."""

    contacts: List[Any] = Field()
