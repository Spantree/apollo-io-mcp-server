from typing import Optional, List
from pydantic import BaseModel, Field
from apollo.people import Person

class BulkPeopleEnrichmentQuery(BaseModel):
    reveal_personal_emails: Optional[bool] = Field(default=False)
    reveal_phone_number: Optional[bool] = Field(default=False)
    webhook_url: Optional[str] = Field(default=None)
    details: List[dict] = Field()

class BulkPeopleEnrichmentResponse(BaseModel):
    status: Optional[str] = Field(default=None)
    error_code: Optional[str] = Field(default=None)
    error_message: Optional[str] = Field(default=None)
    total_requested_enrichments: Optional[int] = Field(default=0)
    unique_enriched_records: Optional[int] = Field(default=0)
    missing_records: Optional[int] = Field(default=0)
    credits_consumed: Optional[int] = Field(default=0)
    matches: Optional[List[Person]] = Field(default=None)
