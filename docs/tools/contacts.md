# Contact Management Tools

Contact tools allow you to manage individual people saved to your Apollo CRM. Contacts are distinct from accounts (companies) and can be associated with organizations.

---

## contact_search

Search contacts saved to YOUR Apollo CRM. Not a global search - only returns contacts you've already saved.

### Parameters

- query: Search by email, name, company, etc.
- page/per_page: Pagination

### Returns

{contacts[], pagination} - Returns contact_id needed for updates

### Use Cases

- Find contacts by email/name
- Get contact_id for updates
- Review saved contacts

---

## contact_create

Create a new contact in your Apollo CRM with optional list assignment.

### Parameters

- first_name, last_name (required)
- email, phone
- organization_name, title
- label_names: Lists to assign (auto-created if don't exist)

### Returns

{contact} with created contact data

### Important

Lists are auto-created if they don't exist. Use label_names parameter.

---

## contact_update

Update an existing contact. **label_names REPLACES all existing labels.**

### Parameters

- contact_id (required)
- Any updatable fields

### ⚠️ Label Replacement

label_names REPLACES all lists. To add to existing lists:
1. Use contact_search to get current label_names
2. Merge with new lists
3. Pass complete list to contact_update

---

## contact_bulk_create

Create up to 100 contacts in a single API call.

### Parameters

- contacts: Array of contact objects (max 100)

### Returns

- created_contacts: Newly created
- existing_contacts: Already existed (matched by email, NOT updated)

### Use Cases

- Import contacts from CSV
- Bulk add prospects

---

## contact_bulk_update

Update up to 100 contacts in a single operation.

### Parameters

- contacts: Array with id + fields to update (max 100)

### Important

Each contact must have id field. Only provided fields are updated.

See full examples in README.md
