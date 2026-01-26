"""
Example: Tests with silent pass risks FIXED.

These tests now GUARANTEE validation or fail explicitly.
"""

import pytest


def test_nist_controls_exist_in_catalog(oscal_data):
    """
    FIXED: Now guarantees we validated at least one NIST control.

    If no NIST controls found, test FAILS with clear error message.
    """
    components = oscal_data.get('components', [])
    nist_controls_validated = 0  # ← ADD: validation counter

    for component in components:
        props = component.get('properties', [])
        for prop in props:
            if 'NIST' in prop.get('name', ''):
                assert prop.get('value'), "NIST control value missing"
                assert len(prop['value']) > 0, "Empty NIST control value"
                nist_controls_validated += 1  # ← ADD: count validations

    # ← ADD: Guarantee we validated something
    assert nist_controls_validated > 0, \
        "No NIST controls found - test validated nothing!"


def test_component_mappings_by_type(data):
    """
    FIXED: Explicitly verify that CSF mappings exist and were validated.

    If no CSF mappings found, test fails instead of passing silently.
    """
    csf_mappings_validated = 0  # ← ADD: counter

    for component in data.get('components', []):
        for prop in component.get('properties', []):
            if prop.get('type') == 'NIST-CSF-Mapping':
                assert prop.get('value'), "Missing CSF mapping value"
                assert '-' in prop['value'], "Invalid mapping format"
                csf_mappings_validated += 1  # ← ADD: increment

    # ← ADD: Guarantee at least one mapping was validated
    assert csf_mappings_validated > 0, \
        "No NIST-CSF-Mapping properties found to validate"


def test_references_exist_in_components(oscal_doc):
    """
    FIXED: Validate that references exist AND are checked.

    If no references found, test fails with explicit error.
    """
    components = oscal_doc.get('components', [])
    references_validated = 0  # ← ADD: counter

    for component in components:
        if 'references' in component:
            refs = component['references']
            if len(refs) > 0:
                for ref in refs:
                    assert ref.get('id'), "Reference missing ID"
                    assert ref.get('href'), "Reference missing href"
                    references_validated += 1  # ← ADD: count

    # ← ADD: Require at least one reference
    assert references_validated > 0, \
        "No references found in any component"


def test_compliance_statements_are_valid(catalog):
    """
    FIXED: Guarantee we validated non-legacy controls.

    If all controls are legacy, test fails. If no controls exist, test fails.
    """
    controls = catalog.get('controls', [])
    assert controls, "No controls in catalog"  # ← ADD: check data exists

    validated_controls = 0  # ← ADD: counter

    for control in controls:
        if 'legacy' in control.get('tags', []):
            continue  # Still skip legacy

        assert control.get('title'), "Control title missing"
        assert control.get('description'), "Control description missing"
        validated_controls += 1  # ← ADD: count

    # ← ADD: Require at least one non-legacy control
    assert validated_controls > 0, \
        "All controls are legacy - no valid controls to validate"


def test_optional_metadata_when_present(item):
    """
    FIXED: Either validate metadata explicitly or skip test.

    Use pytest.skip() for optional data, or add counter + assertion.
    """
    metadata = item.get('metadata')

    # Skip if metadata is missing (optional field)
    if not metadata:
        pytest.skip("No metadata in item - skipping optional metadata test")

    # If we reach here, metadata exists - validate it unconditionally
    assert 'modified' in metadata, "Metadata must have 'modified' field"
    assert metadata['modified'], "Modified timestamp cannot be empty"
    assert '-' in metadata['modified'], "Modified must be valid date format"


def test_nested_empty_loops(data):
    """
    FIXED: Explicit validation or skip.

    Check that data exists before asserting on nested iteration.
    """
    components = data.get('components', [])

    # ← ADD: Guarantee outer loop has items, or skip
    if not components:
        pytest.skip("No components in test data")

    properties_validated = 0  # ← ADD: counter

    for component in components:
        props = component.get('properties', [])

        for prop in props:
            assert prop.get('name'), "Property name missing"
            assert prop.get('value'), "Property value missing"
            properties_validated += 1  # ← ADD: count

    # ← ADD: Require at least one property to be validated
    assert properties_validated > 0, \
        "No properties found in any component"


def test_format_specific_validation(document):
    """
    FIXED: Be explicit about format requirements.

    Either require format or use pytest.skip().
    """
    # ← ADD: Explicitly require format or skip
    doc_format = document.get('format', '').lower()

    if 'json' not in doc_format:
        pytest.skip(f"Skipping JSON validation for {doc_format} format")

    # Now we KNOW it's JSON - validate with confidence
    assert document.get('schema'), "JSON schema missing"
    assert document.get('version'), "Version missing"

    # Test will always validate something if it doesn't skip


# ============================================================================
# BONUS EXAMPLE: Testing that CHECKS passed vs. data existence separately
# ============================================================================

def test_separate_data_validation(document):
    """
    BEST PRACTICE: Separate data existence check from validation logic.

    Use separate assertions for "data exists" vs "data is valid".
    """
    # STEP 1: Verify test data is valid (separate concern)
    assert document, "Document object is required"
    assert document.get('components'), "Document must have components"

    # STEP 2: Validate component structure
    components = document['components']
    validation_count = 0

    for component in components:
        props = component.get('properties', [])

        # This loop WILL execute because we verified components exist
        for prop in props:
            if 'required' in prop.get('tags', []):
                assert prop.get('value'), f"Required property {prop['name']} missing"
                validation_count += 1

    # STEP 3: If we expected to find required properties, check it
    # Only assert if we had reason to expect them
    if any('required' in c.get('properties', [{}])[0].get('tags', [])
           for c in components):
        assert validation_count > 0, "Expected required properties were not validated"
