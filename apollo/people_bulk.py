from typing import Optional, List
from pydantic import BaseModel, Field
from apollo.people import Person

class BulkPeopleEnrichmentQuery(BaseModel):
    reveal_personal_emails: Optional[bool] = Field(default=False, description="Set to true to enrich all matched people with personal emails. May consume credits.")
    reveal_phone_number: Optional[bool] = Field(default=False, description="Set to true to enrich with phone numbers. Requires webhook_url. May consume credits.")
    webhook_url: Optional[str] = Field(default=None, description="Required if reveal_phone_number=true. URL where Apollo sends phone number data asynchronously.")
    details: List[dict] = Field(description="Array of person identification objects (up to 10 people). Each object can contain: id, email, name (or first_name + last_name), domain, organization_name, linkedin_url, or hashed_email.")

class BulkPeopleEnrichmentResponse(BaseModel):
    status: Optional[str] = Field(default=None, description="Status of the bulk enrichment operation")
    error_code: Optional[str] = Field(default=None, description="Error code if operation failed")
    error_message: Optional[str] = Field(default=None, description="Error message if operation failed")
    total_requested_enrichments: Optional[int] = Field(default=0, description="Total number of enrichments requested")
    unique_enriched_records: Optional[int] = Field(default=0, description="Number of unique records successfully enriched")
    missing_records: Optional[int] = Field(default=0, description="Number of records that could not be found")
    credits_consumed: Optional[int] = Field(default=0, description="Number of credits consumed by this operation")
    matches: Optional[List[Person]] = Field(default=None, description="Array of enriched person records")
