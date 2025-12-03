"""
Unit tests for custom fields Pydantic models.

Tests model validation, serialization, and structure for:
- CustomField
- CustomFieldListResponse
- CustomFieldCreateRequest
- CustomFieldCreateResponse
"""
import pytest
from apollo.custom_fields import (
    CustomField,
    CustomFieldListResponse,
    CustomFieldCreateRequest,
    CustomFieldCreateResponse
)


def test_custom_field_model():
    """Test CustomField model with minimal required fields."""
    field = CustomField(
        id="cf_123",
        name="Company Industry",
        type="string",
        modality="account"
    )

    assert field.id == "cf_123"
    assert field.name == "Company Industry"
    assert field.type == "string"
    assert field.modality == "account"


def test_custom_field_with_picklist():
    """Test CustomField model with picklist options."""
    field = CustomField(
        id="cf_456",
        name="Company Size",
        type="picklist",
        modality="account",
        picklist_options=["1-10", "11-50", "51-200", "201+"]
    )

    assert field.type == "picklist"
    assert field.picklist_options == ["1-10", "11-50", "51-200", "201+"]


def test_custom_field_list_response():
    """Test CustomFieldListResponse with multiple fields."""
    response = CustomFieldListResponse(
        typed_custom_fields=[
            CustomField(
                id="cf_1",
                name="Field 1",
                type="string",
                modality="contact"
            ),
            CustomField(
                id="cf_2",
                name="Field 2",
                type="number",
                modality="account"
            )
        ]
    )

    assert len(response.typed_custom_fields) == 2
    assert response.typed_custom_fields[0].name == "Field 1"
    assert response.typed_custom_fields[1].type == "number"


def test_custom_field_create_request_minimal():
    """Test CustomFieldCreateRequest with minimal required fields."""
    request = CustomFieldCreateRequest(
        label="LinkedIn URL",
        type="string",
        modality="contact"
    )

    assert request.label == "LinkedIn URL"
    assert request.type == "string"
    assert request.modality == "contact"
    assert request.meta is None


def test_custom_field_create_request_with_picklist():
    """Test CustomFieldCreateRequest for picklist field."""
    request = CustomFieldCreateRequest(
        label="Industry",
        type="picklist",
        modality="account",
        meta={"picklist_options": ["Tech", "Finance", "Healthcare"]}
    )

    assert request.type == "picklist"
    assert request.meta is not None
    assert len(request.meta["picklist_options"]) == 3


def test_custom_field_create_response():
    """Test CustomFieldCreateResponse."""
    response = CustomFieldCreateResponse(
        typed_custom_field=CustomField(
            id="cf_new",
            name="New Field",
            type="boolean",
            modality="opportunity"
        )
    )

    assert response.typed_custom_field.id == "cf_new"
    assert response.typed_custom_field.type == "boolean"


def test_custom_field_serialization():
    """Test that CustomField can be serialized to dict."""
    field = CustomField(
        id="cf_test",
        name="Test Field",
        type="picklist",
        modality="contact",
        picklist_options=["Option A", "Option B"]
    )

    data = field.model_dump()
    assert data["id"] == "cf_test"
    assert data["type"] == "picklist"
    assert "Option A" in data["picklist_options"]


def test_field_types():
    """Test various field types are valid."""
    field_types = ["string", "textarea", "number", "date", "datetime", "boolean", "picklist"]

    for ft in field_types:
        field = CustomField(
            id=f"cf_{ft}",
            name=f"Test {ft}",
            type=ft,
            modality="contact"
        )
        assert field.type == ft


def test_modalities():
    """Test various modalities are valid."""
    modalities = ["contact", "account", "opportunity"]

    for modality in modalities:
        field = CustomField(
            id=f"cf_{modality}",
            name=f"Test {modality}",
            type="string",
            modality=modality
        )
        assert field.modality == modality


def test_custom_field_extra_fields():
    """Test that CustomField accepts extra fields from API."""
    field = CustomField(
        id="cf_extra",
        name="Test Field",
        type="string",
        modality="contact",
        # Extra fields from API response
        text_field_max_length=100,
        mirrored=False,
        is_local=True,
        system_name="test_field"
    )

    assert field.text_field_max_length == 100
    assert field.mirrored is False
    assert field.is_local is True
    assert field.system_name == "test_field"
