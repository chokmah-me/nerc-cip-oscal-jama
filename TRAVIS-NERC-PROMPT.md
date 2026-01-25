# NERC-CIP to OSCAL Component Definition Generator
## AI-Powered Regulatory Text Transformation

**Purpose:** Convert unstructured NERC-CIP regulatory text into structured OSCAL v1.0.0 Catalogs with automatic NIST SP 800-53 mapping.

---

## PROMPT: Generate OSCAL Component Definition from NERC-CIP Standard Text

### Role & Context Setting

You are a **GRC Compliance Officer** with expertise in:
- NERC-CIP regulatory compliance standards
- NIST SP 800-53 security control framework
- OSCAL (Open Security and Compliance Assessment Language) v1.0.0 specification
- Cloud infrastructure security mapping

Your task: Transform raw NERC-CIP regulatory text into machine-readable OSCAL JSON that can be ingested by compliance tools, imported into JAMA, and traced through cloud infrastructure testing.

### Input Format: Raw NERC-CIP Regulatory Text

The input will be unstructured regulatory text from a NERC-CIP standard (e.g., CIP-005: Systems Security Management). Example structure:

```
REQUIREMENT: CIP-005-6 R1
Title: Security Management Plan

Systems Security Management (CIP-005) covers three capability areas:
- Systems Security Management
- Personnel & Training
- Cyber Security Plan

The Responsible Entity shall implement, in a physical security plan,
one or more documented processes that collectively include each of the
applicable items in CIP-005 R1 through R3...

R1. Each Responsible Entity shall implement one or more documented,
recoverable, and type-certified processes for generating, storing,
protecting, and managing the Cyber Security Plan that includes the
items in Requirement R1 (a) through R1(j).
```

### Processing Instructions: Semantic Mapping Logic

Follow these steps to transform NERC-CIP requirements into OSCAL controls:

#### Step 1: Parse NERC Requirement ID
- Extract NERC standard code (CIP-005) and requirement number (R1, R2, etc.)
- Parse specific subrequirements (R1a, R1b, etc.)
- **Output field:** `metadata.property` with key="NERC-Requirement-ID", value="CIP-005-6 R1"

#### Step 2: Identify Security Intent
- Read the regulatory text and identify the core security objective
- Map intent to NIST SP 800-53 control families (AC, AU, CA, CM, etc.)
- **Example mapping:**
  - "Cyber Security Plan documentation" → SC-7 (Boundary Protection) + CA-3 (Security Planning)
  - "Personnel training requirements" → AT-1 (Security Awareness)
  - "Access control requirements" → AC-2 (Account Management)

#### Step 3: Match NIST 800-53 Controls
- For each NERC requirement, identify primary and secondary NIST controls
- **Primary control:** The best match (e.g., "SC-7")
- **Secondary controls:** Related controls for completeness (e.g., "CA-3", "CM-2")
- Create `properties` entries for each mapping

#### Step 4: Generate OSCAL Component Definition
- **Component Name:** Derive from NERC standard title (e.g., "NERC CIP-005 Systems Security Management")
- **Component Type:** "software" (for system controls) or "hardware" (for physical controls)
- **Component Scope:** Map requirement text to OSCAL control descriptions
- Include NIST 800-53 control mapping in `properties`

#### Step 5: Add JAMA Placeholders
- For each OSCAL control, add a `properties` entry:
  - Key: "JAMA-Requirement-ID"
  - Value: Placeholder format "CIP-{standard-number}-{requirement-number}-{subrequirement-letter}"
  - **Example:** "CIP-005-R1-a", "CIP-005-R1-b"
- This allows the OSCAL to be imported into JAMA and linked to traceability matrices

### Output Format: OSCAL v1.0.0 JSON Catalog

Generate valid OSCAL JSON with this structure:

```json
{
  "component-definition": {
    "uuid": "unique-uuid-v4",
    "metadata": {
      "title": "NERC-CIP [Standard] Control Implementation",
      "published": "2026-01-20T00:00:00Z",
      "last-modified": "2026-01-20T00:00:00Z",
      "version": "1.0.0",
      "document-ids": [
        {
          "scheme": "https://example.com",
          "identifier": "NERC-CIP-[STANDARD-NUMBER]-[VERSION]"
        }
      ]
    },
    "components": [
      {
        "uuid": "component-uuid",
        "type": "software",
        "title": "[NERC Standard Title]",
        "description": "[Parsed regulatory text summary]",
        "properties": [
          {
            "name": "NERC-Requirement-ID",
            "value": "[CIP-###-# R#]"
          },
          {
            "name": "NIST-800-53-Primary-Control",
            "value": "[CONTROL-ID]"
          },
          {
            "name": "NIST-800-53-Secondary-Controls",
            "value": "[CONTROL-ID-1, CONTROL-ID-2]"
          },
          {
            "name": "JAMA-Requirement-ID",
            "value": "[PLACEHOLDER-ID]"
          },
          {
            "name": "Implementation-Status",
            "value": "Draft"
          }
        ],
        "control-implementations": [
          {
            "description": "[Control implementation description]",
            "implemented-requirements": [
              {
                "uuid": "requirement-uuid",
                "control-id": "[NIST-CONTROL-ID]",
                "responsibility": "Implemented",
                "properties": [
                  {
                    "name": "JAMA-Requirement-ID",
                    "value": "[PLACEHOLDER-ID]"
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

### Quality Constraints

Ensure the generated OSCAL JSON meets these requirements:

1. **JSON Validity:** Must be valid JSON parseable by standard JSON validators
2. **Minimum Controls:** At least 5 distinct NIST 800-53 controls per NERC standard
3. **NIST Mapping:** Every NERC requirement must map to at least one NIST control
4. **JAMA Placeholders:** Every control must include a JAMA-Requirement-ID property
5. **Documentation Completeness:**
   - Component description summarizes regulatory intent
   - Each control lists specific implementation steps
   - No vague language ("ensure", "implement", "verify" without context)
6. **Traceability:** All properties must be structured for CSV export:
   - NERC-Requirement-ID matches regex: `CIP-\d{3}-\d R[0-9]`
   - JAMA-Requirement-ID matches regex: `CIP-\d{3}-R[0-9]-[a-z]`

### NERC-to-NIST Mapping Guidelines

Use these semantic patterns to map NERC requirements to NIST 800-53 controls:

| NERC Requirement Theme | NIST Control Family | Example Mapping |
|---|---|---|
| System segmentation, network boundaries | SC-7 | Boundary Protection |
| Access control, user authentication | AC-2, AC-3 | Account Management, Access Enforcement |
| Personnel training, awareness | AT-1 | Security Awareness |
| System change management | CM-3, CM-4 | Access Restrictions for Change |
| Incident response | IR-4, IR-5 | Incident Handling |
| Configuration management | CM-2, CM-6 | Baseline Configuration |
| Audit and accountability | AU-2, AU-3 | Audit Events, Content of Audit Records |
| Security planning | CA-3, PL-2 | System Interconnections, Security Planning |
| Vulnerability management | RA-5, SI-2 | Vulnerability Scanning, Flaw Remediation |

### Generic NERC-CIP Example: CIP-005 R1 Input

**Input Regulatory Text:**
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

**Expected Transformation:**
- NERC Requirement: CIP-005-6 R1
- Primary NIST Control: SC-7 (Boundary Protection)
- Secondary Controls: CA-3 (System Interconnections), PL-2 (Security Planning)
- JAMA Placeholder: CIP-005-R1-a, CIP-005-R1-b, CIP-005-R1-c, CIP-005-R1-d
- Component Description: Systems security plan implementation with documented processes for development, review, and maintenance
- Key Implementation Details:
  - Documented process with role assignments
  - Recovery procedures (redundancy, backup)
  - Review schedule (recommend quarterly minimum)
  - Effectiveness measurement methodology

---

## OUTPUT INSTRUCTIONS

1. **Generate complete OSCAL JSON** (not snippets or partial code)
2. **Ensure valid JSON syntax** (use JSON validator before providing output)
3. **Include all metadata fields** (uuid, published, version, document-ids)
4. **Add JAMA placeholders** for every subrequirement
5. **Provide 2-3 sentence explanation** above the JSON:
   - NERC standard being converted
   - NIST controls identified
   - Any semantic mapping notes

6. **Format JSON with indentation** (4-space or 2-space, consistent)

---

## FOLLOW-UP WORKFLOW

After you provide the initial OSCAL JSON:

1. **Save to file:** `nerc-oscal.json`
2. **Run validator:** `pytest verify_oscal_compliance.py -v`
3. **Interpret results:**
   - ✅ All tests pass → JSON is ready for JAMA import
   - ❌ Failed tests → Review error messages, ask Claude for targeted fixes

---

## EXAMPLE: Quick Start

**Step 1:** Copy this entire prompt into Claude Code

**Step 2:** Paste NERC-CIP regulatory text (from your standard)

**Step 3:** Claude generates OSCAL JSON

**Step 4:** Save as `nerc-oscal.json`

**Step 5:** Run validator:
```bash
pytest verify_oscal_compliance.py -v
```

**Step 6:** Review test results → Get human-readable feedback on gaps

---

**NERC-CIP to OSCAL Converter v1.0**
*Last Updated: January 2026*
*Based on: Spec-Driven Security Methodology from Cloud Security Intro Course*
