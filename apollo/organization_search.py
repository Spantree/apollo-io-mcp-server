from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class OrganizationSearchQuery(BaseModel):
    organization_num_employees_ranges: Optional[List[str]] = Field(default=None, description="Employee count ranges (e.g., ['1,10', '11,50'])")
    organization_locations: Optional[List[str]] = Field(default=None)
    organization_not_locations: Optional[List[str]] = Field(default=None)
    revenue_range_min: Optional[int] = Field(default=None)
    revenue_range_max: Optional[int] = Field(default=None)
    currently_using_any_of_technology_uids: Optional[List[str]] = Field(default=None, description="Filter by technology UIDs (see Apollo tech list)")
    q_organization_keyword_tags: Optional[List[str]] = Field(default=None, description="Filter by industry/keyword tags")
    q_organization_name: Optional[str] = Field(default=None, description="Search by organization name")
    organization_ids: Optional[List[str]] = Field(default=None)
    page: Optional[int] = Field(default=None)
    per_page: Optional[int] = Field(default=None)

class Breadcrumb(BaseModel):
    label: str = Field()
    signal_field_name: str = Field()
    value: str = Field()
    display_name: str = Field()

class PrimaryPhone(BaseModel):
    number: Optional[str] = Field(default=None)
    source: Optional[str] = Field(default=None)
    sanitized_number: Optional[str] = Field(default=None)

class Organization(BaseModel):
    id: str = Field()
    name: Optional[str] = Field(default=None)
    website_url: Optional[str] = Field(default=None)
    blog_url: Optional[str] = Field(default=None)
    angellist_url: Optional[str] = Field(default=None)
    linkedin_url: Optional[str] = Field(default=None)
    twitter_url: Optional[str] = Field(default=None)
    facebook_url: Optional[str] = Field(default=None)
    primary_phone: Optional[PrimaryPhone] = Field(default=None)
    languages: Optional[List[str]] = Field(default=None)
    alexa_ranking: Optional[int] = Field(default=0)
    phone: Optional[str] = Field(default=None)
    linkedin_uid: Optional[str] = Field(default=None)
    founded_year: Optional[int] = Field(default=0)
    publicly_traded_symbol: Optional[str] = Field(default=None)
    publicly_traded_exchange: Optional[str] = Field(default=None)
    logo_url: Optional[str] = Field(default=None)
    crunchbase_url: Optional[str] = Field(default=None)
    primary_domain: Optional[str] = Field(default=None)
    sanitized_phone: Optional[str] = Field(default=None)
    owned_by_organization_id: Optional[str] = Field(default=None)
    intent_strength: Optional[str] = Field(default=None)
    show_intent: Optional[bool] = Field(default=None)
    has_intent_signal_account: Optional[bool] = Field(default=None)
    intent_signal_account: Optional[str] = Field(default=None)

class Pagination(BaseModel):
    page: int = Field(default=0)
    per_page: int = Field(default=0)
    total_entries: int = Field(default=0)
    total_pages: int = Field(default=0)

class OrganizationSearchResponse(BaseModel):
    breadcrumbs: Optional[List[Breadcrumb]] = Field(default=None)
    partial_results_only: Optional[bool] = Field(default=True)
    has_join: Optional[bool] = Field(default=True)
    disable_eu_prospecting: Optional[bool] = Field(default=True)
    partial_results_limit: Optional[int] = Field(default=0)
    pagination: Optional[Pagination] = Field(default=None)
    accounts: Optional[List[Any]] = Field(default=None)
    organizations: Optional[List[Organization]] = Field(default=None)
    model_ids: Optional[List[str]] = Field(default=None)
    num_fetch_result: Optional[str] = Field(default=None)
    derived_params: Optional[Any] = Field(default=None)
