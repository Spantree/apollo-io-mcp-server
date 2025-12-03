# Test Queries for Claude Code

Use these queries to validate the Apollo.io MCP server is working correctly in Claude Code.

## Setup Validation

### Query 1: List Available Tools
```
What Apollo.io tools are available?
```

**Expected:**
- Lists all 20 tools (or filtered count if using --include-tools)
- Organized by category (people, organizations, contacts, accounts, misc)

---

## People Tools Tests

### Query 2: Basic People Search
```
Search Apollo for "Software Engineers" at companies with 50-200 employees
in San Francisco. Show me the first 3 results with their names, titles,
and companies.
```

**Expected:**
- Uses `people_search` tool
- Returns 3 person records
- Shows name, title, company info
- No errors

### Query 3: People Enrichment
```
Enrich this person's data using their email: tim@example.com
What employment history and contact info can you find?
```

**Expected:**
- Uses `people_enrichment` tool
- Returns employment history
- Shows contact information
- Handles not found gracefully if email doesn't exist

### Query 4: Bulk People Enrichment
```
Bulk enrich these 3 people by email:
- john@example.com
- jane@startup.io
- bob@techcorp.com
```

**Expected:**
- Uses `people_bulk_enrichment` tool
- Returns results for all 3 (or explains which weren't found)
- More efficient than 3 separate calls

---

## Organization Tools Tests

### Query 5: Basic Organization Search
```
Find SaaS companies in Austin, Texas with:
- 100-500 employees
- Series A or Series B funding
- Using Salesforce

Show me 5 results.
```

**Expected:**
- Uses `organization_search` tool
- Returns up to 5 companies
- Filters applied correctly
- Shows company name, size, funding, tech stack

### Query 6: Organization Enrichment
```
Enrich the company data for the domain: apollo.io
What can you tell me about their funding, tech stack, and employee count?
```

**Expected:**
- Uses `organization_enrichment` tool
- Returns company details
- Shows funding info if available
- Shows technologies used

### Query 7: Job Postings
```
Get the current job postings for the company with domain: stripe.com
What roles are they hiring for?
```

**Expected:**
- Uses `organization_job_postings` tool
- Returns active job listings
- Shows role titles and departments
- Indicates if no postings found

---

## Contact Management Tests

### Query 8: Search Contacts
```
Search my Apollo CRM for contacts with "Engineering" in their title
```

**Expected:**
- Uses `contact_search` tool
- Returns contacts from YOUR CRM (not global search)
- Shows contact details
- Returns empty if no matches

### Query 9: Create Contact
```
Create a new contact in my Apollo CRM:
- Name: Jane Smith
- Email: jane.smith@example.com
- Title: VP of Engineering
- Company: Example Corp
- Add to list: "Q1 Targets"
```

**Expected:**
- Uses `contact_create` tool
- Creates contact successfully
- Assigns to list (creates list if doesn't exist)
- Returns contact ID

### Query 10: Update Contact
```
Update the contact with ID [contact_id from previous query]:
- Change title to "SVP of Engineering"
- Add to list: "High Priority"
```

**Expected:**
- Uses `contact_update` tool
- Updates title
- Manages list membership
- Returns updated contact

### Query 11: Bulk Create Contacts
```
Bulk create these 3 contacts in my Apollo CRM:

1. John Doe, john@tech.com, CTO at Tech Inc
2. Alice Wong, alice@startup.io, CEO at Startup IO
3. Bob Lee, bob@corp.com, VP Sales at Corp Inc

Add all to the "New Leads" list.
```

**Expected:**
- Uses `contact_bulk_create` tool
- Creates 3 contacts in one API call
- All assigned to "New Leads" list
- Returns created contact IDs
- Handles duplicates gracefully

---

## Account Management Tests

### Query 12: Search Accounts
```
Search my Apollo CRM for accounts in the "Enterprise" list
```

**Expected:**
- Uses `account_search` tool
- Returns accounts from your CRM
- Filtered by list membership

### Query 13: Create Account (Requires Master API Key)
```
Create a new account in my Apollo CRM:
- Name: TechCorp Industries
- Domain: techcorp.com
- Add to list: "Target Accounts"
```

**Expected:**
- Uses `account_create` tool
- Creates account (if master key available)
- Returns 403 if using regular API key
- Clear error message about master key requirement

### Query 14: Add to List Safely
```
Add these account IDs to the "Q2 Pipeline" list:
- account_123
- account_456

Make sure we don't lose their existing lists.
```

**Expected:**
- Uses `account_add_to_list` tool
- Adds to list without losing existing labels
- Returns success status for each account

---

## Utility Tools Tests

### Query 15: List Labels (Requires Master API Key)
```
List all contact lists in my Apollo account
```

**Expected:**
- Uses `labels_list` tool with modality=contacts
- Returns all contact lists
- Or returns 403 with clear message about master key

### Query 16: Usage Stats (Requires Master API Key)
```
Get my Apollo.io API usage statistics.
How many requests have I used today?
```

**Expected:**
- Uses `usage_stats` tool
- Returns rate limit info per endpoint
- Shows used/remaining counts
- Or returns 403 with clear message about master key

### Query 17: List Custom Fields (Requires Master API Key)
```
List all custom fields for contacts in my Apollo account
```

**Expected:**
- Uses `custom_fields_list` tool
- Returns custom field definitions
- Shows field IDs, names, types
- Or returns 403 if no master key

---

## Error Handling Tests

### Query 18: Invalid Input
```
Search Apollo for people with an invalid query that has no filters
```

**Expected:**
- Handles gracefully
- Returns clear error message
- Doesn't crash the server

### Query 19: Rate Limiting
```
Make 10 search requests in quick succession:
[Repeat a search query 10 times]
```

**Expected:**
- Server handles rate limiting
- Waits when limits hit (doesn't return 429)
- All queries complete eventually
- Or clear message about waiting

### Query 20: Missing API Key
```
[Temporarily remove APOLLO_IO_API_KEY and restart]
Try to search for people
```

**Expected:**
- Clear error about missing API key
- Doesn't expose credentials
- Helpful error message

---

## Performance Tests

### Query 21: Large Results
```
Search Apollo for "Software Engineer" with no location filter.
Request 100 results.
```

**Expected:**
- Returns up to 100 results
- Response within 10 seconds
- No timeout errors
- Results paginated properly

### Query 22: Bulk Operations
```
Bulk create 50 contacts with random names in my CRM
```

**Expected:**
- Uses `contact_bulk_create`
- Completes in reasonable time
- Rate limiting handles bulk operation
- All contacts created or clear errors

---

## Integration Tests

### Query 23: Multi-Step Workflow
```
1. Search for VPs at Series B companies in Austin
2. Get the top 3 results
3. Enrich each person's data
4. Create contacts for them in my CRM with list "Prospects"
5. Show me the summary
```

**Expected:**
- Uses multiple tools in sequence
- `organization_search` -> `people_search` -> `people_enrichment` -> `contact_bulk_create`
- All steps complete successfully
- Creates contacts with enriched data

### Query 24: Search and Organize
```
1. Search for companies using React and Node.js in San Francisco
2. Get 5 companies
3. Create accounts for them in my CRM
4. Add them all to "Tech Stack Match" list
```

**Expected:**
- `organization_search` -> `account_bulk_create` -> `account_add_to_list`
- Chained operations work
- Final result shows all accounts in list

---

## Test Results Checklist

After running all queries:

- [ ] All search tools return results
- [ ] Enrichment tools work correctly
- [ ] Contact CRUD operations succeed
- [ ] Account operations work (or clear master key errors)
- [ ] Utility tools return data (or clear permission errors)
- [ ] Error handling is graceful
- [ ] Rate limiting prevents 429 errors
- [ ] Multi-step workflows complete
- [ ] Server remains stable (no crashes)
- [ ] Response times are acceptable (<5s for most queries)

## Success Criteria

**Pass:** All queries work as expected, with clear error messages for permission issues
**Partial:** Some queries work, but errors are unclear or server is unstable
**Fail:** Server crashes, returns no data, or gives unhelpful errors

## Next Steps After Testing

If all tests pass:
1. ✅ Server is production-ready
2. Share installation guide with users
3. Monitor for issues in real-world usage

If tests fail:
1. Review error logs
2. Fix identified issues
3. Re-run tests
4. Update documentation with any caveats
