# People Search & Enrichment Tools

People tools help you find and enrich data for individuals in Apollo's global database of 275M+ contacts.

---

## people_enrichment

Enrich data for a single person by providing identifying information.

### Parameters

Provide one or more:
- id: Apollo person ID (from people_search)
- email: Email address
- name: Full name OR first_name + last_name
- linkedin_url: LinkedIn profile URL
- domain + name: Employer domain + person name
- organization_name + name: Employer + person name

### Returns

Person details including:
- Employment history (current and previous)
- Contact information (email, phone if revealed)
- Organization details
- Engagement signals (is_likely_to_engage)
- Professional details (seniority, functions)

### Credit Consumption

- reveal_personal_emails=true: May consume credits
- reveal_phone_number=true: May consume credits + requires webhook_url
- Basic enrichment: No credits

### GDPR

Personal emails NOT revealed for people in GDPR regions.

---

## people_bulk_enrichment

Enrich up to 10 people in a single request. More efficient than individual calls.

### Parameters

- details: Array of person identification objects (max 10)
- reveal_personal_emails (optional)
- reveal_phone_number (optional) - requires webhook_url

### Returns

- status, total_requested_enrichments
- unique_enriched_records, missing_records
- credits_consumed
- matches: Array of enriched Person objects

---

## people_search

Search Apollo's 275M+ person database. Does not consume credits.

### Search Filters

PERSON ATTRIBUTES:
- person_titles: Job titles (matches similar unless include_similar_titles=false)
- person_seniorities: c_suite, vp, director, manager, senior, entry, intern
- person_locations: Where people live
- contact_email_status: verified, unverified, likely to engage, unavailable

COMPANY FILTERS:
- organization_ids: From organization_search
- q_organization_domains_list: Employer domains (up to 1000)
- organization_locations: Company HQ location
- organization_num_employees_ranges: Company size

OTHER:
- q_keywords: Keyword search
- page/per_page: Pagination

### Returns

- People with person_id (use with people_enrichment)
- Employment history
- Contact information
- Professional metadata

### Use Cases

- Build targeted prospect lists
- Find decision makers at companies
- Identify people by job function
- Research contacts before outreach

See https://docs.apollo.io/reference/people-search for full details
