from typing import Optional, List
from pydantic import BaseModel, Field

class OrganizationJobPostingsQuery(BaseModel):
    organization_id: str = Field()

class OrganizationJobPosting(BaseModel):
    id: str = Field()
    title: str = Field()
    url: str = Field()
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    country: str = Field()
    last_seen_at: str = Field()
    posted_at: str = Field()

class OrganizationJobPostingsResponse(BaseModel):
    organization_job_postings: List[OrganizationJobPosting] = Field()
