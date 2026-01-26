"""
Example: Tests with silent pass risk patterns.

These tests pass when they validate ZERO items because all assertions
are inside conditional blocks that may never execute.
"""

import pytest


def test_nist_controls_exist_in_catalog(oscal_data):
    """
    RISKY: This test can pass with 0 validations.

    If oscal_data has no NIST control properties, the inner assertion
    is never executed, so the test passes silently without validating
    anything.
    """
    components = oscal_data.get('components', [])

    for component in components:
        props = component.get('properties', [])
        for prop in props:
            # ← RISKY: Assertion only runs if condition is true
            if 'NIST' in prop.get('name', ''):
                assert prop.get('value'), "NIST control value missing"
                assert len(prop['value']) > 0, "Empty NIST control value"

    # Test ends here. If no NIST properties found:
    # - 0 assertions executed
    # - Test PASSES
    # - Test appears to validate NIST controls but it DIDN'T


def test_component_mappings_by_type(data):
    """
    RISKY: Silent pass with property type filtering.

    All validations depend on finding a specific property type.
    If that property type doesn't exist, 0 assertions run.
    """
    for component in data.get('components', []):
        for prop in component.get('properties', []):
            # ← RISKY: Assertion only if type matches
            if prop.get('type') == 'NIST-CSF-Mapping':
                assert prop.get('value'), "Missing CSF mapping value"
                assert '-' in prop['value'], "Invalid mapping format"

    # If no NIST-CSF-Mapping properties: test PASSES with 0 validations


def test_references_exist_in_components(oscal_doc):
    """
    RISKY: Nested loop with conditional validation.

    Each component could have references. Test validates them only
    if they exist. If no references: 0 assertions.
    """
    components = oscal_doc.get('components', [])

    for component in components:
        # ← Assertion nested deep in conditions
        if 'references' in component:
            refs = component['references']
            if len(refs) > 0:
                for ref in refs:
                    assert ref.get('id'), "Reference missing ID"
                    assert ref.get('href'), "Reference missing href"

    # If no component has references: test PASSES with 0 validations


def test_compliance_statements_are_valid(catalog):
    """
    RISKY: Early continue skips all validations.

    Test loops through all controls but skips most of them.
    If all controls are skipped, 0 assertions run.
    """
    controls = catalog.get('controls', [])

    for control in controls:
        # ← RISKY: Early continue skips the assertion
        if 'legacy' in control.get('tags', []):
            continue  # Skip legacy controls

        # Only non-legacy controls reach this point
        assert control.get('title'), "Control title missing"
        assert control.get('description'), "Control description missing"

    # If ALL controls are legacy: 0 assertions executed → test PASSES


def test_optional_metadata_when_present(item):
    """
    RISKY: Optional validation never reaches assertion.

    Test validates optional metadata only if it exists.
    If metadata is always missing, 0 validations occur.
    """
    metadata = item.get('metadata')

    # ← RISKY: If metadata is None/empty, this block never executes
    if metadata:
        if 'modified' in metadata:
            assert metadata['modified'], "Modified timestamp empty"
            assert '-' in metadata['modified'], "Invalid date format"

    # If metadata is missing: test PASSES without validating anything


def test_nested_empty_loops(data):
    """
    LOW RISK: Nested loops could both be empty.

    Less common than conditional assertions, but still risky if
    outer loop is unexpectedly empty.
    """
    components = data.get('components', [])  # Could be empty

    for component in components:  # ← If empty: 0 iterations
        props = component.get('properties', [])

        for prop in props:  # ← Also could be empty
            assert prop.get('name'), "Property name missing"
            assert prop.get('value'), "Property value missing"

    # If components is empty: test PASSES with 0 assertions


def test_format_specific_validation(document):
    """
    MEDIUM RISK: Validation that's intentionally conditional.

    This pattern is sometimes intentional (e.g., only validate
    if document is in JSON format), but still risky if the
    condition makes assumptions about data.
    """
    if 'json' in document.get('format', '').lower():
        # Only validate JSON documents
        assert document.get('schema'), "JSON schema missing"
        assert document.get('version'), "Version missing"

    # If document is XML: 0 assertions → test PASSES
    # This might be intentional, but should be explicit
