# NERC-CIP to OSCAL Component Definition Toolkit
## Convert Regulatory Text to Structured Compliance JSON

This toolkit transforms unstructured NERC-CIP regulatory text into structured OSCAL v1.1.2 Component Definitions with automatic mapping to NIST SP 800-53 controls.

---

## Release Notes

### v1.1.0 (January 25, 2026) 🚀

**Production-Grade OSCAL Dataset Released**

This release delivers a complete, validated OSCAL v1.1.0 compliance dataset covering **49 active NERC-CIP Requirements** across **14 standards** (CIP-002 through CIP-015).

**Major Features:**
- **PDF Extraction Toolchain**: Automated parsing of 30 NERC-CIP regulatory documents with OCR cleanup
  - `nerc_pdf_parser.py` - PDF text extraction with pagination filtering
  - `extract_nerc_text.py` - State machine-based requirement parsing
  - `nerc_raw_text/` - Complete extracted text corpus for all standards

- **OSCAL Generation**: Production script for converting parsed NERC text to OSCAL v1.1.0 JSON
  - `generate_oscal.py` - Reproducible OSCAL generation with deduplication
  - Auto-prioritizes latest standard versions (e.g., CIP-003-11 over CIP-003-9)

- **Complete Standards Library**: 30 PDF documents across CIP-002 through CIP-015
  - `NERC-CIP/` directory - Full NERC standards library with multiple versions

- **Parser Test Suite**: Validation and unit tests
  - `test_nerc_parser.py` - Comprehensive test coverage for extraction and parsing

**Quality Assurance:**
- ✅ **Schema Compliance**: Valid OSCAL v1.1.0 with unique UUIDs and ISO-8601 timestamps
- ✅ **Data Hygiene**: Zero OCR artifacts, pagination markers, or violation tables detected
- ✅ **Logic Integrity**: Smart deduplication verified; only latest versions included
- ✅ **Scope Coverage**: Delivered CIP-002 through CIP-015 (exceeded original CIP-014 scope)

**Breakdown by Standard:**
- CIP-002 (-8): 2 requirements | CIP-003 (-11): 4 | CIP-004 (-8): 6 | CIP-005 (-8): 3
- CIP-006 (-7): 3 | CIP-007 (-7): 5 | CIP-008 (-7): 4 | CIP-009 (-7): 3
- CIP-010 (-5): 4 | CIP-011 (-4): 2 | CIP-012 (-2): 1 | CIP-013 (-3): 3
- CIP-014 (-3): 6 | CIP-015 (-1): 3
- **Total: 49 requirements across 14 standards**

**Changes:**
- Updated `nerc-oscal.json` with latest standard mappings and complete data
- Removed deprecated `nerc-oscal.csv` (use `oscal_to_jama_csv.py` to regenerate)

**Commit:** `3549905` | **Tag:** `v1.1.0` | **Files:** 65 changed, 44,718 insertions

**Ready for:** JAMA import, GRC tool ingestion, compliance audit evidence

See [CLAUDE.md](CLAUDE.md) for technical architecture and development details.

---

## Overview

**Problem:** NERC-CIP standards are written as regulatory text. Converting them to compliance frameworks requires manual effort, semantic mapping, and careful traceability.

**Solution:** This toolkit uses Claude Code to:
1. Parse NERC regulatory text (CIP-005, CIP-007, etc.)
2. Map requirements to NIST SP 800-53 controls
3. Generate structured OSCAL JSON
4. Include JAMA placeholders for requirement traceability
5. Validate output automatically

**Result:** Machine-readable JSON that can be:
- Imported into JAMA for requirements management
- Used as compliance evidence in audits
- Traced through cloud infrastructure tests
- Exported as CSV traceability matrices

---

## Prerequisites

Before using this toolkit, ensure you have:

- **Python 3.8+** installed
- **pytest** package: `pip install pytest`
- **Claude Code** access (free or paid)
- **NERC-CIP regulatory text** to convert (from official NERC documentation)
- **Text editor or IDE** (VS Code, Sublime, etc.)

### Optional Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pytest

# Verify pytest works
pytest --version
```

---

## For Developers & Contributors

**New to the codebase?** Start with **CLAUDE.md** for a comprehensive overview:
- Architecture & three-layer compliance mapping (NERC → OSCAL → JAMA)
- Core components explanation (nist_controls.py, verify_oscal_compliance.py, oscal_to_jama_csv.py)
- Format specifications for NIST controls, NERC requirements, and JAMA placeholders
- Common development tasks (adding controls, writing tests, debugging)
- Troubleshooting guide with real error examples

**Quick reference for common development commands:**
```bash
# Run all 27 validation tests
pytest verify_oscal_compliance.py -v

# Run specific test
pytest verify_oscal_compliance.py::TestOSCALCompliance::test_nist_controls_exist_in_catalog -v

# Export to JAMA CSV
python oscal_to_jama_csv.py nerc-oscal.json --validate
```

See **CLAUDE.md** for detailed explanations of the architecture, command reference, and development workflows.

---

## Quick Start Workflow

Follow these 5 steps to convert NERC-CIP text to OSCAL JSON:

### Step 1: Prepare NERC-CIP Input Text (5 minutes)

**What you need:** Regulatory text from a NERC-CIP standard (CIP-005, CIP-007, etc.)

**Where to get it:**
- NERC official docs: https://www.nerc.com/standards
- Look for "CIP-00X-Y Requirements"
- Copy the full requirement text (including subrequirements a, b, c, etc.)

**Example input (CIP-005 R1):**
```
CIP-005-6 Requirement 1: Systems Security Management
The Responsible Entity shall implement one or more documented,
recoverable, and type-certified processes for generating, storing,
protecting, and managing the Cyber Security Plan that includes:
  a) The roles and responsibilities for developing, approving,
     implementing, and maintaining the plan
  b) The methodology for assessing the effectiveness of the Cyber
     Security Plan
  c) A schedule for reviewing and updating the plan
  d) The means to ensure that the Cyber Security Plan and
     implementation are recoverable
```

**Action:** Copy this text and save it somewhere accessible (you'll paste it into Claude Code next).

### Step 2: Use TRAVIS-NERC-PROMPT.md with Claude Code (10-15 minutes)

**What to do:**

1. Open Claude Code in VS Code or at claude.ai/code
2. Open the `TRAVIS-NERC-PROMPT.md` file from this directory
3. Copy the entire **PROMPT** section (starting at "Generate a complete OSCAL Component Definition...")
4. Paste into Claude Code's input field
5. Add your NERC-CIP regulatory text after the prompt
6. Wait for Claude to generate the OSCAL JSON response

**Expected output:** A complete OSCAL JSON Component Definition with:
- ✅ Valid JSON syntax
- ✅ NERC-Requirement-ID properties
- ✅ NIST 800-53 control mappings
- ✅ JAMA-Requirement-ID placeholders
- ✅ Component description and implementation details

**If Claude's response is incomplete:**
- Ask follow-up: "Add more implementation details to the control-implementations section"
- Or: "Expand the properties array to include all subrequirements (a, b, c, d)"

### Step 3: Save Output as `nerc-oscal.json` (2 minutes)

**What to do:**

1. Copy the JSON from Claude's response
2. Create a new file in this directory: `nerc-oscal.json`
3. Paste the JSON into the file
4. Save the file

**Verify:**
- File is in the same directory as this README.md
- File is named exactly `nerc-oscal.json` (case-sensitive on Linux/Mac)
- JSON is valid (use an online JSON validator if unsure)

**Example structure:**
```json
{
  "component-definition": {
    "uuid": "12345678-1234-1234-1234-123456789012",
    "metadata": {
      "title": "NERC-CIP-005 Control Implementation",
      ...
    },
    "components": [
      {
        "uuid": "...",
        "title": "NERC CIP-005 Systems Security Management",
        "description": "...",
        "properties": [...]
      }
    ]
  }
}
```

### Step 4: Run Validator (2-3 minutes)

**What to do:**

Open terminal/command prompt and navigate to this directory, then run:

```bash
pytest verify_oscal_compliance.py -v
```

**Expected output:**
```
test_is_valid_json PASSED
test_has_component_definition_root PASSED
test_component_def_has_metadata PASSED
test_metadata_has_required_fields PASSED
...
======================== 22 passed in 2.34s ========================
```

### Step 5: Interpret Results (Review)

**All tests pass (✅):**
- Your OSCAL JSON is valid and ready for use
- Can be imported into JAMA
- Can be traced to NIST 800-53
- Can be used as compliance evidence

**Some tests fail (❌):**
- Review the error message for which test failed
- Common failures:
  - Missing JAMA-Requirement-ID → Ask Claude to add JAMA properties
  - Invalid NIST control format → Ask Claude to use format like "SC-7"
  - Missing control-implementations → Ask Claude to add implementation details
- Go back to Step 2 and ask Claude to fix the specific issue
- Save the updated JSON and re-run pytest

### Step 6 (NEW): Export to JAMA CSV Traceability Matrix (2 minutes)

**What to do:**

Once validation passes, export your OSCAL JSON to a JAMA-compatible CSV:

```bash
python oscal_to_jama_csv.py nerc-oscal.json --validate
```

**Expected output:**
```
[OK] Successfully exported 3 components to nerc-oscal.csv
[OK] CSV validation passed (3 rows)
[OK] JAMA export is valid and ready for import
```

**What you get:**
- `nerc-oscal.csv` - A CSV file with columns:
  - `JAMA-Requirement-ID` - Requirement ID in JAMA format
  - `NERC-Requirement-ID` - Original NERC standard reference
  - `NIST-Primary-Control` - Primary NIST 800-53 control mapping
  - `NIST-Secondary-Controls` - Additional related controls
  - `Title` - Requirement title
  - `Description` - Full requirement description
  - `Implementation-Status` - Current status (Draft/Implemented)

**How to use in JAMA:**
1. Open JAMA Requirements Management System
2. Create new Project or Requirements Set
3. Use "Import" feature → Select CSV file
4. Map CSV columns to JAMA fields
5. Import completes with full traceability

---

## New Enhanced Features (Tier 1)

### 1. NIST Control Validation

The toolkit now validates that all mapped NIST controls exist in the official NIST SP 800-53 R5 catalog:

```bash
pytest verify_oscal_compliance.py::TestOSCALCompliance::test_nist_controls_exist_in_catalog -v
```

**What it checks:**
- ✅ All NIST control IDs follow proper format (e.g., SC-7, AC-2)
- ✅ All controls exist in NIST SP 800-53 R5 official catalog
- ✅ No typos in control mappings (prevents SC-7 → ZZ-99 errors)

**Common errors fixed:**
- Invalid control format (e.g., "Security Control 7" → must be "SC-7")
- Non-existent controls (e.g., "XX-99" → verify in catalog)

### 2. JAMA CSV Export Utility

New `oscal_to_jama_csv.py` script provides command-line control:

**Basic export:**
```bash
python oscal_to_jama_csv.py nerc-oscal.json
```

**Export with custom output:**
```bash
python oscal_to_jama_csv.py nerc-oscal.json -o my-traceability-matrix.csv
```

**Detailed format (includes metadata):**
```bash
python oscal_to_jama_csv.py nerc-oscal.json --format detailed
```

**Validate CSV before import:**
```bash
python oscal_to_jama_csv.py nerc-oscal.json --validate
```

### 3. Expanded Test Suite (27 Tests)

The toolkit now includes 5 additional validation tests:

- **Test 23:** NIST controls exist in catalog
- **Test 24:** NIST controls have descriptions
- **Test 25:** CSV export format is valid
- **Test 26:** CSV includes required columns
- **Test 27:** CSV has no empty requirement IDs

Run all validation:
```bash
pytest verify_oscal_compliance.py -v
```

---

## Detailed Test Explanations

### Core Tests (Run First)

#### Test 1: JSON Validity (`test_is_valid_json`)
- **What it checks:** The file is valid JSON
- **Why it matters:** JSON must be parseable by tools and JAMA
- **Common error:** "JSON syntax error" → Check for missing commas, quotes, brackets
- **Fix:** Use an online JSON validator or ask Claude to fix syntax

#### Test 6: NIST Mapping (`test_has_nist_mapping`)
- **What it checks:** Every component maps to at least one NIST 800-53 control
- **Why it matters:** NERC requirements must trace to NIST for compliance evidence
- **Common error:** "Missing NIST 800-53 mapping" → Component has no NIST controls
- **Fix:** Ask Claude to add property: `"NIST-800-53-Primary-Control": "SC-7"` (example)

#### Test 9: JAMA Properties (`test_jama_props_exist`)
- **What it checks:** Components have JAMA-Requirement-ID fields
- **Why it matters:** JAMA placeholders enable traceability to requirements
- **Common error:** "Missing JAMA-Requirement-ID property" → Add property to component
- **Fix:** Ask Claude to add: `"JAMA-Requirement-ID": "CIP-005-R1-a"` format

### Validation Tests

#### Test 13: NERC Requirement Format (`test_nerc_requirement_format`)
- **Expected format:** `CIP-005-6 R1` or `CIP-005 R2`
- **Example:** `"NERC-Requirement-ID": "CIP-005-6 R1"`
- **Invalid examples:** `CIP005R1` (missing hyphens), `NERC-R1` (missing standard code)

#### Test 10: JAMA Placeholder Format (`test_jama_placeholders_follow_format`)
- **Expected format:** `CIP-###-R#-[a-z]`
- **Examples:** `CIP-005-R1-a`, `CIP-005-R1-b`, `CIP-007-R3-c`
- **Invalid examples:** `CIP005R1A` (wrong format), `JAMA-001` (not NERC-based)

#### Test 7: NIST Control Format (`test_nist_controls_are_valid_format`)
- **Expected format:** Two-letter family code + hyphen + number
- **Examples:** `SC-7`, `AC-2`, `CA-3`, `IR-4`
- **Invalid examples:** `SC7` (missing hyphen), `Security Control 7` (spelled out)

---

## Example: CIP-005 R1 to OSCAL JSON

### Input (Raw NERC Text)
```
CIP-005-6 Requirement 1: Systems Security Management

The Responsible Entity shall implement one or more documented,
recoverable, and type-certified processes for generating, storing,
protecting, and managing the Cyber Security Plan that includes:

a) The roles and responsibilities for developing, approving,
   implementing, and maintaining the plan
```

### Expected OSCAL Output (Simplified)
```json
{
  "component-definition": {
    "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "metadata": {
      "title": "NERC-CIP-005 Control Implementation",
      "published": "2026-01-20T00:00:00Z",
      "version": "1.0.0"
    },
    "components": [
      {
        "uuid": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
        "type": "software",
        "title": "NERC CIP-005 Systems Security Management",
        "description": "Implements documented cyber security planning processes including role definition, effectiveness assessment, review scheduling, and recovery assurance for CIP-005 R1.",
        "properties": [
          {
            "name": "NERC-Requirement-ID",
            "value": "CIP-005-6 R1"
          },
          {
            "name": "NIST-800-53-Primary-Control",
            "value": "SC-7"
          },
          {
            "name": "NIST-800-53-Secondary-Controls",
            "value": "CA-3, PL-2"
          },
          {
            "name": "JAMA-Requirement-ID",
            "value": "CIP-005-R1-a"
          },
          {
            "name": "Implementation-Status",
            "value": "Draft"
          }
        ],
        "control-implementations": [
          {
            "description": "Systems Security Plan documentation and management",
            "implemented-requirements": [
              {
                "uuid": "c3d4e5f6-a7b8-9012-cdef-123456789012",
                "control-id": "sc-7",
                "responsibility": "Implemented",
                "properties": [
                  {
                    "name": "JAMA-Requirement-ID",
                    "value": "CIP-005-R1-a"
                  }
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

### Validation Results
```
✅ test_is_valid_json PASSED
✅ test_has_component_definition_root PASSED
✅ test_has_nist_mapping PASSED
✅ test_jama_props_exist PASSED
✅ test_nerc_req_ids_exist PASSED
✅ test_oscal_is_jama_ready PASSED
... (all 22 tests pass)
```

---

## Troubleshooting

### Problem: "OSCAL file not found: nerc-oscal.json"

**Cause:** The file doesn't exist or is in the wrong directory.

**Solution:**
1. Verify file is in the same directory as README.md
2. Check spelling: exactly `nerc-oscal.json` (lowercase, with hyphens)
3. On Linux/Mac: filenames are case-sensitive

### Problem: "JSON syntax error in OSCAL file"

**Cause:** The JSON is malformed (missing quotes, commas, brackets).

**Solution:**
1. Copy the JSON into an online JSON validator (https://jsonlint.com/)
2. Look for red error indicators
3. Ask Claude: "Fix the JSON syntax error in this OSCAL output" + paste the JSON
4. Save the corrected JSON

### Problem: "Component X missing NIST 800-53 mapping"

**Cause:** Claude didn't include NIST control mappings.

**Solution:**
1. Ask Claude: "Add NIST 800-53 control mapping to this OSCAL JSON. For each component, add a property with name='NIST-800-53-Primary-Control' and value like 'SC-7'"
2. Ask Claude which NIST controls apply to your NERC requirement
3. Paste the corrected JSON into `nerc-oscal.json`
4. Re-run validator

### Problem: "JAMA-Requirement-ID values follow invalid format"

**Cause:** JAMA placeholders don't match expected pattern.

**Expected:** `CIP-005-R1-a` (CIP-[3-digit-code]-R[number]-[letter])

**Invalid examples:** `JAMA-001`, `CIP005R1A` (wrong format), `CIP-R1` (missing standard number)

**Solution:**
1. Ask Claude: "Fix JAMA-Requirement-ID format. Should be like 'CIP-005-R1-a', 'CIP-005-R1-b', etc."
2. Ensure every subrequirement (a, b, c) gets its own JAMA ID
3. Save corrected JSON and re-run

### Problem: pytest command not found

**Cause:** pytest not installed or not in PATH.

**Solution:**
```bash
# Install pytest
pip install pytest

# Verify installation
pytest --version

# If still not found, use Python module:
python -m pytest verify_oscal_compliance.py -v
```

---

## Integration: Next Steps After Validation

Once your OSCAL JSON passes all tests:

### Export to JAMA Traceability Matrix
```bash
# (Future tool) Convert OSCAL JSON to CSV for JAMA import
python oscal_to_jama_csv.py nerc-oscal.json > traceability-matrix.csv
```

### Map to Cloud Infrastructure Tests
Link JAMA requirement IDs to pytest tests in your cloud infrastructure:
```
JAMA-ID: CIP-005-R1-a
└─ NIST Control: SC-7 (Boundary Protection)
└─ Cloud Test: tests/test_security_boundary.py::test_vpc_security_groups
```

### Use as Compliance Evidence
- Reference in audit responses: "See nerc-oscal.json:components[0]:properties[JAMA-Requirement-ID]"
- Export properties as evidence spreadsheet
- Link to cloud infrastructure test results

---

## Reference: Files in This Toolkit

### Core Toolkit
| File | Purpose | When to Use |
|---|---|---|
| `README.md` | This file. Usage instructions and troubleshooting | First! Read this before starting |
| `CLAUDE.md` | Developer guide for architecture, commands, and development | Reference during development; consult for architecture questions |
| `CLAUDE_README.md` | Meta-guide explaining how to use CLAUDE.md | Understand what CLAUDE.md provides and how to leverage it |
| `TRAVIS-NERC-PROMPT.md` | Claude Code prompt for OSCAL generation | Step 2: Copy the PROMPT section into Claude Code |
| `verify_oscal_compliance.py` | Pytest validator for OSCAL JSON quality | Step 4: Run with `pytest verify_oscal_compliance.py -v` |
| `nist_controls.py` | NIST SP 800-53 R5 control catalog and validation | Used internally by validator; reference for control lookups |
| `oscal_to_jama_csv.py` | CSV export utility for JAMA traceability matrix | Step 6: Export validated OSCAL to CSV format |

### Generated Outputs (v1.1.0)
| File/Directory | Purpose | Contents |
|---|---|---|
| `nerc-oscal.json` | Complete OSCAL v1.1.0 dataset | 49 requirements across 14 standards (CIP-002 through CIP-015) |
| `nerc_all_combined.txt` | Full NERC text corpus | Combined extracted text from all 30 PDF standards |

### Parsing Toolchain (v1.1.0)
| File/Directory | Purpose | Usage |
|---|---|---|
| `nerc_pdf_parser.py` | PDF text extraction with OCR cleanup | Core PDF parsing engine; handles pagination filtering |
| `extract_nerc_text.py` | State machine-based requirement parsing | Converts raw PDF text to structured NERC requirement format |
| `generate_oscal.py` | OSCAL generation from parsed text | Reproducible script for generating OSCAL from NERC text |
| `test_nerc_parser.py` | Parser validation test suite | Unit tests for extraction and parsing logic |
| `NERC-CIP/` | NERC-CIP standards library | 30 PDF documents (CIP-002 through CIP-015 with versions) |
| `nerc_raw_text/` | Extracted text outputs | 30 .txt files corresponding to each PDF standard |

---

## Key Concepts

### OSCAL (Open Security and Compliance Assessment Language)
- Structured format for security compliance documentation
- Version used: **OSCAL v1.1.2**
- JSON format (this toolkit)
- Can be imported into JAMA, Tableau, and other tools

### NIST SP 800-53
- Security and Privacy Controls for Federal Information Systems
- 200+ controls organized by family (AC, AU, CA, CM, etc.)
- NERC-CIP requirements map to these controls

### NERC-CIP Standards
- North American Electric Reliability Corporation Critical Infrastructure Protection
- 14 standards (CIP-002 through CIP-013, plus enhancements)
- Used by electricity grid operators, power plants, etc.

### JAMA (Jira Align or similar)
- Requirements management platform
- This toolkit generates OSCAL that can be imported
- Enables traceability: NERC → NIST → Tests → Evidence

---

## Support & Feedback

**Issues?**
1. Check Troubleshooting section above
2. Run pytest with verbose output: `pytest verify_oscal_compliance.py -vv -s`
3. Review error messages carefully (they're designed to be helpful)

**Want to improve this toolkit?**
- Suggest better prompt wording
- Request additional validators
- Propose OSCAL schema improvements

---

## Credits

**Based on:** Spec-Driven Security Methodology from Cloud Security Intro Course (Module 1, Module 2)
- Prompt architecture adapted from Module 1: LIVE-DEMO-PROMPTS.md
- Validator pattern adapted from Module 1: test-spec-validator.py
- Traceability format from Module 2: Lab-2.2-Traceability-Matrix

**Latest Version:** 1.1.0 (January 25, 2026)
**Initial Release:** 1.0.0 (January 2026)

---

**Ready to convert NERC-CIP to OSCAL? Start with Step 1 above! 🚀**
