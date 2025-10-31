# Utility Tools

---

## labels_list

List all labels/lists in your Apollo account. **Requires master API key.**

### Parameters

- modality (optional): Filter by type
  - "contacts": Contact lists only
  - "accounts": Account lists only  
  - "emailer_campaigns": Email campaign lists
  - None: All labels across all types

### Returns

{labels[]} with label objects containing:
- id, name, modality
- cached_count (number of items in list)

### Use Cases

- Get list IDs for filtering
- Review list organization
- Audit list usage

### Important

Requires MASTER API KEY. Regular keys get 403 error.

---

## usage_stats

Get API usage statistics and rate limits. **Requires master API key.**

### Returns

Rate limits per endpoint:
- minute, hour, day limits
- consumed and remaining counts

### Use Cases

- Monitor API usage
- Avoid rate limit errors
- Plan bulk operations

### Important

Requires MASTER API KEY. Regular keys get 403 error.

---

## Master API Key

Both utility endpoints require a master API key from Apollo.io:
1. Contact your Apollo.io account manager
2. Request master API key
3. Store in .env.secrets as APOLLO_IO_API_KEY

Regular API keys will receive 403 Forbidden errors.
