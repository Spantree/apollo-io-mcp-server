from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# Note: Contact model is defined in apollo/people.py and can be imported from apollo package


class PhoneNumber(BaseModel):
    """Phone number with type information for contact operations."""
    raw_number: str = Field(description="Phone number in international format (e.g., '+1-555-0123')")
    type: Optional[str] = Field(default="mobile", description="Phone type: 'mobile', 'work', or 'home'")


class ContactSearchQuery(BaseModel):
    """Query parameters for searching saved contacts in your Apollo CRM."""
    q: Optional[str] = Field(default=None, description="Search query - matches name, email, company, title, etc.")
    contact_label_ids: Optional[List[str]] = Field(default=None, description="Filter by list IDs (label IDs)")
    page: int = Field(default=1, description="Page number for pagination (default: 1)")
    per_page: int = Field(default=25, description="Results per page (default: 25, max: 100)")


class ContactCreateRequest(BaseModel):
    """Request data for creating a new contact in your Apollo CRM."""
    first_name: str = Field(description="Contact's first name (required)")
    last_name: str = Field(description="Contact's last name (required)")
    email: Optional[str] = Field(default=None, description="Email address (recommended for future updates)")
    organization_name: Optional[str] = Field(default=None, description="Company/organization name")
    title: Optional[str] = Field(default=None, description="Job title")
    label_names: Optional[List[str]] = Field(default=None, description="List names to add contact to (lists are called 'labels' in Apollo API)")
    phone_numbers: Optional[List[PhoneNumber]] = Field(default=None, description="Phone numbers with types")
    city: Optional[str] = Field(default=None, description="City")
    state: Optional[str] = Field(default=None, description="State/province")
    country: Optional[str] = Field(default=None, description="Country code (e.g., 'US')")
    linkedin_url: Optional[str] = Field(default=None, description="LinkedIn profile URL")

    class Config:
        # Exclude None values when serializing to avoid sending null fields
        exclude_none = True


class ContactUpdateRequest(BaseModel):
    """Request data for updating an existing contact in your Apollo CRM."""
    contact_id: str = Field(description="Apollo contact ID (required for API call)")
    first_name: Optional[str] = Field(default=None, description="Update first name")
    last_name: Optional[str] = Field(default=None, description="Update last name")
    email: Optional[str] = Field(default=None, description="Update email address")
    organization_name: Optional[str] = Field(default=None, description="Update company/organization name")
    title: Optional[str] = Field(default=None, description="Update job title")
    label_names: Optional[List[str]] = Field(default=None, description="Update list membership (REPLACES existing lists)")
    phone_numbers: Optional[List[PhoneNumber]] = Field(default=None, description="Update phone numbers")
    city: Optional[str] = Field(default=None, description="Update city")
    state: Optional[str] = Field(default=None, description="Update state/province")
    country: Optional[str] = Field(default=None, description="Update country code")
    linkedin_url: Optional[str] = Field(default=None, description="Update LinkedIn profile URL")

    class Config:
        # Exclude None values when serializing to only update provided fields
        exclude_none = True


class Pagination(BaseModel):
    """Pagination information for search results."""
    page: int = Field(description="Current page number")
    per_page: int = Field(description="Results per page")
    total_entries: int = Field(description="Total number of matching contacts")
    total_pages: int = Field(description="Total number of pages")


class ContactSearchResponse(BaseModel):
    """Response from contacts search endpoint."""
    contacts: List[Any] = Field(description="List of matching contacts")
    pagination: Pagination = Field(description="Pagination information")


class ContactCreateResponse(BaseModel):
    """Response from contact create endpoint."""
    contact: Any = Field(description="Created contact with contact_id")


class ContactUpdateResponse(BaseModel):
    """Response from contact update endpoint."""
    contact: Any = Field(description="Updated contact")
