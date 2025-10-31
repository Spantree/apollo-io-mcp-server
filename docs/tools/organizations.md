# Organization Search & Enrichment Tools

Organization tools help you find and enrich data for companies in Apollo's global database of 73M+ organizations.

---

## organization_enrichment

Enrich data for a single company by domain. Does not consume credits.

### Parameters

- domain (REQUIRED): Company domain without www or @ symbol
  Examples: "apollo.io", "microsoft.com"

### Returns

- Company basics (name, domain, industry, description)
- Contact information (phone, HQ address)
- Company metrics (employee count, revenue, founded year)
- Social profiles (LinkedIn, Twitter, Facebook, AngelList)
- Funding information (total funding, investors)
- Technologies used (tech stack)
- Account status (if saved to CRM, shows label_names)

### Use Cases

- Research companies before outreach
- Enrich existing company data
- Verify company information
- Find company contact details

---

## organization_search

Search Apollo's 73M+ company database. Does not consume credits.

### Search Filters

COMPANY SIZE & REVENUE:
- organization_num_employees_ranges: ["1,10", "250,500", "10000,20000"]
- revenue_range_min/max: Annual revenue in dollars

LOCATION:
- organization_locations: HQ locations ["texas", "tokyo", "spain"]
- organization_not_locations: Exclude locations

TECHNOLOGY & KEYWORDS:
- currently_using_any_of_technology_uids: ["salesforce", "google_analytics"]
  See: https://api.apollo.io/v1/auth/supported_technologies_csv
- q_organization_keyword_tags: Industry keywords ["mining", "sales strategy"]
- q_organization_name: Company name search

### Returns

- organization_id (use with organization_enrichment, people_search)
- Company basics, contact info
- Company metrics
- Social profiles
- Account status (shows label_names if in CRM)

### Use Cases

- Build target account lists
- Find companies by industry/size
- Identify companies using specific tech
- Research markets

---

## organization_job_postings

Get active job postings for a specific company. Does not consume credits.

### Parameters

- organization_id (REQUIRED): From organization_search

### Returns

Array of job postings with:
- id, title, url
- location (city, state, country)
- posted_at, last_seen_at

### Use Cases

- Identify hiring signals (growth, new departments)
- Find decision makers (hiring managers)
- Prioritize outreach based on company needs
- Time outreach when actively hiring

### Workflow

1. organization_search to find companies
2. Get organization_id from results
3. Call this endpoint for job postings
4. Use people_search with matching titles to find hiring managers

Example: If "VP of Marketing" posting found, search for "CMO" or "Marketing Director" as potential decision makers.

See https://docs.apollo.io/reference/organization-jobs-postings
