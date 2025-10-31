"""
Integration tests for Apollo.io organization operations.

These tests make real API calls and record them with VCR.py.
Cassettes are stored in .scratch/http-tests/ (not committed).

To run these tests:
    pytest -m integration

By default, these tests are skipped (see pyproject.toml).
"""
import pytest
import vcr
from pathlib import Path
from apollo_client import ApolloClient
from apollo import OrganizationEnrichmentQuery, OrganizationSearchQuery


# VCR configuration for all tests
vcr_config = vcr.VCR(
    cassette_library_dir=".scratch/http-tests",
    record_mode="once",  # Record once, then replay
    match_on=["method", "uri"],
    filter_headers=[("x-api-key", "REDACTED")],
    decode_compressed_response=True,
)


@pytest.mark.integration
async def test_organization_enrichment(apollo_api_key):
    """
    Test enriching organization data for a known company.

    This validates the Organization Enrichment endpoint.
    """
    with vcr_config.use_cassette("organization_enrichment.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # Enrich organization data for Apollo.io
        query = OrganizationEnrichmentQuery(domain="apollo.io")
        result = await client.organization_enrichment(query)

        # Should return successful response
        assert result is not None
        assert hasattr(result, 'organization')

        org = result.organization
        assert hasattr(org, 'id')
        assert org.id is not None
        assert org.primary_domain == 'apollo.io'


@pytest.mark.integration
async def test_organization_search(apollo_api_key):
    """
    Test searching for organizations with filters.

    This validates the Organization Search endpoint.
    """
    with vcr_config.use_cassette("organization_search.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # Search for organizations with employee range filter
        query = OrganizationSearchQuery(
            organization_num_employees_ranges=["1,10"],
            page=1,
            per_page=5
        )
        result = await client.organization_search(query)

        # Should return successful response
        assert result is not None
        assert hasattr(result, 'organizations')
        assert hasattr(result, 'pagination')
        assert isinstance(result.organizations, list)

        # Validate pagination
        assert result.pagination.page == 1
        assert result.pagination.per_page == 5


@pytest.mark.integration
async def test_organization_job_postings(apollo_api_key):
    """
    Test getting job postings for a specific organization.

    This validates the Organization Job Postings endpoint.
    """
    with vcr_config.use_cassette("organization_job_postings.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # Get job postings for Apollo.io's organization ID
        # Using a known organization ID from Apollo.io
        org_id = "5e66b6381e05b4008c8331b8"
        result = await client.organization_job_postings(organization_id=org_id)

        # Should return successful response
        assert result is not None
        assert hasattr(result, 'organization_job_postings')
        assert isinstance(result.organization_job_postings, list)
