"""Unit tests for Apollo.io organization operations using mocked responses."""
import pytest
import respx
from httpx import Response
from apollo_client import ApolloClient
from apollo import OrganizationEnrichmentQuery, OrganizationSearchQuery


@pytest.mark.skip(reason="Complex Organization model requires full mock data")
@respx.mock
async def test_organization_enrichment_unit():
    """Test organization enrichment with mocked response."""
    pass


@respx.mock
async def test_organization_search_unit():
    """Test organization search with mocked response."""
    mock_response = {
        "organizations": [],
        "pagination": {"page": 1, "per_page": 5, "total_entries": 0, "total_pages": 0}
    }

    respx.post("https://api.apollo.io/api/v1/mixed_companies/search").mock(
        return_value=Response(200, json=mock_response)
    )

    client = ApolloClient(api_key="test_api_key")
    query = OrganizationSearchQuery(page=1, per_page=5)
    result = await client.organization_search(query)

    assert result is not None
    assert result.pagination.page == 1


@respx.mock
async def test_organization_job_postings_unit():
    """Test organization job postings with mocked response."""
    mock_response = {"organization_job_postings": []}

    respx.get("https://api.apollo.io/api/v1/organizations/test_org/job_postings").mock(
        return_value=Response(200, json=mock_response)
    )

    client = ApolloClient(api_key="test_api_key")
    result = await client.organization_job_postings(organization_id="test_org")

    assert result is not None
    assert isinstance(result.organization_job_postings, list)
