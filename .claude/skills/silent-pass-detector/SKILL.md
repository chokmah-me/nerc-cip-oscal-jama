---
name: silent-pass-detector
description: Detect tests that pass silently when validating zero items. Use when user says "check test quality", "find silent pass tests", or "validate test coverage".
---

# Silent Pass Detector

## 🎯 Purpose

Identify tests that pass silently because they validated **zero items** rather than validating successfully. Catches the real-world bug where loops with conditional assertions pass when the condition is never met, leaving zero validations and a false sense of security.

## 🚀 Key Features

- **AST-based pattern detection** - Analyzes Python test files for risky assertion patterns
- **Risk scoring** - Classifies findings as HIGH, MEDIUM, or LOW risk with clear rationale
- **Actionable fix suggestions** - Provides code snippets to add validation counters and minimum count assertions
- **Real-world focused** - Detects patterns from actual test failures (e.g., Test 23 of verify_oscal_compliance.py)
- **pytest/unittest compatible** - Works with both testing frameworks

## 📋 Usage

When user requests test quality analysis or mentions tests that passed unexpectedly:

1. Run analysis on the test file: `detector.py <test_file.py>`
2. Scan output for HIGH risk tests first (top priority fixes)
3. Present findings with pattern explanation and concrete fix
4. Offer to apply fixes or create test verification

**Command line:**
```bash
python detector.py test_file.py
python detector.py test_file.py --output json
python detector.py test_file.py --severity HIGH
```

## 🎛️ Parameters

**File path** (required): Python test file to analyze

**Options:**
- `--output format` - JSON or text (default: text)
- `--severity level` - Filter by HIGH, MEDIUM, LOW (default: all)
- `--verbose` - Include code snippets in output

## 💡 Examples

### Example 1: Conditional Assertions in Loop (HIGH RISK)

**Problem test:**
```python
def test_nist_controls_exist(oscal_data):
    """This test passes with 0 validations if no NIST props exist."""
    components = oscal_data.get('components', [])
    for component in components:
        props = component.get('properties', [])
        for prop in props:
            if 'NIST' in prop.get('name', ''):
                assert validate_nist_control(prop['value'])
    # ← If no NIST properties found: 0 assertions executed → TEST PASSES
```

**Detection output:**
```
[HIGH RISK] test_nist_controls_exist (line 10)
Pattern: Conditional validation in nested loops
Issue: All assertions inside 'if NIST in prop_name' condition
Risk: If no properties match condition → 0 validations → test PASSES

Suggested fix:
    nist_count = 0
    # ... existing loop ...
    if 'NIST' in prop.get('name', ''):
        assert validate_nist_control(prop['value'])
        nist_count += 1

    assert nist_count > 0, "No NIST controls found!"
```

### Example 2: Property Filter with Silent Pass (HIGH RISK)

**Problem test:**
```python
def test_component_mappings(data):
    for component in data['components']:
        for prop in component.get('properties', []):
            if prop.get('type') == 'NIST-CSF':  # ← RISKY CONDITION
                assert prop.get('value'), "NIST-CSF value missing"
    # Passes with 0 assertions if no NIST-CSF properties exist
```

**Detection output:**
```
[HIGH RISK] test_component_mappings (line 5)
Pattern: Property name/type filtering in loop
Issue: All assertions depend on property type match
Risk: Empty result set → 0 validations → silent pass

Fix: Add validation counter
    csf_props = 0
    # ... validation loop ...
    csf_props += 1

    assert csf_props > 0, "No NIST-CSF properties found to validate!"
```

### Example 3: Nested Empty Loops (LOW RISK)

**Problem test:**
```python
def test_component_references(data):
    for component in data.get('components', []):  # Could be empty
        for ref in component.get('refs', []):      # Could be empty
            assert ref.get('id'), "Missing reference ID"
    # LOW risk: Caught by validation framework, but explicit check better
```

**Detection output:**
```
[LOW RISK] test_component_references (line 2)
Pattern: Nested empty loops
Issue: If outer loop has no items → 0 assertions
Risk: Uncommon but possible with empty test data

Recommended: Use pytest.skip() or explicit length check
    if not data.get('components'):
        pytest.skip("No components in test data")
```

## 🎁 Output

**Text report format:**
```
============================================================
Silent Pass Test Detection Report
============================================================

File: test_example.py
Tests analyzed: 25
Silent pass risks detected: 4

------------------------------------------------------------
[HIGH] test_nist_exists (line 12) - Pattern: conditional_assertion
[HIGH] test_mapping_valid (line 45) - Pattern: property_filter
[MEDIUM] test_refs_exist (line 78) - Pattern: optional_validation
[LOW] test_nested_data (line 102) - Pattern: nested_empty_loop
------------------------------------------------------------

Summary:
  HIGH:   2 tests (immediate fix needed)
  MEDIUM: 1 test (recommended fix)
  LOW:    1 test (optional improvement)
```

**JSON output format:**
```json
[
  {
    "test_name": "test_nist_exists",
    "line_number": 12,
    "risk_level": "HIGH",
    "pattern": "conditional_assertion",
    "issue": "All assertions inside if block",
    "fix_suggestion": "Add validation counter..."
  }
]
```

## ⚠️ Important Notes

- **Static analysis only** - Cannot detect all runtime silent passes; use in combination with test coverage tools
- **False positives possible** - Some conditional assertions are intentional (e.g., format-specific validation). Review fixes before applying.
- **Best used proactively** - Run on test files BEFORE committing to catch issues early
- **Not a substitute for pytest.skip()** - Use `pytest.skip()` for format/version-dependent tests; add counters for conditional validations
- **Complement with test coverage** - Use with coverage.py to ensure all code paths tested
- **Real-world discovery** - Patterns based on actual bugs found in OSCAL compliance testing

## Integration with Other Skills

- **quick-test-runner** - Run tests after applying fixes to verify they work correctly
- **anti-pattern-sniffer** - Similar AST-based pattern detection for Coq proofs
- **dead-code-hunter** - Complementary code quality analysis

## Best Practices

1. **Always verify fixes** - Run tests after applying counter-based fixes to ensure they catch real failures
2. **Document intentional conditional validation** - Add comments explaining why assertions are conditional
3. **Use meaningful counter names** - `nist_controls_validated` is clearer than `count`
4. **Check expected counts** - `assert count > 0` is good; `assert count == 5` is better if expected
5. **Integrate into CI/CD** - Run before merging to catch silent pass tests in PRs
