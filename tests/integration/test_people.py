"""Integration tests for Apollo.io people operations."""
import pytest
import vcr
from apollo_client import ApolloClient
from apollo import PeopleEnrichmentQuery, PeopleSearchQuery


vcr_config = vcr.VCR(
    cassette_library_dir=".scratch/http-tests",
    record_mode="once",
    match_on=["method", "uri"],
    filter_headers=[("x-api-key", "REDACTED")],
    decode_compressed_response=True,
)


@pytest.mark.integration
async def test_people_enrichment(apollo_api_key):
    """Test people enrichment endpoint."""
    with vcr_config.use_cassette("people_enrichment.yaml"):
        client = ApolloClient(api_key=apollo_api_key)
        query = PeopleEnrichmentQuery(first_name="Tim", last_name="Zheng")
        result = await client.people_enrichment(query)

        assert result is not None
        assert hasattr(result, 'person')


@pytest.mark.integration
async def test_people_search(apollo_api_key):
    """Test people search endpoint."""
    with vcr_config.use_cassette("people_search.yaml"):
        client = ApolloClient(api_key=apollo_api_key)
        query = PeopleSearchQuery(
            person_titles=["Engineer"],
            page=1,
            per_page=5
        )
        result = await client.people_search(query)

        assert result is not None
        assert hasattr(result, 'people')
        assert hasattr(result, 'pagination')
