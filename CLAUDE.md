# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**NERC-CIP OSCAL Toolkit** - Transforms unstructured NERC-CIP regulatory text into structured OSCAL v1.0.0 Catalogs with automatic mapping to NIST SP 800-53 controls.

**Key Purpose:** Generate machine-readable compliance JSON that bridges regulatory requirements (NERC), security controls (NIST), and requirements management systems (JAMA) for traceability matrices.

---

## Quick Start Commands

### Core Development Workflow

```bash
# Run all validation tests (27 tests)
pytest verify_oscal_compliance.py -v

# Run a single test class
pytest verify_oscal_compliance.py::TestOSCALCompliance -v

# Run specific test by name
pytest verify_oscal_compliance.py::TestOSCALCompliance::test_is_valid_json -v

# Run with verbose output and print statements
pytest verify_oscal_compliance.py -vv -s

# Export validated OSCAL JSON to JAMA CSV
python oscal_to_jama_csv.py nerc-oscal.json --validate

# Export with custom output filename
python oscal_to_jama_csv.py nerc-oscal.json -o my-matrix.csv

# Export with detailed metadata
python oscal_to_jama_csv.py nerc-oscal.json --format detailed
```

---

## Architecture & Data Flow

### Three-Layer Compliance Mapping

The toolkit implements a three-layer compliance mapping that converts regulatory text into actionable compliance evidence:

```
Layer 1: NERC-CIP Requirements (Regulatory Text)
   ↓ (AI parsing with claude-prompt)
Layer 2: OSCAL Component Definition (JSON structure)
   ├─ Properties: NERC-ID, NIST-ID, JAMA-ID
   ├─ Control-implementations: NIST 800-53 mappings
   └─ Metadata: version, uuid, timestamps
   ↓ (Validation + Export)
Layer 3: JAMA CSV Traceability Matrix (Requirements Management)
   └─ Importable into JAMA for linked requirements
```

### Core Data Structures

**OSCAL Component Definition** (nerc-oscal.json):
```json
{
  "component-definition": {
    "uuid": "unique-id",
    "metadata": {
      "title": "NERC-CIP Control Implementation",
      "published": "ISO-8601 timestamp",
      "version": "1.0.0"
    },
    "components": [
      {
        "uuid": "component-uuid",
        "title": "NERC CIP-XXX Requirement Title",
        "description": "Implementation details",
        "properties": [
          { "name": "NERC-Requirement-ID", "value": "CIP-005-6 R1" },
          { "name": "NIST-800-53-Primary-Control", "value": "SC-7" },
          { "name": "NIST-800-53-Secondary-Controls", "value": "CA-3, PL-2" },
          { "name": "JAMA-Requirement-ID", "value": "CIP-005-R1-a" },
          { "name": "Implementation-Status", "value": "Draft" }
        ],
        "control-implementations": [
          {
            "description": "NIST control mapping",
            "implemented-requirements": [
              {
                "control-id": "sc-7",
                "responsibility": "Implemented",
                "properties": [
                  { "name": "JAMA-Requirement-ID", "value": "CIP-005-R1-a" }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### File Organization

```
repo/
├── README.md                           # User-facing documentation
├── QUICK-START.md                      # 6-step workflow overview
├── TRAVIS-NERC-PROMPT.md              # AI prompt for OSCAL generation
├── verify_oscal_compliance.py          # Pytest validation suite (27 tests)
├── oscal_to_jama_csv.py               # CSV export utility
├── nist_controls.py                    # NIST SP 800-53 R5 catalog + validation
├── nerc-oscal.json                     # Generated OSCAL output (user-created)
├── nerc-oscal.csv                      # Generated JAMA matrix (user-created)
└── requirements.txt                    # Python dependencies
```

---

## Core Components

### 1. NIST Control Catalog (`nist_controls.py`)

**Purpose:** Validate that all mapped NIST controls exist in the official NIST SP 800-53 R5 catalog.

**Key Functions:**
- `validate_nist_control(control_id)`: Returns True if control exists in NIST R5
- `get_control_description(control_id)`: Retrieves official control description
- `get_control_family(control_id)`: Extracts family code (e.g., "SC" from "SC-7")
- `get_all_controls()`: Returns list of all 900+ NIST controls

**Architecture:**
```python
NIST_SP_800_53_R5_CONTROLS = {
    # ~900 controls organized by family
    "AC-1": "Policy and Procedures",           # Access Control family
    "AC-2": "Account Management",
    # ... SC-7, SC-8, etc. (System & Communications Protection)
    # ... and 13 other control families
}
```

The catalog is comprehensive but relatively static (based on NIST R5). Updates to R6 or higher would require updating this dictionary.

### 2. Validation Suite (`verify_oscal_compliance.py`)

**Purpose:** Ensure generated OSCAL JSON meets 27 different structural and semantic requirements.

**Test Organization (27 tests across 7 categories):**

| Category | Tests | Purpose |
|----------|-------|---------|
| Basic Validation | 5 | JSON syntax, root structure, metadata, components array |
| NIST Mapping | 3 | NIST control presence, format validity (SC-7), minimum controls per component |
| JAMA Placeholders | 3 | JAMA-ID presence, format (CIP-###-R#-[a-z]), no empty values |
| NERC Requirements | 2 | NERC-ID presence, format (CIP-###-6 R#) |
| OSCAL Structure | 5 | UUID presence, titles, descriptions, properties count |
| Control Implementation | 2 | control-implementations array, control-id specification |
| Quality & Export | 7 | Vague language detection, CSV export validation, empty ID checks |

**Key Test Patterns:**

```python
# Format validation using regex
jama_pattern = re.compile(r'^CIP-\d{3}-R\d+(-[a-z])?$')
nist_pattern = re.compile(r'^[A-Z]{2}-\d{1,2}(\s*\([0-9]+\))?$')

# Catalog validation
assert validate_nist_control(control_id), f"Control '{control_id}' not in NIST R5"

# CSV export testing
rows = oscal_to_jama_csv(oscal_file, output_csv)
assert 'JAMA-Requirement-ID' in rows[0], "CSV missing required column"
```

### 3. CSV Export Utility (`oscal_to_jama_csv.py`)

**Purpose:** Convert OSCAL JSON to JAMA-compatible CSV traceability matrices.

**Command-line Interface:**
```bash
python oscal_to_jama_csv.py nerc-oscal.json [OPTIONS]

Options:
  -o, --output FILE           Custom output CSV path
  --format [standard|detailed] CSV format (standard=7 cols, detailed=10 cols)
  --validate                  Validate CSV after export
```

**CSV Output Columns (Standard Format):**
- JAMA-Requirement-ID: CIP-005-R1-a
- NERC-Requirement-ID: CIP-005-6 R1
- NIST-Primary-Control: SC-7
- NIST-Secondary-Controls: CA-3, PL-2
- Title: Component title from OSCAL
- Description: Component description from OSCAL
- Implementation-Status: Draft, Implemented, etc.

**Detailed Format (adds):**
- Component-UUID: From OSCAL
- Component-Type: software, hardware, process
- Control-Count: Number of control-implementations

**Key Functions:**
- `load_oscal_json()`: Parse and validate JSON
- `extract_component_properties()`: Convert OSCAL properties array to dict
- `oscal_to_jama_csv()`: Main conversion logic
- `validate_csv_format()`: Check CSV structure and content

---

## NIST SP 800-53 R5 Reference

**Control Families (18 total):**
- AC: Access Control (22 controls)
- AU: Audit and Accountability (12 controls)
- CA: Security Assessment and Authorization (9 controls)
- CM: Configuration Management (14 controls)
- IA: Identification and Authentication (12 controls)
- SC: System and Communications Protection (44 controls)
- SR: Supply Chain Risk Management (12 controls)
- And 10 more...

**Control Format:**
- Base control: XX-# (e.g., SC-7, AC-2)
- Enhanced control: XX-#(n) (e.g., SC-7(1), AC-2(2))

**NERC-to-NIST Mapping Examples:**
- CIP-005 (System Security Management) → SC-7, CA-3, PL-2
- CIP-007 (System Security Administration) → SC-2, SC-3, AC-6
- CIP-010 (Configuration and Vulnerability Management) → CM-2, RA-5, SI-2

---

## Workflow: NERC-CIP Text → OSCAL → JAMA

### Step 1: Input Preparation
User extracts NERC requirement from official NERC documentation:
```
CIP-005-6 R1: Systems Security Management
The Responsible Entity shall implement one or more documented processes...
a) Roles and responsibilities
b) Methodology for assessing effectiveness
```

### Step 2: AI-Powered Transformation
User copies the TRAVIS-NERC-PROMPT.md into Claude Code with the NERC text. The prompt instructs Claude to:
1. Parse requirement ID (CIP-005-6 R1)
2. Map to NIST controls (SC-7 primary, CA-3, PL-2 secondary)
3. Generate OSCAL JSON with all required properties
4. Include JAMA placeholders (CIP-005-R1-a, CIP-005-R1-b, etc.)

### Step 3: Output Validation
User runs pytest to validate 27 requirements:
```bash
pytest verify_oscal_compliance.py -v

# Output:
# test_is_valid_json PASSED
# test_has_component_definition_root PASSED
# test_nist_controls_exist_in_catalog PASSED  ← Validates against nist_controls.py
# test_jama_placeholders_follow_format PASSED
# ... (24 more tests)
# ============ 27 passed in 0.89s ============
```

If any test fails, the error message guides users to fix the issue:
```
AssertionError: Component 0 maps to non-existent NIST control: 'ZZ-99'.
Verify control ID exists in NIST SP 800-53 R5 catalog.
Valid format: Family-Number (e.g., 'SC-7', 'AC-2', 'CA-3')
```

### Step 4: JAMA Export
```bash
python oscal_to_jama_csv.py nerc-oscal.json --validate

# Generates nerc-oscal.csv with 1 row per component
# Can be imported into JAMA for requirements management
```

---

## Programmatic NIST Generation (v1.1.4+)

### Overview
`generate_oscal.py` now supports programmatic generation of NIST mappings without manual prompting.

### Usage

**Generate OSCAL with NIST mappings:**
```bash
python generate_oscal.py input_nerc_requirements.txt -o nerc-oscal.json
```

**With gap analysis:**
```bash
python generate_oscal.py input_nerc_requirements.txt --gap-analysis -o nerc-oscal.json
```

### How It Works

1. **Parse Requirements** - Extracts NERC requirement IDs and descriptions from input
2. **Generate NIST Mappings** - Uses Claude API to intelligently map to NIST SP 800-53 R5
3. **Validate Controls** - Verifies all mapped controls exist in nist_controls.py
4. **Build OSCAL JSON** - Constructs OSCAL-compliant component definitions
5. **Detect Gaps** - (Optional) Identifies unmapped NERC requirements

### Integration with Validation Suite

Generated OSCAL files are immediately testable:
```bash
# After generation, validate the output
pytest verify_oscal_compliance.py -v

# Export to JAMA for requirements management
python oscal_to_jama_csv.py nerc-oscal.json --validate
```

---

## Common Development Tasks

### Adding a New NIST Control
1. Identify the control ID (e.g., "AA-1")
2. Add to `NIST_SP_800_53_R5_CONTROLS` dictionary in nist_controls.py:
   ```python
   "AA-1": "New Control Family - Control Name",
   ```
3. Re-run tests to verify: `pytest verify_oscal_compliance.py::TestOSCALCompliance::test_nist_controls_exist_in_catalog -v`

### Creating a New Validation Test
Tests use pytest fixtures for OSCAL file loading:
```python
def test_my_new_requirement(self, oscal_data):
    """Test 28: My new validation requirement."""
    comp_def = oscal_data.get('component-definition', {})
    components = comp_def.get('components', [])

    for i, component in enumerate(components):
        # Your assertion here
        assert some_condition, f"Component {i} failed: {error_message}"
```

Add to `TestOSCALCompliance` class and update the test docstring with test number.

### Debugging a Failed Test
```bash
# Run with full traceback
pytest verify_oscal_compliance.py::TestOSCALCompliance::test_nist_controls_exist_in_catalog -vv -s

# This will show:
# - Full error message with assertion details
# - Which component/property failed
# - Exact value that failed validation
```

### Extending CSV Export Format
1. Add new column to CSV in `oscal_to_jama_csv()`:
   ```python
   row = {
       # existing columns...
       'New-Column': component.get('new_field', ''),
   }
   ```
2. Update `validate_csv_format()` if column is required:
   ```python
   required_columns = ['JAMA-Requirement-ID', ..., 'New-Column']
   ```
3. Add test to `verify_oscal_compliance.py`:
   ```python
   def test_csv_export_has_new_column(self, oscal_data, oscal_file):
       """Test XX: CSV includes new column."""
       rows = oscal_to_jama_csv(oscal_file)
       assert 'New-Column' in rows[0], "CSV missing New-Column"
   ```

---

## Key Concepts & Constraints

### OSCAL v1.0.0 Requirements
- Root element MUST be `component-definition`
- Each component requires: uuid, title, description, properties
- Properties use name-value pairs for semantic meaning
- control-implementations maps to NIST controls with responsibility levels
- Timestamps use ISO-8601 format (YYYY-MM-DDTHH:MM:SSZ)

### NERC-CIP Format Requirements
- Standard code: CIP-005, CIP-007, etc. (3-digit + letter option)
- Requirement: R1, R2, R3 (letter "R" + number)
- Subrequirement: a, b, c, d (lowercase letter)
- Full ID example: CIP-005-6 R1 (includes version digit "-6")
- JAMA placeholder: CIP-005-R1-a (no version digit, includes subrequirement letter)

### NIST Control Validation
- Family code: 2 uppercase letters (AC, SC, SR, etc.)
- Control number: 1-2 digits
- Enhancement: optional (n) notation for enhancements
- Must exist in NIST SP 800-53 R5 catalog (~900 controls)

### JAMA Integration Points
- JAMA-Requirement-ID is the primary linking field
- Format must be parseable by JAMA's CSV import
- Each subrequirement should have its own JAMA-ID
- CSV columns must match JAMA's expected schema

---

## Testing Strategy

### Test Coverage by Category
1. **Structural Validation** (Tests 1-5): Ensures JSON is well-formed and has required top-level structure
2. **NIST Mapping** (Tests 6-8): Validates control existence and format against NIST R5 catalog
3. **JAMA Readiness** (Tests 9-11, 22): Ensures all fields needed for JAMA import are present and correctly formatted
4. **NERC Traceability** (Tests 12-13): Validates requirement IDs link back to original standards
5. **Quality Metrics** (Tests 19-21): Checks descriptions are specific (not vague), minimum metadata present
6. **CSV Export** (Tests 25-27): Validates that OSCAL can be exported to JAMA-compatible CSV
7. **Integration** (Test 22): Overall "JAMA-ready" assessment

### Validation Counter Pattern (v1.1.4+)
All conditional assertion tests now use validation counters to prevent silent pass bugs:

```python
# Pattern: Counter-based validation
validation_count = 0
for item in items:
    if condition_matches:
        assert validation_check(item)
        validation_count += 1

# Guarantee minimum validations occurred
assert validation_count > 0, "No items validated - check test data!"
```

This ensures tests fail if:
- Conditional blocks never execute
- Data is missing required fields
- Loops iterate over empty collections

**Result:** Tests accurately reflect data quality instead of passing silently.

**Running Specific Test Categories:**
```bash
# NIST mapping tests only
pytest verify_oscal_compliance.py -k "nist" -v

# JAMA-related tests
pytest verify_oscal_compliance.py -k "jama" -v

# CSV export tests
pytest verify_oscal_compliance.py -k "csv" -v
```

---

## Performance Notes

- Validation suite: ~0.9 seconds for 27 tests
- NIST control lookup: O(1) dictionary access (cached in NIST_SP_800_53_R5_CONTROLS)
- CSV export: O(n) where n = number of components (typically < 50)
- No external API calls; all validation is local
- NIST R5 catalog loaded on import (~40 KB in memory)

---

## Troubleshooting Guide

### "Component X missing NIST 800-53 mapping"
**Cause:** Component has no properties with "NIST" in the name, or no control-implementations.

**Fix:**
```json
{
  "properties": [
    {"name": "NIST-800-53-Primary-Control", "value": "SC-7"},
    {"name": "NIST-800-53-Secondary-Controls", "value": "CA-3, PL-2"}
  ]
}
```

### "Component X maps to non-existent NIST control: 'XX-99'"
**Cause:** Control ID doesn't exist in NIST SP 800-53 R5.

**Fix:** Verify the control ID is correct:
```python
from nist_controls import validate_nist_control
print(validate_nist_control("SC-7"))  # True
print(validate_nist_control("XX-99")) # False
```

### "JAMA-Requirement-ID values follow invalid format"
**Cause:** Format doesn't match `CIP-\d{3}-R\d+(-[a-z])?`

**Examples:**
- ❌ `CIP005R1` (missing hyphens)
- ❌ `JAMA-001` (wrong prefix)
- ✅ `CIP-005-R1-a` (correct)
- ✅ `CIP-007-R2-b` (correct)

### "pytest: command not found"
**Fix:**
```bash
pip install pytest
# or
python -m pytest verify_oscal_compliance.py -v
```

---

## Future Enhancement Areas

1. **NIST SP 800-53 R6** - Update NIST_SP_800_53_R5_CONTROLS when NIST R6 is released
2. **Additional NERC Standards** - Support CIP-014, CIP-015 (newer standards)
3. **Schema Validation** - Add JSONSchema validation against official OSCAL schema
4. **SCAP/XCCDF Integration** - Export to SCAP format for additional compliance tools
5. **Markdown Report Generation** - Generate human-readable compliance reports from OSCAL JSON
6. **API Endpoint** - Expose validation as REST API for integration with other tools

---

## References & Documentation

- **OSCAL v1.0.0 Specification:** https://pages.nist.gov/OSCAL/
- **NIST SP 800-53 R5:** https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
- **NERC Standards:** https://www.nerc.net/pa/Stand/Pages/default.aspx
- **JAMA Documentation:** See JAMA vendor documentation for CSV import schema

---

## Recent Implementation Notes

**Tier 1 Enhancements (Latest Release):**
- Added NIST control catalog validation (nist_controls.py)
- Expanded test suite from 22 to 27 tests
- Implemented JAMA CSV export with validation
- Enhanced error messages to guide users on fixing issues
- Added detailed format option for CSV export
