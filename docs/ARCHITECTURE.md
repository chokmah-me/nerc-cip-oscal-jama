# Technical Architecture

Complete technical overview of the NERC-CIP to OSCAL Toolkit.

## System Overview

```
NERC-CIP PDFs (30 documents)
    ↓
[nerc_pdf_parser.py] → Extract text from PDFs
    ↓
nerc_raw_text/ (30 text files)
    ↓
[extract_nerc_text.py] → Parse requirements using state machine
    ↓
nerc_all_combined.txt (consolidated requirements text)
    ↓
[generate_oscal.py] → Generate OSCAL JSON with deduplication
    ↓
nerc-oscal.json (49 NERC-CIP requirements in OSCAL format)
    ↓
[verify_oscal_compliance.py] → Validate with 27 tests
    ↓
[oscal_to_jama_csv.py] → Export to GRC systems
    ↓
nerc-oscal.csv (JAMA-compatible traceability matrix)
```

---

## Core Components

### 1. PDF Extraction (`nerc_pdf_parser.py`)

**Purpose:** Extract text from NERC-CIP PDF documents

**Features:**
- Handles multiple PDF versions
- Removes pagination markers ("Page X of Y")
- Cleans OCR artifacts
- Preserves semantic structure

**Input:** NERC-CIP/*.pdf (30 documents)

**Output:** nerc_raw_text/ (30 .txt files)

### 2. Text Extraction (`extract_nerc_text.py`)

**Purpose:** Parse regulatory text to identify requirements

**State Machine Logic:**
1. Split documents by CIP sections (CIP-002, CIP-003, etc.)
2. Identify requirement blocks (CIP-###-# section)
3. Extract individual requirements (R1, R2, R3, etc.)
4. Stop at measures section (M1, M2, etc.)
5. Clean and normalize extracted text

**Input:** nerc_raw_text/ (30 text files)

**Output:**
- nerc_all_combined.txt (consolidated)
- Individual requirement objects

### 3. OSCAL Generation (`generate_oscal.py`)

**Purpose:** Convert parsed requirements to OSCAL v1.0.0 format

**Process:**
1. Parse requirements from combined text
2. Extract CIP family, version, title, purpose
3. Organize by requirement section
4. Smart deduplication (keep latest versions only)
5. Generate OSCAL catalog structure with unique UUIDs
6. Add properties and metadata

**Features:**
- Generates unique UUIDs for all entities
- ISO-8601 formatted timestamps
- Automatic version prioritization
- Clean property structure

**Input:** nerc_all_combined.txt

**Output:** nerc-oscal.json (OSCAL v1.0.0 catalog)

```json
{
  "catalog": {
    "uuid": "unique-id",
    "metadata": {
      "title": "NERC CIP OSCAL Catalog",
      "version": "1.1.0",
      "oscal-version": "1.0.0"
    },
    "groups": [
      {
        "id": "cip-002-8",
        "title": "CIP-002-8 - Cyber Security",
        "controls": [
          {
            "id": "cip-002-8-r1",
            "class": "requirement",
            "title": "CIP-002-8 R1",
            "parts": [{"prose": "Requirement text..."}],
            "props": [{"name": "label", "value": "R1"}]
          }
        ]
      }
    ]
  }
}
```

### 4. Validation Suite (`verify_oscal_compliance.py`)

**Purpose:** Validate OSCAL compliance and data quality

**27 Tests Organized By:**

| Category | Tests | Purpose |
|----------|-------|---------|
| Basic Validation | 5 | JSON syntax, root structure, metadata |
| NIST Mapping | 3 | Control validation against NIST R5 |
| JAMA Integration | 3 | Placeholder format and presence |
| NERC Requirements | 2 | Requirement ID format and structure |
| OSCAL Structure | 5 | UUID, title, description, properties |
| Control Implementation | 2 | Control mapping and implementation |
| Quality & Export | 7 | Vague language, CSV export, field validation |

**Key Test Patterns:**
```python
# Format validation using regex
jama_pattern = re.compile(r'^CIP-\d{3}-R\d+(-[a-z])?$')
nist_pattern = re.compile(r'^[A-Z]{2}-\d{1,2}(\s*\([0-9]+\))?$')

# NIST catalog validation
validate_nist_control(control_id)  # Checks against 900+ controls

# CSV export testing
rows = oscal_to_jama_csv(oscal_file)
assert len(rows) > 0
```

### 5. GRC Export (`oscal_to_jama_csv.py`)

**Purpose:** Export OSCAL to GRC system formats

**Features:**
- Supports both catalog and component-definition schemas
- Extracts component properties intelligently
- Generates JAMA-compatible CSV
- Optional detailed format with extra columns

**CSV Format (Standard):**
- JAMA-Requirement-ID
- NERC-Requirement-ID
- NIST-Primary-Control
- NIST-Secondary-Controls
- Title
- Description
- Implementation-Status

**CSV Format (Detailed):**
- All standard columns plus:
- Component-UUID
- Component-Type
- Control-Count

### 6. NIST Control Catalog (`nist_controls.py`)

**Purpose:** Validate NIST SP 800-53 R5 control references

**Provides:**
- `validate_nist_control(control_id)` - Check if control exists
- `get_control_description(control_id)` - Retrieve control info
- `get_control_family(control_id)` - Extract family code
- NIST_SP_800_53_R5_CONTROLS dictionary (~900 controls)

**Control Format:**
- Base: XX-# (SC-7, AC-2)
- Enhancement: XX-#(n) (SC-7(1))

---

## Data Flow

### Phase 1: Extraction
```
PDFs → PDF Parser → Raw Text Files
```

### Phase 2: Parsing
```
Raw Text → Text Parser → State Machine → Parsed Requirements
```

### Phase 3: Generation
```
Parsed Requirements → OSCAL Generator → OSCAL JSON
```

### Phase 4: Validation
```
OSCAL JSON → Test Suite (27 tests) → Verification Report
```

### Phase 5: Export
```
OSCAL JSON → CSV Exporter → JAMA CSV → GRC Systems
```

---

## Schema Design

### OSCAL Catalog Format

**Why Catalog?**
- Directly represents regulatory requirements
- Authoritative source of control definitions
- Can be exported to component implementations

**Structure:**
```
Catalog
├── Metadata (title, version, timestamps)
├── Groups (organized by standard: CIP-002, CIP-003, etc.)
│   └── Controls (individual requirements R1, R2, etc.)
│       ├── Class (purpose, requirement)
│       ├── Title (display name)
│       ├── Parts (prose content)
│       └── Props (structured properties)
```

### Dual-Schema Support

Both schemas now supported:

**Catalog (Current Implementation):**
```json
{"catalog": {"groups": [{"controls": [...]}]}}
```

**Component-Definition (Alternative):**
```json
{"component-definition": {"components": [...]}}
```

Schema abstraction layer handles both:
- `get_components_from_oscal()` - Test suite
- `_extract_components_from_oscal()` - CSV export

---

## Requirements Coverage

### Standards Mapping

| CIP | Version | Reqs | Purpose |
|-----|---------|------|---------|
| CIP-002 | -8 | 2 | BES Cyber System Categorization |
| CIP-003 | -11 | 4 | Security Management Controls |
| CIP-004 | -8 | 6 | Personnel and Training |
| CIP-005 | -8 | 3 | Electronic Security Perimeter |
| CIP-006 | -7 | 3 | Physical Security |
| CIP-007 | -7 | 5 | System Security Administration |
| CIP-008 | -7 | 4 | Incident Reporting & Response |
| CIP-009 | -7 | 3 | Recovery Plans |
| CIP-010 | -5 | 4 | Configuration & Vulnerability Mgmt |
| CIP-011 | -4 | 2 | Information Protection |
| CIP-012 | -2 | 1 | Supply Chain Risk Mgmt |
| CIP-013 | -3 | 3 | Physical Security of Gen Facilities |
| CIP-014 | -3 | 6 | System Protection from Seismic |
| CIP-015 | -1 | 3 | Internal Network Security Monitoring |

### Version Prioritization

Smart deduplication keeps only latest versions:
- Multiple PDFs for each CIP (CIP-003-8, CIP-003-9, CIP-003-11)
- Algorithm: Keep highest version number
- Example: CIP-003-11 preferred over CIP-003-8

---

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Test Suite | 0.60s | 27 tests, parallel execution |
| NIST Lookup | O(1) | Dictionary-based, cached |
| CSV Export | O(n) | Linear in component count (49) |
| OSCAL Generation | ~5s | Includes deduplication |
| PDF Parsing | ~10s | Depends on PDF size |

---

## Error Handling

### Validation Layer
- JSON syntax validation
- Schema structure checks
- Control existence verification
- Format validation (regex patterns)
- NIST catalog lookups
- Empty field detection

### Error Messages
Clear, actionable error messages:
```
Component 0 maps to non-existent NIST control: 'ZZ-99'.
Verify control ID exists in NIST SP 800-53 R5 catalog.
Valid format: Family-Number (e.g., 'SC-7', 'AC-2', 'CA-3')
```

---

## Integration Points

### JAMA Integration
- CSV export for JAMA import
- Requirement ID format: CIP-005-R1-a
- Traceability matrix with 49 rows

### ServiceNow Integration
- Direct OSCAL JSON import
- CSV format support
- Metadata mapping available

### Tableau/Splunk Integration
- CSV export with standard columns
- Detailed format option
- Metadata available

### Custom Integration
- OSCAL v1.0.0 standard format
- Well-documented structure
- Easy to parse and transform

---

## Quality Assurance

### Test Coverage
- 27 comprehensive tests
- 100% success rate
- Execution time: 0.60 seconds

### Data Quality
- ✅ No OCR artifacts
- ✅ No pagination markers
- ✅ No violation tables
- ✅ Clean regulatory prose
- ✅ Unique UUIDs
- ✅ ISO-8601 timestamps

### Production Verification
- ✅ Schema compliance
- ✅ Control mapping validation
- ✅ JAMA format compatibility
- ✅ Zero known issues

---

## Development Workflows

### Adding a New NIST Control
```python
# Edit nist_controls.py
NIST_SP_800_53_R5_CONTROLS = {
    ...
    "AA-1": "New Control Family - Control Name",
    ...
}
```

### Creating a New Validation Test
```python
def test_my_new_requirement(self, oscal_data):
    """Test N: My new validation requirement."""
    components = self.get_components_from_oscal(oscal_data)

    for i, component in enumerate(components):
        assert some_condition, f"Component {i} failed: {error_message}"
```

### Extending CSV Export Format
```python
# In oscal_to_jama_csv()
row = {
    # existing columns...
    'New-Column': component.get('new_field', ''),
}
```

---

## References

- **OSCAL Spec:** https://pages.nist.gov/OSCAL/
- **NIST SP 800-53 R5:** https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
- **NERC Standards:** https://www.nerc.net/pa/Stand/Pages/default.aspx

---

**Architecture Version:** 1.1.1 | **Last Updated:** January 25, 2026
