from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AccountCreateRequest(BaseModel):
    """Request data for creating a new account in your Apollo CRM."""

    name: str = Field(description="Account name (required, human-readable)")
    domain: Optional[str] = Field(
        default=None,
        description="Domain name without www (e.g., 'apollo.io')"
    )
    owner_id: Optional[str] = Field(
        default=None,
        description="Apollo user ID for account owner"
    )
    account_stage_id: Optional[str] = Field(
        default=None,
        description="Apollo ID for account stage"
    )
    phone: Optional[str] = Field(
        default=None,
        description="Primary phone number (e.g., '555-303-1234')"
    )
    raw_address: Optional[str] = Field(
        default=None,
        description="Corporate location (e.g., 'Dallas, United States')"
    )
    typed_custom_fields: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Custom fields data (use Get Custom Fields endpoint to find field IDs)"
    )
    label_names: Optional[List[str]] = Field(
        default=None,
        description="List names to add account to (lists are called 'labels' in Apollo API)"
    )

    class Config:
        exclude_none = True


class AccountUpdateRequest(BaseModel):
    """Request data for updating an existing account in your Apollo CRM."""

    account_id: str = Field(description="Apollo account ID (required for API call)")
    name: Optional[str] = Field(default=None, description="Update account name")
    domain: Optional[str] = Field(default=None, description="Update domain")
    owner_id: Optional[str] = Field(default=None, description="Update account owner")
    account_stage_id: Optional[str] = Field(
        default=None,
        description="Update account stage"
    )
    phone: Optional[str] = Field(default=None, description="Update phone number")
    raw_address: Optional[str] = Field(default=None, description="Update address")
    typed_custom_fields: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Update custom fields"
    )
    label_names: Optional[List[str]] = Field(
        default=None,
        description="Update list membership (REPLACES existing lists)"
    )

    class Config:
        exclude_none = True


class AccountSearchQuery(BaseModel):
    """Query parameters for searching saved accounts in your Apollo CRM."""

    q: Optional[str] = Field(
        default=None,
        description="Search query - matches name, domain, etc."
    )
    account_label_ids: Optional[List[str]] = Field(
        default=None,
        description="Filter by list IDs (label IDs)"
    )
    page: int = Field(default=1, description="Page number for pagination (default: 1)")
    per_page: int = Field(
        default=25,
        description="Results per page (default: 25, max: 100)"
    )


class Pagination(BaseModel):
    """Pagination information for search results."""

    page: int = Field(description="Current page number")
    per_page: int = Field(description="Results per page")
    total_entries: int = Field(description="Total number of matching accounts")
    total_pages: int = Field(description="Total number of pages")


class AccountSearchResponse(BaseModel):
    """Response from accounts search endpoint."""

    accounts: List[Any] = Field(description="List of matching accounts")
    pagination: Pagination = Field(description="Pagination information")


class AccountCreateResponse(BaseModel):
    """Response from account create endpoint."""

    account: Any = Field(description="Created account with account_id")


class AccountUpdateResponse(BaseModel):
    """Response from account update endpoint."""

    account: Any = Field(description="Updated account")


class AccountBulkItem(BaseModel):
    """Account data for bulk create operation."""

    name: str = Field(description="Account name (required)")
    domain: Optional[str] = Field(default=None, description="Domain name")
    owner_id: Optional[str] = Field(default=None, description="Account owner ID")
    account_stage_id: Optional[str] = Field(default=None, description="Account stage ID")
    phone: Optional[str] = Field(default=None, description="Phone number")
    raw_address: Optional[str] = Field(default=None, description="Address")
    typed_custom_fields: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Custom fields"
    )
    label_names: Optional[List[str]] = Field(
        default=None,
        description="List names to add account to"
    )


class AccountBulkCreateRequest(BaseModel):
    """Request for bulk create accounts endpoint (up to 100 accounts)."""

    accounts: List[AccountBulkItem] = Field(
        description="Array of account objects to create (max 100)",
        max_length=100
    )


class AccountBulkCreateResponse(BaseModel):
    """Response from bulk create accounts endpoint."""

    created_accounts: List[Any] = Field(
        description="Array of newly created accounts"
    )
    existing_accounts: List[Any] = Field(
        description="Array of existing accounts that matched (not updated)"
    )


class AccountBulkUpdateItem(BaseModel):
    """Account data for bulk update operation."""

    id: str = Field(description="Account ID (required for update)")
    name: Optional[str] = Field(default=None, description="Update name")
    domain: Optional[str] = Field(default=None, description="Update domain")
    owner_id: Optional[str] = Field(default=None, description="Update owner")
    account_stage_id: Optional[str] = Field(default=None, description="Update stage")
    phone: Optional[str] = Field(default=None, description="Update phone")
    raw_address: Optional[str] = Field(default=None, description="Update address")
    typed_custom_fields: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Update custom fields"
    )
    label_names: Optional[List[str]] = Field(
        default=None,
        description="Update list membership (replaces existing)"
    )

    class Config:
        exclude_none = True


class AccountBulkUpdateRequest(BaseModel):
    """Request for bulk update accounts endpoint (up to 100 accounts)."""

    accounts: List[AccountBulkUpdateItem] = Field(
        description="Array of account objects to update (max 100)",
        max_length=100
    )


class AccountBulkUpdateResponse(BaseModel):
    """Response from bulk update accounts endpoint."""

    accounts: List[Any] = Field(description="Array of updated accounts")
