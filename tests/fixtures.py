"""
Anonymized fixtures for unit tests.

These fixtures are based on real API responses from VCR cassettes
but with all personal/sensitive data anonymized.
"""

# Empty search results response
CONTACTS_SEARCH_NO_RESULTS = {
    "contacts": [],
    "breadcrumbs": [],
    "partial_results_only": False,
    "has_join": False,
    "disable_eu_prospecting": False,
    "partial_results_limit": 10000,
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total_entries": 0,
        "total_pages": 0
    },
    "num_fetch_result": None
}

# Search results with pagination
CONTACTS_SEARCH_WITH_RESULTS = {
    "contacts": [
        {
            "id": "test_contact_1",
            "first_name": "Jane",
            "last_name": "Doe",
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "title": "Senior Product Manager",
            "organization_name": "Example Corp",
            "organization_id": "org_123",
            "contact_stage_id": "stage_123",
            "owner_id": "owner_123",
            "creator_id": "creator_123",
            "person_id": "person_123",
            "email_status": "verified",
            "email_from_customer": True,
            "linkedin_url": "http://www.linkedin.com/in/jane-doe",
            "headline": "Senior Product Manager",
            "present_raw_address": "San Francisco, California, United States",
            "city": "San Francisco",
            "state": "California",
            "country": "United States",
            "time_zone": "America/Los_Angeles",
            "label_ids": ["label_1"],
            "contact_emails": [
                {
                    "email": "jane.doe@example.com",
                    "email_status": "verified",
                    "position": 0,
                    "free_domain": False
                }
            ],
            "phone_numbers": [],
            "account": {
                "id": "account_123",
                "name": "Example Corp",
                "domain": "example.com",
                "website_url": "http://www.example.com"
            },
            "organization": {
                "id": "org_123",
                "name": "Example Corp",
                "website_url": "http://www.example.com",
                "primary_domain": "example.com"
            }
        },
        {
            "id": "test_contact_2",
            "first_name": "John",
            "last_name": "Smith",
            "name": "John Smith",
            "email": "john.smith@testco.com",
            "title": "Software Engineer",
            "organization_name": "Test Company",
            "organization_id": "org_456",
            "contact_stage_id": "stage_123",
            "owner_id": "owner_123",
            "creator_id": "creator_123",
            "person_id": "person_456",
            "email_status": "verified",
            "email_from_customer": True,
            "linkedin_url": "http://www.linkedin.com/in/john-smith",
            "headline": "Software Engineer",
            "present_raw_address": "New York, New York, United States",
            "city": "New York",
            "state": "New York",
            "country": "United States",
            "time_zone": "America/New_York",
            "label_ids": [],
            "contact_emails": [
                {
                    "email": "john.smith@testco.com",
                    "email_status": "verified",
                    "position": 0,
                    "free_domain": False
                }
            ],
            "phone_numbers": [],
            "account": {
                "id": "account_456",
                "name": "Test Company",
                "domain": "testco.com",
                "website_url": "http://www.testco.com"
            },
            "organization": {
                "id": "org_456",
                "name": "Test Company",
                "website_url": "http://www.testco.com",
                "primary_domain": "testco.com"
            }
        }
    ],
    "breadcrumbs": [],
    "partial_results_only": False,
    "has_join": False,
    "disable_eu_prospecting": False,
    "partial_results_limit": 10000,
    "pagination": {
        "page": 1,
        "per_page": 5,
        "total_entries": 42,
        "total_pages": 9
    },
    "num_fetch_result": None
}

# Contact create response
CONTACT_CREATE_RESPONSE = {
    "contact": {
        "id": "created_contact_123",
        "first_name": "Test",
        "last_name": "Contact",
        "name": "Test Contact",
        "email": "test.contact@example.com",
        "title": "Test Engineer",
        "organization_name": "Test Organization",
        "organization_id": "test_org_123",
        "contact_stage_id": "stage_123",
        "owner_id": "owner_123",
        "creator_id": "creator_123",
        "person_id": None,
        "email_needs_tickling": False,
        "source": "api",
        "original_source": "api",
        "headline": None,
        "photo_url": None,
        "present_raw_address": None,
        "linkedin_uid": None,
        "linkedin_url": None,
        "extrapolated_email_confidence": None,
        "salesforce_id": None,
        "salesforce_lead_id": None,
        "salesforce_contact_id": None,
        "salesforce_account_id": None,
        "crm_owner_id": None,
        "created_at": "2025-10-30T20:17:16.128Z",
        "emailer_campaign_ids": [],
        "direct_dial_status": None,
        "direct_dial_enrichment_failed_at": None,
        "email_status": "verified",
        "email_source": None,
        "account_id": None,
        "last_activity_date": None,
        "hubspot_vid": None,
        "hubspot_company_id": None,
        "crm_id": None,
        "sanitized_phone": None,
        "merged_crm_ids": None,
        "updated_at": "2025-10-30T20:17:16.195Z",
        "queued_for_crm_push": True,
        "suggested_from_rule_engine_config_id": None,
        "email_unsubscribed": None,
        "person_deleted": None,
        "call_opted_out": None,
        "street_address": None,
        "city": None,
        "state": None,
        "country": None,
        "postal_code": None,
        "formatted_address": None,
        "time_zone": None,
        "label_ids": ["test_label_123"],
        "has_pending_email_arcgate_request": False,
        "has_email_arcgate_request": False,
        "existence_level": "full",
        "email_from_customer": True,
        "typed_custom_fields": {},
        "custom_field_errors": {},
        "crm_record_url": None,
        "email_status_unavailable_reason": None,
        "email_true_status": "User Managed",
        "updated_email_true_status": True,
        "source_display_name": "Created from API",
        "twitter_url": None,
        "facebook_url": None,
        "contact_roles": [],
        "contact_campaign_statuses": [],
        "contact_emails": [
            {
                "email_md5": "test_md5_hash",
                "email_sha256": "test_sha256_hash",
                "email_status": "verified",
                "extrapolated_email_confidence": None,
                "position": 0,
                "email": "test.contact@example.com",
                "free_domain": False,
                "source": "User Managed",
                "third_party_vendor_name": None,
                "vendor_validation_statuses": [],
                "email_needs_tickling": False,
                "email_true_status": "User Managed",
                "email_status_unavailable_reason": None
            }
        ],
        "next_contact_id": None,
        "intent_strength": None,
        "show_intent": False,
        "phone_numbers": [],
        "account_phone_note": None,
        "free_domain": False,
        "email_domain_catchall": False
    },
    "labels": [
        {
            "id": "test_label_123",
            "modality": "contacts",
            "cached_count": 0,
            "name": "MCP Test",
            "created_at": "2025-10-30T20:16:01.248Z",
            "updated_at": "2025-10-30T20:17:16.171Z",
            "user_id": "test_user_123"
        }
    ]
}

# Contact update response
CONTACT_UPDATE_RESPONSE = {
    "contact": {
        "id": "created_contact_123",
        "first_name": "Test",
        "last_name": "Contact",
        "name": "Test Contact",
        "email": "test.contact@example.com",
        "title": "Senior Test Engineer",  # Updated title
        "organization_name": "Test Organization",
        "organization_id": "test_org_123",
        "contact_stage_id": "stage_123",
        "owner_id": "owner_123",
        "creator_id": "creator_123",
        "person_id": None,
        "email_needs_tickling": False,
        "source": "api",
        "original_source": "api",
        "headline": None,
        "photo_url": None,
        "present_raw_address": None,
        "linkedin_uid": None,
        "linkedin_url": None,
        "extrapolated_email_confidence": None,
        "salesforce_id": None,
        "salesforce_lead_id": None,
        "salesforce_contact_id": None,
        "salesforce_account_id": None,
        "crm_owner_id": None,
        "created_at": "2025-10-30T20:17:16.128Z",
        "emailer_campaign_ids": [],
        "direct_dial_status": None,
        "direct_dial_enrichment_failed_at": None,
        "email_status": "verified",
        "email_source": None,
        "account_id": None,
        "last_activity_date": None,
        "hubspot_vid": None,
        "hubspot_company_id": None,
        "crm_id": None,
        "sanitized_phone": None,
        "merged_crm_ids": None,
        "updated_at": "2025-10-30T20:17:16.195Z",
        "queued_for_crm_push": True,
        "suggested_from_rule_engine_config_id": None,
        "email_unsubscribed": None,
        "person_deleted": None,
        "call_opted_out": None,
        "street_address": None,
        "city": None,
        "state": None,
        "country": None,
        "postal_code": None,
        "formatted_address": None,
        "time_zone": None,
        "label_ids": ["test_label_123", "test_label_456"],  # Updated labels
        "has_pending_email_arcgate_request": False,
        "has_email_arcgate_request": False,
        "existence_level": "full",
        "email_from_customer": True,
        "typed_custom_fields": {},
        "custom_field_errors": {},
        "crm_record_url": None,
        "email_status_unavailable_reason": None,
        "email_true_status": "User Managed",
        "updated_email_true_status": True,
        "source_display_name": "Created from API",
        "twitter_url": None,
        "facebook_url": None,
        "contact_roles": [],
        "contact_emails": [
            {
                "email_md5": "test_md5_hash",
                "email_sha256": "test_sha256_hash",
                "email_status": "verified",
                "extrapolated_email_confidence": None,
                "position": 0,
                "email": "test.contact@example.com",
                "free_domain": False,
                "source": "User Managed",
                "third_party_vendor_name": None,
                "vendor_validation_statuses": [],
                "email_needs_tickling": False,
                "email_true_status": "User Managed",
                "email_status_unavailable_reason": None
            }
        ],
        "next_contact_id": None,
        "intent_strength": None,
        "show_intent": False,
        "phone_numbers": [],
        "account_phone_note": None,
        "free_domain": False,
        "email_domain_catchall": False
    },
    "labels": [
        {
            "id": "test_label_123",
            "modality": "contacts",
            "cached_count": 0,
            "name": "MCP Test",
            "created_at": "2025-10-30T20:16:01.248Z",
            "updated_at": "2025-10-30T20:17:16.171Z",
            "user_id": "test_user_123"
        },
        {
            "id": "test_label_456",
            "modality": "contacts",
            "cached_count": 0,
            "name": "Updated",
            "created_at": "2025-10-30T20:16:01.695Z",
            "updated_at": "2025-10-30T20:17:16.579Z",
            "user_id": "test_user_123"
        }
    ]
}

# Labels list response - all labels (mixed modalities)
LABELS_LIST_ALL = [
    {
        "id": "label_contact_1",
        "name": "Sales Prospects",
        "modality": "contacts",
        "cached_count": 42,
        "team_id": "team_123",
        "user_id": "user_123",
        "created_at": "2024-01-15T10:00:00.000Z",
        "updated_at": "2024-01-20T15:30:00.000Z"
    },
    {
        "id": "label_account_1",
        "name": "Enterprise Clients",
        "modality": "accounts",
        "cached_count": 15,
        "team_id": "team_123",
        "user_id": "user_123",
        "created_at": "2024-01-10T09:00:00.000Z",
        "updated_at": "2024-01-18T12:00:00.000Z"
    },
    {
        "id": "label_contact_2",
        "name": "MCP Test",
        "modality": "contacts",
        "cached_count": 2,
        "team_id": "team_123",
        "user_id": "user_123",
        "created_at": "2025-10-30T20:16:01.248Z",
        "updated_at": "2025-10-30T20:17:16.171Z"
    },
    {
        "id": "label_account_2",
        "name": "Target Accounts",
        "modality": "accounts",
        "cached_count": 8,
        "team_id": "team_123",
        "user_id": "user_123",
        "created_at": "2024-02-01T11:00:00.000Z",
        "updated_at": "2024-02-05T14:30:00.000Z"
    }
]

# Labels list response - contacts only
LABELS_LIST_CONTACTS = [
    {
        "id": "label_contact_1",
        "name": "Sales Prospects",
        "modality": "contacts",
        "cached_count": 42,
        "team_id": "team_123",
        "user_id": "user_123",
        "created_at": "2024-01-15T10:00:00.000Z",
        "updated_at": "2024-01-20T15:30:00.000Z"
    },
    {
        "id": "label_contact_2",
        "name": "MCP Test",
        "modality": "contacts",
        "cached_count": 2,
        "team_id": "team_123",
        "user_id": "user_123",
        "created_at": "2025-10-30T20:16:01.248Z",
        "updated_at": "2025-10-30T20:17:16.171Z"
    }
]

# Labels list response - accounts only
LABELS_LIST_ACCOUNTS = [
    {
        "id": "label_account_1",
        "name": "Enterprise Clients",
        "modality": "accounts",
        "cached_count": 15,
        "team_id": "team_123",
        "user_id": "user_123",
        "created_at": "2024-01-10T09:00:00.000Z",
        "updated_at": "2024-01-18T12:00:00.000Z"
    },
    {
        "id": "label_account_2",
        "name": "Target Accounts",
        "modality": "accounts",
        "cached_count": 8,
        "team_id": "team_123",
        "user_id": "user_123",
        "created_at": "2024-02-01T11:00:00.000Z",
        "updated_at": "2024-02-05T14:30:00.000Z"
    }
]

# Contact bulk create response
CONTACT_BULK_CREATE_RESPONSE = {
    "created_contacts": [
        {
            "id": "bulk_created_1",
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com",
            "title": "Product Manager",
            "organization_name": "Test Corp",
            "source": "api",
            "label_ids": ["test_label_123"],
            "created_at": "2025-10-30T20:30:00.000Z"
        },
        {
            "id": "bulk_created_2",
            "first_name": "Bob",
            "last_name": "Jones",
            "email": "bob.jones@testco.com",
            "title": "Engineer",
            "organization_name": "Test Company",
            "source": "api",
            "label_ids": ["test_label_123"],
            "created_at": "2025-10-30T20:30:00.100Z"
        }
    ],
    "existing_contacts": [
        {
            "id": "existing_contact_1",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "title": "Senior Product Manager",
            "organization_name": "Example Corp",
            "source": "import",
            "label_ids": ["label_1"],
            "created_at": "2025-10-15T10:00:00.000Z"
        }
    ]
}

# Contact bulk update response
CONTACT_BULK_UPDATE_RESPONSE = {
    "contacts": [
        {
            "id": "bulk_created_1",
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com",
            "title": "Senior Product Manager",  # Updated
            "organization_name": "Test Corp",
            "source": "api",
            "label_ids": ["test_label_123", "test_label_456"],  # Updated
            "updated_at": "2025-10-30T20:35:00.000Z"
        },
        {
            "id": "bulk_created_2",
            "first_name": "Bob",
            "last_name": "Jones",
            "email": "bob.jones.new@testco.com",  # Updated
            "title": "Engineer",
            "organization_name": "Test Company",
            "source": "api",
            "label_ids": ["test_label_123"],
            "updated_at": "2025-10-30T20:35:00.100Z"
        }
    ]
}

# Usage stats response
USAGE_STATS_RESPONSE = {
    "api/v1/mixed_people/search": {
        "minute": {
            "limit": 60,
            "consumed": 12,
            "left_over": 48
        },
        "hour": {
            "limit": 600,
            "consumed": 145,
            "left_over": 455
        },
        "day": {
            "limit": 5000,
            "consumed": 823,
            "left_over": 4177
        }
    },
    "api/v1/contacts/search": {
        "minute": {
            "limit": 60,
            "consumed": 5,
            "left_over": 55
        },
        "hour": {
            "limit": 600,
            "consumed": 42,
            "left_over": 558
        },
        "day": {
            "limit": 5000,
            "consumed": 234,
            "left_over": 4766
        }
    },
    "api/v1/contacts/bulk_create": {
        "minute": {
            "limit": 10,
            "consumed": 2,
            "left_over": 8
        },
        "hour": {
            "limit": 100,
            "consumed": 15,
            "left_over": 85
        },
        "day": {
            "limit": 1000,
            "consumed": 87,
            "left_over": 913
        }
    }
}

# Account search - no results
ACCOUNTS_SEARCH_NO_RESULTS = {
    "accounts": [],
    "pagination": {
        "page": 1,
        "per_page": 25,
        "total_entries": 0,
        "total_pages": 0
    }
}

# Account search - with results
ACCOUNTS_SEARCH_WITH_RESULTS = {
    "accounts": [
        {
            "id": "account_123",
            "name": "Example Corp",
            "domain": "example.com",
            "team_id": "team_123",
            "organization_id": "org_123",
            "owner_id": "owner_123",
            "phone": "+1-555-0100",
            "label_names": ["Enterprise Clients"],
            "created_at": "2024-01-15T10:00:00.000Z"
        },
        {
            "id": "account_456",
            "name": "Test Company",
            "domain": "testco.com",
            "team_id": "team_123",
            "organization_id": "org_456",
            "owner_id": "owner_123",
            "phone": "+1-555-0200",
            "label_names": ["Target Accounts"],
            "created_at": "2024-02-01T11:00:00.000Z"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 25,
        "total_entries": 2,
        "total_pages": 1
    }
}

# Account create response
ACCOUNT_CREATE_RESPONSE = {
    "account": {
        "id": "account_789",
        "name": "New Corp",
        "domain": "newcorp.com",
        "team_id": "team_123",
        "organization_id": "org_789",
        "owner_id": "owner_123",
        "phone": "+1-555-0300",
        "label_names": ["New Accounts"],
        "source": "api",
        "created_at": "2025-10-30T21:00:00.000Z"
    }
}

# Account update response
ACCOUNT_UPDATE_RESPONSE = {
    "account": {
        "id": "account_123",
        "name": "Example Corp Updated",
        "domain": "example.com",
        "team_id": "team_123",
        "organization_id": "org_123",
        "owner_id": "owner_123",
        "phone": "+1-555-0100",
        "label_names": ["Enterprise Clients", "High Priority"],
        "updated_at": "2025-10-30T21:05:00.000Z"
    }
}

# Account bulk create response
ACCOUNT_BULK_CREATE_RESPONSE = {
    "created_accounts": [
        {
            "id": "bulk_account_1",
            "name": "Bulk Corp 1",
            "domain": "bulkcorp1.com",
            "team_id": "team_123",
            "organization_id": "org_bulk_1",
            "source": "api",
            "label_names": ["Bulk Import"],
            "created_at": "2025-10-30T21:10:00.000Z"
        },
        {
            "id": "bulk_account_2",
            "name": "Bulk Corp 2",
            "domain": "bulkcorp2.com",
            "team_id": "team_123",
            "organization_id": "org_bulk_2",
            "source": "api",
            "label_names": ["Bulk Import"],
            "created_at": "2025-10-30T21:10:00.100Z"
        }
    ],
    "existing_accounts": [
        {
            "id": "account_123",
            "name": "Example Corp",
            "domain": "example.com",
            "team_id": "team_123",
            "organization_id": "org_123",
            "label_names": ["Enterprise Clients"],
            "created_at": "2024-01-15T10:00:00.000Z"
        }
    ]
}

# Account bulk update response
ACCOUNT_BULK_UPDATE_RESPONSE = {
    "accounts": [
        {
            "id": "account_123",
            "name": "Example Corp",
            "domain": "example.com",
            "team_id": "team_123",
            "organization_id": "org_123",
            "label_names": ["Enterprise Clients", "Q1 Targets"],
            "updated_at": "2025-10-30T21:15:00.000Z"
        },
        {
            "id": "account_456",
            "name": "Test Company",
            "domain": "testco.com",
            "team_id": "team_123",
            "organization_id": "org_456",
            "label_names": ["Target Accounts", "Q1 Targets"],
            "updated_at": "2025-10-30T21:15:00.100Z"
        }
    ]
}

# Bulk people enrichment response
BULK_PEOPLE_ENRICHMENT_RESPONSE = {
    "status": "success",
    "total_requested_enrichments": 3,
    "unique_enriched_records": 2,
    "missing_records": 1,
    "credits_consumed": 0,
    "matches": [
        {
            "id": "person_123",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "title": "Senior Product Manager",
            "organization": {
                "id": "org_123",
                "name": "Example Corp"
            }
        },
        {
            "id": "person_456",
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@testco.com",
            "title": "Engineering Manager",
            "organization": {
                "id": "org_456",
                "name": "Test Company"
            }
        }
    ]
}
