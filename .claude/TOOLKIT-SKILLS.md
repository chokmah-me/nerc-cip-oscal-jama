# NERC-CIP OSCAL Toolkit Skills

This directory contains three production-ready Claude Code skills integrated from [claude-code-skills](https://github.com/chokmah-me/claude-code-skills) to enhance development workflow for the NERC-CIP OSCAL toolkit.

## Available Skills

### 1. Silent Pass Detector
**Purpose:** Detect tests that pass silently when validating zero items

- **Use when:** Running `check test quality`, `find silent pass tests`, or `validate test coverage`
- **Key benefit:** Catches hidden test failures where assertions never execute (e.g., conditional loops with zero matches)
- **Ideal for:** Your 27-test compliance suite to ensure all tests actually validate components
- **Command:** `/silent-pass-detector verify_oscal_compliance.py`

### 2. Quick Test Runner
**Purpose:** Run only tests impacted by recent changes

- **Use when:** Making changes and want to verify only affected tests
- **Key benefit:** Reduces feedback loop from full 27-test suite to only impacted tests
- **Ideal for:** Rapid iteration when fixing NIST mappings or component definitions
- **Command:** `/quick-test-runner`

### 3. Markdown Quality Validator
**Purpose:** Validate markdown structure, formatting, and content completeness

- **Use when:** Before releases, use `validate documentation`, `check markdown quality`
- **Key benefit:** Enforces heading hierarchy, detects TODO/FIXME placeholders, validates sections
- **Ideal for:** Your extensive documentation (README, GETTING-STARTED, ARCHITECTURE, RELEASES)
- **Command:** `/markdown-quality-validator docs/` or `/markdown-quality-validator README.md`

## How to Use

1. **View a skill's full documentation:**
   ```bash
   cat .claude/skills/silent-pass-detector/SKILL.md
   cat .claude/skills/quick-test-runner/SKILL.md
   cat .claude/skills/markdown-quality-validator/SKILL.md
   ```

2. **Invoke a skill in Claude Code:**
   - Type the skill name in Claude Code prompts
   - Example: "Use /silent-pass-detector to check test quality"

3. **Integrate into workflow:**
   - After making test changes: `/silent-pass-detector verify_oscal_compliance.py`
   - Before releases: `/markdown-quality-validator docs/`
   - During development: `/quick-test-runner` after code changes

## Skill Origins

All three skills are sourced from the [claude-code-skills](https://github.com/chokmah-me/claude-code-skills) production repository:
- `silent-pass-detector` - Detects real test quality issues found in v1.1.4
- `quick-test-runner` - Reduces test feedback loop for rapid iteration
- `markdown-quality-validator` - Quality gates for documentation releases

## Files Structure

```
.claude/skills/
├── silent-pass-detector/
│   ├── SKILL.md                    # Full skill documentation
│   └── [supporting files]
├── quick-test-runner/
│   ├── SKILL.md
│   └── [supporting files]
├── markdown-quality-validator/
│   ├── SKILL.md
│   └── [supporting files]
└── TOOLKIT-SKILLS.md               # This file
```

## Recommended Usage Sequence

1. **Setup:** Run silent-pass-detector on current test suite
   ```
   Objective: Validate all 27 tests are truly validating components
   ```

2. **Development:** Use quick-test-runner for rapid feedback
   ```
   After modifying NIST mappings: check only impacted tests
   ```

3. **Pre-Release:** Run markdown-quality-validator on docs
   ```
   Before v1.1.5: ensure all docs follow quality standards
   ```

## Integration with NERC-CIP OSCAL Workflow

- **Test Development:** silent-pass-detector catches hidden test failures
- **Feature Branches:** quick-test-runner accelerates feedback loops
- **Documentation:** markdown-quality-validator enforces quality gates

These skills complement the existing toolkit:
- `verify_oscal_compliance.py` (validation)
- `oscal_to_jama_csv.py` (export)
- `generate_oscal.py` (generation)

---

**Added:** 2026-01-25
**Source:** [claude-code-skills](https://github.com/chokmah-me/claude-code-skills) repository
**Branch:** `feature/toolkit-skills`
