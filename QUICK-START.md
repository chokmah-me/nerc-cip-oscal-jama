# NERC-CIP OSCAL Toolkit - Quick Start Guide

## What's New (Tier 1 Enhancements)

This toolkit now includes enhanced validation and JAMA export capabilities:

### 3 New Features
1. **NIST Control Validation** - Verify controls exist in official catalog
2. **JAMA CSV Export** - Generate traceability matrices for JAMA import
3. **Expanded Tests** - 27 comprehensive validation tests (was 22)

---

## Complete Workflow (6 Steps)

### Step 1: Prepare Input
Extract NERC-CIP requirement text from official documentation

### Step 2: Generate OSCAL JSON
Use Claude Code with `TRAVIS-NERC-PROMPT.md` to convert text to OSCAL JSON

### Step 3: Save Output
Save the generated JSON as `nerc-oscal.json` in this directory

### Step 4: Run Validation Tests
```bash
pytest verify_oscal_compliance.py -v
```
Expected: 27 tests pass in ~0.9 seconds

### Step 5: Export to JAMA CSV
```bash
python oscal_to_jama_csv.py nerc-oscal.json --validate
```
Creates: `nerc-oscal.csv` with full traceability matrix

### Step 6: Import into JAMA
Use JAMA's CSV import feature with the generated CSV file

---

## File Reference

| File | Purpose | Size |
|------|---------|------|
| `nist_controls.py` | NIST SP 800-53 R5 control catalog (500+ controls) | 63 KB |
| `oscal_to_jama_csv.py` | CSV export utility with validation | 8.6 KB |
| `verify_oscal_compliance.py` | 27 comprehensive validation tests | 20 KB |
| `requirements.txt` | Python dependencies | 381 B |
| `README.md` | Full documentation | 15 KB |
| `IMPLEMENTATION-SUMMARY.md` | What was implemented | 11 KB |

---

## Common Commands

### Validate OSCAL JSON
```bash
# Run all tests
pytest verify_oscal_compliance.py -v

# Run specific test
pytest verify_oscal_compliance.py::TestOSCALCompliance::test_nist_controls_exist_in_catalog -v

# Run only NIST validation tests
pytest verify_oscal_compliance.py -k "nist_controls" -v

# Run only CSV export tests
pytest verify_oscal_compliance.py -k "csv_export" -v
```

### Export to JAMA
```bash
# Basic export with validation
python oscal_to_jama_csv.py nerc-oscal.json --validate

# Export to custom filename
python oscal_to_jama_csv.py nerc-oscal.json -o my-matrix.csv

# Detailed format (includes metadata)
python oscal_to_jama_csv.py nerc-oscal.json --format detailed

# Export without validation
python oscal_to_jama_csv.py nerc-oscal.json
```

### Check NIST Controls
```bash
# Verify a control exists
python -c "from nist_controls import validate_nist_control; print(validate_nist_control('SC-7'))"

# Get control description
python -c "from nist_controls import get_control_description; print(get_control_description('SC-7'))"

# List all valid controls
python -c "from nist_controls import get_all_controls; print(len(get_all_controls()), 'controls')"
```

---

## Test Results

### Test Coverage

**Structural Validation (5 tests)**
- JSON syntax
- Root elements
- Metadata presence

**NIST Mapping (6 tests)**
- Format validation
- Control existence (NEW)
- Control descriptions (NEW)
- Minimum controls per component

**JAMA Placeholders (3 tests)**
- Property existence
- Format compliance
- Non-empty values

**NERC Requirements (2 tests)**
- Property existence
- Format compliance

**OSCAL Structure (4 tests)**
- UUIDs
- Titles
- Descriptions
- Control implementations

**Quality Validation (3 tests)**
- Vague language detection
- Property counts
- JAMA readiness

**CSV Export (3 tests) - NEW**
- Export format validity
- Required columns
- No empty IDs

---

## Troubleshooting

### Test Failures

**Test: `test_nist_controls_exist_in_catalog` fails**
- Error: "Component 0 maps to non-existent NIST control: 'ZZ-99'"
- Fix: Verify NIST control ID exists in SP 800-53 R5 catalog
- Use: `python -c "from nist_controls import get_all_controls; print([c for c in get_all_controls() if 'SC' in c])"`

**Test: `test_csv_export_required_columns` fails**
- Error: "CSV missing required columns: {'JAMA-Requirement-ID'}"
- Fix: Ensure OSCAL components have JAMA-Requirement-ID property
- Check: Review nerc-oscal.csv to verify all columns present

**Test: `test_csv_export_no_empty_ids` fails**
- Error: "Row 0: Empty JAMA-Requirement-ID"
- Fix: Ensure all components have non-empty requirement IDs
- Check: Open nerc-oscal.csv and verify no empty cells in ID columns

### CSV Export Issues

**Error: Character encoding issue**
- Solution: Script automatically uses UTF-8 encoding
- If issue persists: Check CSV in Excel with UTF-8 import settings

**Error: File not found**
- Verify: nerc-oscal.json exists in current directory
- Command: `ls -la nerc-oscal.json` (or `dir nerc-oscal.json` on Windows)

**CSV file is empty**
- Check: nerc-oscal.json has valid components array
- Run: `python -c "import json; f=open('nerc-oscal.json'); d=json.load(f); print(len(d['component-definition']['components']), 'components')"`

---

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
pytest --version
python nist_controls.py  # Should not error
```

### Verify
```bash
# Run validation tests
pytest verify_oscal_compliance.py -v

# Expected: 27 passed in ~0.9s
```

---

## Integration with JAMA

### JAMA CSV Import Steps
1. Open JAMA Requirements Management System
2. Create new Project → Create new Requirement Set
3. Click "Import" button
4. Select `nerc-oscal.csv` file
5. Map CSV columns:
   - CSV "JAMA-Requirement-ID" → JAMA "ID" field
   - CSV "Title" → JAMA "Title" field
   - CSV "Description" → JAMA "Description" field
   - CSV "NERC-Requirement-ID" → Custom attribute
   - CSV "NIST-Primary-Control" → Custom attribute
6. Complete import
7. Verify requirement count matches CSV row count

### JAMA CSV Columns Generated

| Column | Example | Purpose |
|--------|---------|---------|
| JAMA-Requirement-ID | CIP-005-R1-a | Requirement ID for JAMA |
| NERC-Requirement-ID | CIP-005-6 R1 | Source NERC standard reference |
| NIST-Primary-Control | SC-7 | Primary NIST 800-53 control |
| NIST-Secondary-Controls | CA-3, PL-2 | Related controls |
| Title | NERC CIP-005 Systems Security Management | Component title |
| Description | Implements documented cyber security... | Full description |
| Implementation-Status | Draft | Current status |

---

## Performance

- **Test Execution:** 0.88 seconds (27 tests)
- **CSV Export:** <1 second (3 components)
- **Control Validation:** Instant (hash lookup)
- **Memory Usage:** ~100 MB for catalog + components

---

## Support

### Key Files for Reference
- `TRAVIS-NERC-PROMPT.md` - Claude Code conversion prompt
- `verify_oscal_compliance.py` - All validation logic
- `nist_controls.py` - Control catalog details
- `README.md` - Comprehensive documentation
- `IMPLEMENTATION-SUMMARY.md` - What was implemented

### Next Steps
- See `README.md` for detailed documentation
- See `IMPLEMENTATION-SUMMARY.md` for what was implemented
- See `TRAVIS-NERC-PROMPT.md` for conversion prompt details
