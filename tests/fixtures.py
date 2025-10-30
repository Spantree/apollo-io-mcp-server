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
