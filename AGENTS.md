# NERC-CIP to OSCAL Toolkit - AI Agent Guide

## Project Overview

This toolkit transforms unstructured NERC-CIP regulatory text into structured OSCAL v1.0.0 Catalogs with automatic mapping to NIST SP 800-53 controls. The project enables compliance teams to convert regulatory requirements into machine-readable JSON that can be imported into JAMA for requirements management and traced through cloud infrastructure tests.

**Core Problem Solved:** Manual conversion of NERC-CIP regulatory text to compliance frameworks requires significant effort, semantic mapping, and careful traceability. This toolkit automates the process using AI-powered conversion with comprehensive validation.

## Technology Stack

- **Language:** Python 3.8+
- **Testing Framework:** pytest (27 comprehensive tests)
- **Dependencies:** jsonschema, pandas, pytest-cov
- **AI Integration:** Claude Code for regulatory text conversion
- **Standards:** OSCAL v1.0.0, NIST SP 800-53 R5, NERC-CIP Standards
- **Output Formats:** JSON (OSCAL), CSV (JAMA import)

## Architecture & Components

### Core Modules

1. **nist_controls.py** (64KB)
   - Complete NIST SP 800-53 R5 control catalog (500+ controls)
   - Validation functions for control existence and format checking
   - Control description lookup and family extraction

2. **verify_oscal_compliance.py** (26KB)
   - 27 comprehensive validation tests
   - Structural validation (JSON syntax, OSCAL schema)
   - NIST mapping validation (format, existence, descriptions)
   - JAMA placeholder validation (format, completeness)
   - CSV export validation

3. **oscal_to_jama_csv.py** (9KB)
   - Command-line CSV export utility
   - JAMA-compatible format with 7 standard columns
   - Validation and error reporting
   - Support for standard and detailed export modes

### AI Integration

4. **TRAVIS-NERC-PROMPT.md** (10KB)
   - Comprehensive Claude Code prompt for regulatory text conversion
   - Semantic mapping logic (NERC → NIST → OSCAL)
   - Step-by-step processing instructions
   - Output format specifications

### Sample Data

5. **nerc-oscal.json** (7.5KB)
   - Example OSCAL Component Definition for CIP-005
   - Demonstrates proper structure and property formatting
   - Includes 3 sample components with complete mappings

## Development Workflow

### Standard Conversion Process

1. **Prepare Input:** Extract NERC-CIP regulatory text from official documentation
2. **AI Conversion:** Use Claude Code with TRAVIS-NERC-PROMPT.md to generate OSCAL JSON
3. **Save Output:** Store generated JSON as `nerc-oscal.json`
4. **Validate:** Run `pytest verify_oscal_compliance.py -v` (27 tests)
5. **Export CSV:** Run `python oscal_to_jama_csv.py nerc-oscal.json --validate`
6. **Import to JAMA:** Use generated CSV with JAMA's import feature

### Testing Strategy

```bash
# Run all validation tests
pytest verify_oscal_compliance.py -v

# Run specific test categories
pytest verify_oscal_compliance.py -k "nist_controls" -v
pytest verify_oscal_compliance.py -k "csv_export" -v
pytest verify_oscal_compliance.py -k "jama" -v

# Test CSV export functionality
python oscal_to_jama_csv.py nerc-oscal.json --validate
```

### Test Categories (27 Tests)

- **Structural Validation (5):** JSON syntax, OSCAL schema, metadata
- **NIST Mapping (6):** Control format, existence, descriptions
- **JAMA Placeholders (3):** Format compliance, completeness
- **NERC Requirements (2):** Property existence, format
- **OSCAL Structure (4):** UUIDs, titles, descriptions, implementations
- **Quality Validation (3):** Vague language, property counts, JAMA readiness
- **CSV Export (3):** Format, columns, data integrity
- **Integration (1):** Overall JAMA readiness

## Code Organization

### File Structure
```
nerc-cip-oscal-jama/
├── nist_controls.py              # NIST control catalog
├── verify_oscal_compliance.py    # Validation test suite
├── oscal_to_jama_csv.py         # CSV export utility
├── TRAVIS-NERC-PROMPT.md        # AI conversion prompt
├── nerc-oscal.json              # Sample OSCAL output
├── nerc-oscal.csv               # Generated CSV export
├── requirements.txt             # Python dependencies
├── README.md                    # User documentation
├── QUICK-START.md               # Quick reference
├── IMPLEMENTATION-SUMMARY.md    # Implementation details
└── .gitignore                   # Git exclusions
```

### Key Dependencies
- **pytest>=8.0.0** - Testing framework
- **jsonschema>=4.20.0** - JSON validation
- **pandas>=2.0.0** - Data processing
- **pytest-cov>=4.1.0** - Coverage reporting

## Development Conventions

### Code Style
- Python naming conventions (snake_case for functions, PascalCase for classes)
- Comprehensive docstrings for all functions
- Type hints for better code clarity
- Error handling with actionable messages

### Testing Standards
- All tests must pass before committing changes
- New features require corresponding tests
- Tests should be atomic and independent
- Error messages must be actionable and specific

### Validation Requirements
- JSON must be valid and parseable
- All NIST controls must exist in official catalog
- JAMA placeholders must follow format: `CIP-###-R#-[a-z]`
- NERC requirement IDs must follow format: `CIP-###-# R#`
- Minimum one NIST control per component
- All components must have UUIDs, titles, and descriptions

## Security Considerations

### Input Validation
- All JSON inputs are validated before processing
- NIST control IDs are validated against official catalog
- File paths are checked for existence and accessibility
- CSV outputs are sanitized for proper encoding

### Data Integrity
- UUID generation ensures unique component identifiers
- Property validation prevents incomplete mappings
- CSV validation ensures JAMA import compatibility
- Error reporting prevents silent failures

## Build and Deployment

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
pytest --version
python -c "import nist_controls; print('OK')"
```

### Validation
```bash
# Run complete test suite
pytest verify_oscal_compliance.py -v

# Expected: 27 passed in ~0.9 seconds

# Test CSV export
python oscal_to_jama_csv.py nerc-oscal.json --validate
```

### Performance Metrics
- **Test Execution:** 0.86 seconds (27 tests)
- **CSV Export:** <1 second (3 components)
- **Control Validation:** Instant (hash lookup)
- **Memory Usage:** ~100 MB for catalog + components

## Common Development Tasks

### Adding New NIST Controls
Edit `nist_controls.py` and add to `NIST_SP_800_53_R5_CONTROLS` dictionary:
```python
"NEW-CONTROL": "Control Description"
```

### Modifying Validation Logic
Update `verify_oscal_compliance.py` - add new test methods to `TestOSCALCompliance` class.

### Updating CSV Export Format
Modify `oscal_to_jama_csv.py` - adjust `JAMA_CSV_COLUMNS` and export logic.

### Enhancing AI Prompt
Edit `TRAVIS-NERC-PROMPT.md` - update mapping logic and output specifications.

## Troubleshooting Guide

### Common Issues

**Test Failures:**
- Check error messages for specific test failures
- Verify nerc-oscal.json exists in working directory
- Ensure all required properties are present

**CSV Export Issues:**
- Verify nerc-oscal.json has valid components array
- Check for empty requirement IDs
- Ensure proper CSV encoding (UTF-8)

**NIST Control Validation:**
- Use correct format: "SC-7" (not "SC7" or "Security Control 7")
- Verify control exists in catalog: `python -c "from nist_controls import validate_nist_control; print(validate_nist_control('SC-7'))"`

### Debug Commands
```bash
# Check NIST control existence
python -c "from nist_controls import get_all_controls; print(len(get_all_controls()))"

# Validate JSON syntax
python -c "import json; json.load(open('nerc-oscal.json'))"

# Test CSV export manually
python oscal_to_jama_csv.py nerc-oscal.json --format detailed
```

## Integration Points

### JAMA Software
- CSV import with configurable field mapping
- Requirement traceability through JAMA-Requirement-ID
- Custom attributes for NERC and NIST mappings

### Cloud Infrastructure
- Links JAMA requirement IDs to infrastructure tests
- Enables compliance evidence collection
- Supports audit trail documentation

### Compliance Tools
- OSCAL JSON import/export
- NIST control mapping validation
- Regulatory requirement traceability

## Future Enhancements

### Tier 2 (Medium Priority)
- OSCAL schema validation against official NIST JSON schema
- Expanded NERC-NIST mapping database with recommendations
- Batch processing for multiple NERC standards
- Traceability matrix CSV generation

### Tier 3 (Lower Priority)
- PDF extraction from NERC documents
- Web UI for non-technical users
- GitHub Actions CI/CD pipeline
- JAMA API direct integration

---

**Last Updated:** 2026-01-21  
**Version:** 1.0.0  
**Status:** Production Ready (27/27 tests passing)