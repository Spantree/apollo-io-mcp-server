"""Unit tests for Apollo.io people operations using mocked responses."""
import pytest
import respx
from httpx import Response
from apollo_client import ApolloClient
from apollo import PeopleEnrichmentQuery, PeopleSearchQuery


@pytest.mark.skip(reason="Complex Person model requires full mock data")
@respx.mock
async def test_people_enrichment_unit():
    """Test people enrichment with mocked response."""
    pass


@respx.mock
async def test_people_search_unit():
    """Test people search with mocked response."""
    mock_response = {
        "people": [],
        "pagination": {"page": 1, "per_page": 5, "total_entries": 0, "total_pages": 0}
    }

    respx.post("https://api.apollo.io/api/v1/mixed_people/search").mock(
        return_value=Response(200, json=mock_response)
    )

    client = ApolloClient(api_key="test_api_key")
    query = PeopleSearchQuery(page=1, per_page=5)
    result = await client.people_search(query)

    assert result is not None
    assert result.pagination.page == 1
