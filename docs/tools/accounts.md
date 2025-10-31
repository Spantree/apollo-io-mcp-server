# Account Management Tools

Account tools allow you to manage companies/organizations saved to your Apollo CRM. All account write operations (create, update, bulk operations) **require a master API key**.

**Important Note**: Apollo's API uses `label_names` for what appears as "Lists" in the UI. These are the same thing.

---

## account_search

Search accounts (companies) saved to YOUR Apollo CRM. This searches your saved accounts, not Apollo's global database. For prospecting, use `organization_search` instead.

### Parameters

- **query** (optional): Search query - matches name, domain, etc.
- **label_ids** (optional): Filter by list IDs (Apollo calls these "labels")
- **page** (default: 1): Page number for pagination
- **per_page** (default: 25): Results per page (affects API performance)

### Returns

```json
{
  "accounts": [
    {
      "id": "account_123",
      "name": "Company Name",
      "domain": "example.com",
      "label_names": ["Enterprise", "Active"],
      "phone": "+1-555-0100",
      ...
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total_entries": 150,
    "total_pages": 6
  }
}
```

### Use Cases

- Find accounts by name or domain
- Filter accounts by assigned lists
- Get account_id for updates
- Review accounts before bulk operations

### Example

```python
# Search for all accounts
account_search(page=1, per_page=50)

# Search by domain
account_search(query="apollo.io")

# Filter by lists
account_search(label_ids=["label_123", "label_456"])
```

---

## account_create

Create a new account (company) in your Apollo CRM. **Requires master API key.**

### Parameters

- **name** (required): Company name
- **domain** (required): Company domain (without www or @)
- **phone** (optional): Company phone number
- **website_url** (optional): Company website
- **label_names** (optional): Lists to add account to (auto-created if don't exist)
- Additional fields: raw_address, city, state, postal_code, country, etc.

### Returns

```json
{
  "account": {
    "id": "account_123",
    "name": "Company Name",
    "domain": "example.com",
    "label_names": ["New Accounts"],
    ...
  }
}
```

### Use Cases

- Add new prospects to your CRM
- Import companies from external sources
- Create accounts discovered during prospecting

### Example

```python
account_create(
    name="Apollo.io",
    domain="apollo.io",
    phone="+1-415-555-0100",
    label_names=["Enterprise", "Active"]
)
```

---

## account_update

Update an existing account in your Apollo CRM. **Requires master API key.**

### Parameters

- **account_id** (required): Apollo account ID (from account_search)
- Any updatable fields: name, domain, phone, website_url, label_names, etc.

### Returns

```json
{
  "account": {
    "id": "account_123",
    "name": "Updated Name",
    ...
  }
}
```

### ⚠️ Important: Label Replacement Behavior

The `label_names` parameter **REPLACES ALL existing labels**. If an account has labels `["A", "B"]` and you update with `label_names=["C"]`, the account will ONLY have label `["C"]`.

**To safely add/remove labels, use the helper tools:**
- `account_add_to_list` - Adds a label while preserving existing ones
- `account_remove_from_list` - Removes a label while preserving others

### Use Cases

- Update account information
- Change account lists (use helpers for safety)
- Update contact details

### Example

```python
# Update phone number
account_update(
    account_id="account_123",
    phone="+1-555-0200"
)

# ⚠️ DANGER: This replaces ALL labels
account_update(
    account_id="account_123",
    label_names=["VIP"]  # Removes all other labels!
)
```

---

## account_bulk_create

Bulk create multiple accounts in a single API call. **Requires master API key.**

### Parameters

- **accounts** (required): Array of account objects (up to 100)
  - Each account needs: name, domain
  - Optional: phone, label_names, etc.

### Returns

```json
{
  "created_accounts": [
    {"id": "account_123", "name": "Company A", ...}
  ],
  "existing_accounts": [
    {"id": "account_456", "name": "Company B", ...}
  ]
}
```

### Behavior

- **created_accounts**: Newly created accounts
- **existing_accounts**: Accounts that already existed (matched by domain, **not updated**)

### Use Cases

- Import companies from CSV/spreadsheet
- Bulk add prospects from research
- Create accounts from organization_search results

### Example

```python
account_bulk_create(
    accounts=[
        {
            "name": "Company A",
            "domain": "companya.com",
            "label_names": ["Q1 Prospects"]
        },
        {
            "name": "Company B",
            "domain": "companyb.com",
            "label_names": ["Q1 Prospects"]
        }
    ]
)
```

---

## account_bulk_update

Bulk update multiple accounts in a single API call. Much more efficient than individual updates. **Requires master API key.**

### Parameters

- **accounts** (required): Array of update objects (up to 100)
  - Each object must have: **id** (account_id)
  - Optional: any updatable fields

### Returns

```json
{
  "accounts": [
    {"id": "account_123", "label_names": ["Updated"], ...}
  ]
}
```

### ⚠️ Important: Label Replacement

Same as `account_update` - `label_names` **REPLACES** all existing labels. Use the helper tools for safe label management.

### Use Cases

- Update multiple accounts at once
- Bulk reassign to different lists
- Update account information from external data

### Example

```python
account_bulk_update(
    accounts=[
        {
            "id": "account_123",
            "phone": "+1-555-0100"
        },
        {
            "id": "account_456",
            "label_names": ["Enterprise", "Active"]
        }
    ]
)
```

---

## account_add_to_list

**Helper tool** to safely add accounts to a list WITHOUT losing their existing labels. Handles up to 10 accounts. **Requires master API key.**

### Why This Tool Exists

Apollo's API has a critical limitation: the `label_names` parameter in `account_update` and `account_bulk_update` **REPLACES** all labels. If you want to add an account to a new list, you must:

1. Fetch current labels
2. Merge new label with existing labels
3. Update with complete list

This helper tool does all that automatically.

### Parameters

- **account_ids** (required): List of account IDs to add (max 10)
- **label_name** (required): Name of the list to add accounts to

### Returns

```json
{
  "found_ids": ["account_123", "account_456"],
  "not_found_ids": ["account_789"],
  "updated_accounts": [
    {
      "id": "account_123",
      "label_names": ["Existing Label", "New Label"]
    }
  ],
  "total_requested": 3
}
```

### Workflow

1. Fetches current accounts from your CRM (searches up to 1000 accounts)
2. Finds accounts matching the provided account_ids
3. Merges existing labels with new label (automatically deduplicates)
4. Performs bulk update with complete label list

### Use Cases

- Add accounts to campaigns without losing existing segmentation
- Safely organize accounts into multiple lists
- Add accounts to nurture sequences

### Example

```python
# Add two accounts to "Q1 Targets" list
account_add_to_list(
    account_ids=["account_123", "account_456"],
    label_name="Q1 Targets"
)

# Result: Accounts keep their existing labels AND get "Q1 Targets"
```

---

## account_remove_from_list

**Helper tool** to safely remove accounts from a list while preserving all other labels. Handles up to 10 accounts. **Requires master API key.**

### Why This Tool Exists

Same label replacement problem as above. To remove an account from one list without affecting other lists, you must:

1. Fetch current labels
2. Remove only the specified label
3. Update with remaining labels

This helper tool automates that process.

### Parameters

- **account_ids** (required): List of account IDs to remove (max 10)
- **label_name** (required): Name of the list to remove accounts from

### Returns

```json
{
  "found_ids": ["account_123"],
  "not_found_ids": ["account_456"],
  "updated_accounts": [
    {
      "id": "account_123",
      "label_names": ["Other Label"]  // "Removed Label" is gone
    }
  ],
  "total_requested": 2
}
```

### Workflow

1. Fetches current accounts from your CRM
2. Finds accounts matching the provided account_ids
3. Removes only the specified label from each account
4. Keeps all other labels intact
5. Performs bulk update

### Use Cases

- Remove accounts from completed campaigns
- Clean up account segmentation
- Move accounts between lists safely

### Example

```python
# Remove accounts from "Q1 Targets" but keep all other labels
account_remove_from_list(
    account_ids=["account_123", "account_456"],
    label_name="Q1 Targets"
)

# If account had ["Q1 Targets", "Enterprise", "Active"]
# After removal: ["Enterprise", "Active"]
```

---

## Best Practices

### Label Management

1. **Always use the helper tools** (`account_add_to_list`, `account_remove_from_list`) when managing lists
2. **Only use direct update** when you want to completely replace all labels
3. **Test with small batches** before bulk operations

### Bulk Operations

1. **Stay within limits**: 10 accounts for helpers, 100 for bulk operations
2. **Check found_ids**: Always verify which accounts were actually updated
3. **Handle not_found_ids**: Some accounts might not be in your CRM

### Master API Key

Account write operations require a master API key. To obtain one:
1. Contact your Apollo.io account manager
2. Request a master API key for your account
3. Store it in `.env.secrets` as `APOLLO_IO_API_KEY`

### Performance

- `account_search` pagination affects performance - use 25-50 per page
- Bulk operations are much faster than individual updates
- Helper tools search up to 1000 accounts to find matches
