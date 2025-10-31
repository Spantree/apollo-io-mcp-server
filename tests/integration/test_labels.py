"""
Integration tests for Apollo.io labels operations.

These tests make real API calls and record them with VCR.py.
Cassettes are stored in .scratch/http-tests/ (not committed).

To run these tests:
    pytest -m integration

By default, these tests are skipped (see pyproject.toml).

Note: labels_list endpoint requires a master API key.
"""
import pytest
import vcr
from pathlib import Path
from apollo_client import ApolloClient


# VCR configuration for all tests
vcr_config = vcr.VCR(
    cassette_library_dir=".scratch/http-tests",
    record_mode="once",  # Record once, then replay
    match_on=["method", "uri"],
    filter_headers=[("x-api-key", "REDACTED")],
    decode_compressed_response=True,
)


@pytest.mark.integration
async def test_labels_list_all(apollo_api_key):
    """
    Test listing all labels without filtering.

    This should return labels across all modalities (contacts, accounts, emailer_campaigns).
    """
    with vcr_config.use_cassette("labels_list_all.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # List all labels
        result = await client.labels_list()

        # Should return successful response
        assert result is not None
        assert hasattr(result, 'labels')
        assert isinstance(result.labels, list)

        # Should have at least some labels (assuming account has labels)
        # Note: This might be 0 for a brand new account, so we just check structure
        for label in result.labels:
            assert hasattr(label, 'id')
            assert hasattr(label, 'name')
            assert hasattr(label, 'modality')
            assert label.modality in ['contacts', 'accounts', 'emailer_campaigns']


@pytest.mark.integration
async def test_labels_list_contacts_only(apollo_api_key):
    """
    Test listing only contacts labels.

    This validates client-side filtering by modality.
    """
    with vcr_config.use_cassette("labels_list_contacts.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # List only contacts labels
        result = await client.labels_list(modality="contacts")

        # Should return successful response
        assert result is not None
        assert hasattr(result, 'labels')
        assert isinstance(result.labels, list)

        # All returned labels should have contacts modality
        for label in result.labels:
            assert label.modality == "contacts"


@pytest.mark.integration
async def test_labels_list_accounts_only(apollo_api_key):
    """
    Test listing only accounts labels.

    This validates client-side filtering by modality.
    """
    with vcr_config.use_cassette("labels_list_accounts.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # List only accounts labels
        result = await client.labels_list(modality="accounts")

        # Should return successful response
        assert result is not None
        assert hasattr(result, 'labels')
        assert isinstance(result.labels, list)

        # All returned labels should have accounts modality
        for label in result.labels:
            assert label.modality == "accounts"


@pytest.mark.integration
async def test_labels_response_structure(apollo_api_key):
    """
    Test the complete response structure of labels_list.

    This validates all expected fields in the Label model.
    """
    with vcr_config.use_cassette("labels_response_structure.yaml"):
        client = ApolloClient(api_key=apollo_api_key)

        # List all labels
        result = await client.labels_list()

        # Should return successful response
        assert result is not None
        assert hasattr(result, 'labels')

        # If there are labels, validate full structure
        if len(result.labels) > 0:
            label = result.labels[0]

            # Required fields
            assert hasattr(label, 'id')
            assert isinstance(label.id, str)
            assert hasattr(label, 'name')
            assert isinstance(label.name, str)
            assert hasattr(label, 'modality')
            assert isinstance(label.modality, str)

            # Optional fields (may be None)
            assert hasattr(label, 'cached_count')
            assert hasattr(label, 'team_id')
            assert hasattr(label, 'user_id')
            assert hasattr(label, 'created_at')
            assert hasattr(label, 'updated_at')
