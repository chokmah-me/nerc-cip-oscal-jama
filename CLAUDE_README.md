# CLAUDE.md Reference Guide

## What is CLAUDE.md?

**CLAUDE.md** is a developer guide specifically designed for Claude Code (AI coding assistant) to understand the architecture, workflows, and development practices for the NERC-CIP OSCAL Toolkit.

This file helps Claude Code instances quickly become productive by providing:
- Architecture overview without requiring deep dives into multiple files
- Command reference for common development tasks
- Explanation of the three-layer compliance mapping system
- Format specifications and validation rules
- Troubleshooting guides with real error examples

## Who Should Read This?

### Primary Audience
- **Claude Code (AI Assistant):** Automatically consulted when Claude Code works on this repository
- **Human Developers:** Looking to understand the compliance mapping architecture
- **New Contributors:** Onboarding to the project

### Secondary Audience
- Project maintainers reviewing compliance validation logic
- Security teams implementing OSCAL-based compliance automation
- JAMA administrators integrating the toolkit

## How CLAUDE.md Helps Claude Code

### 1. Context Without File Hopping
Instead of reading through all files to understand the architecture, Claude Code can quickly grasp:
- **What the three layers are:** NERC → OSCAL → JAMA
- **Where each component lives:** Which Python file handles what
- **How data flows:** From regulatory text to compliance evidence
- **What validation ensures:** 27 specific checks and why each matters

### 2. Format Specifications
Reduces errors by providing exact format requirements:
```
NIST Control:     SC-7, AC-2 (not "SC7" or "Security Control 7")
NERC Requirement: CIP-005-6 R1 (includes version digit "-6")
JAMA Placeholder: CIP-005-R1-a (no version digit, includes letter)
```

### 3. Troubleshooting Guidance
When tests fail, CLAUDE.md provides:
- What the error actually means
- Real examples of ❌ wrong vs ✅ correct formats
- Exact fix code to copy
- Where to find the issue in the codebase

Example:
```
❌ "Component X maps to non-existent NIST control: 'XX-99'"
  → Run: from nist_controls import validate_nist_control
  → Check: print(validate_nist_control("SC-7"))  # Returns True
```

## Document Structure

### Essential Sections (for quick reference)
- **Quick Start Commands** - 7 essential pytest and export commands
- **Architecture & Data Flow** - Visual diagram + data structure examples
- **Three-Layer Compliance Mapping** - How NERC text becomes JAMA imports

### Deep Dive Sections (for implementation)
- **Core Components** - nist_controls.py, verify_oscal_compliance.py, oscal_to_jama_csv.py
- **NIST SP 800-53 R5 Reference** - Control families and NERC mappings
- **Complete Workflow** - 4-step user journey
- **Common Development Tasks** - Adding controls, creating tests

### Troubleshooting Sections
- **Troubleshooting Guide** - Real error messages and fixes (8 scenarios)
- **Testing Strategy** - How tests are organized and what to run
- **Key Concepts & Constraints** - Format requirements and validation rules

## Using CLAUDE.md During Development

### Scenario 1: Adding a New NIST Control
Search CLAUDE.md for "Adding a New NIST Control" → Copy exact code steps → No need to understand nist_controls.py internals

### Scenario 2: Writing a New Test
Search for "Creating a New Validation Test" → Follow pytest fixture pattern → Add to TestOSCALCompliance class

### Scenario 3: A Test Fails
Look up the error message in "Troubleshooting Guide" → Get exact cause, example fix, and validation command

### Scenario 4: Understanding Why 27 Tests Exist
Check "Testing Strategy by Category" → See the 7 categories and what each tests → Understand validation coverage

## Key Information Provided

### Command Reference
```bash
pytest verify_oscal_compliance.py -v              # All 27 tests
python oscal_to_jama_csv.py nerc-oscal.json      # Export to JAMA
```

### Format Specifications
- NIST: `[A-Z]{2}-\d{1,2}(\s*\([0-9]+\))?` (e.g., SC-7, AC-2(1))
- NERC: `CIP-\d{3}(?:-\d+)? R\d+[a-z]?` (e.g., CIP-005-6 R1)
- JAMA: `CIP-\d{3}-R\d+(-[a-z])?` (e.g., CIP-005-R1-a)

### Architecture Overview
```
NERC Text (CIP-005 R1)
  ↓ Claude prompt
OSCAL JSON (component-definition)
  ├─ Properties: NERC-ID, NIST-ID, JAMA-ID
  ├─ Control-implementations: SC-7, CA-3, PL-2
  └─ Metadata: uuid, timestamp, version
  ↓ Validation (27 tests) + Export
JAMA CSV (traceability-matrix.csv)
  └─ Import-ready for requirements management
```

## What CLAUDE.md Does NOT Include

- **User-facing instructions** (see README.md instead)
- **Line-by-line code comments** (see source files)
- **Installation steps** (see README.md)
- **NERC standard details** (refer to official NERC documentation)
- **JAMA admin setup** (refer to JAMA documentation)

## When CLAUDE.md Gets Used

1. **Automatically:** When Claude Code analyzes this repository
2. **Explicitly:** When a developer says "Use CLAUDE.md as reference"
3. **For Guidance:** When implementing new features or fixing bugs
4. **For Onboarding:** When new team members join the project

## Maintaining CLAUDE.md

### Update When:
- ✅ New Python files are added to the toolkit
- ✅ New validation tests are added (update test count from 27)
- ✅ New NIST control families are referenced
- ✅ New troubleshooting patterns emerge
- ✅ Architecture changes (e.g., new export formats)

### Do NOT Update For:
- ❌ Bug fixes in existing code (doesn't change architecture)
- ❌ Performance optimizations (doesn't change interfaces)
- ❌ Minor comment changes (use source file comments)
- ❌ User documentation (use README.md)

### Update Process:
1. Edit CLAUDE.md with architecture or command changes
2. Commit with clear message: "Update CLAUDE.md: [specific change]"
3. Push to remote immediately (this is reference documentation)

## Example: How Claude Code Uses CLAUDE.md

### Scenario: User asks to add validation for new field
```
User: "Add a test to check that all components have a 'risk-level' property"

Claude's process:
1. Reads CLAUDE.md "Creating a New Validation Test" section
2. Understands pytest fixture pattern (oscal_data parameter)
3. Sees that test numbers are sequential (Tests 1-27)
4. Adds new test as "Test 28: Components have risk-level property"
5. Uses exact assertion pattern from other tests in the file
6. Runs: pytest verify_oscal_compliance.py::TestOSCALCompliance::test_components_have_risk_level -v
7. Updates CLAUDE.md test count from 27 to 28
```

All without needing to understand pytest internals, fixtures, or the exact test file structure.

## Integration with Repository

```
repository/
├── README.md              ← User-facing guide (how to use the toolkit)
├── CLAUDE.md             ← AI assistant guide (architecture, commands, development)
├── CLAUDE_README.md      ← This file (how to use CLAUDE.md)
├── QUICK-START.md        ← 6-step workflow overview
├── TRAVIS-NERC-PROMPT.md ← AI prompt for OSCAL generation
├── verify_oscal_compliance.py    ← 27 validation tests
├── oscal_to_jama_csv.py         ← CSV export utility
├── nist_controls.py             ← NIST catalog + validation
└── nerc-oscal.json              ← User-generated OSCAL output
```

**Reading Order:**
1. First-time user: README.md → QUICK-START.md
2. Developer (human): README.md → CLAUDE.md → source files
3. Claude Code (AI): CLAUDE.md → source files (as needed)
4. AI prompt task: TRAVIS-NERC-PROMPT.md

## Benefits of This Approach

### For Claude Code
✅ Faster context acquisition (reads ~15-20 KB instead of 50+ KB of code)
✅ Clear format specifications reduce generation errors
✅ Troubleshooting section prevents common mistakes
✅ Architecture overview prevents misunderstandings

### For Developers
✅ One canonical source for architecture explanation
✅ Reduces need to explain project structure verbally
✅ New contributors onboard faster
✅ Maintenance tasks have clear instructions

### For the Project
✅ Consistency in how requirements are formatted
✅ Centralized documentation of validation rules
✅ Easier to onboard new tools/integrations
✅ Reduced support burden for explaining architecture

## References

- **CLAUDE.md** - This repository's developer guide
- **README.md** - User-facing documentation and quick start
- **TRAVIS-NERC-PROMPT.md** - AI prompt for OSCAL generation
- **NIST SP 800-53 R5** - https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
- **OSCAL Specification** - https://pages.nist.gov/OSCAL/

---

**Created:** 2026-01-20
**Last Updated:** 2026-01-20
**Author:** Claude Code (AI Assistant)
