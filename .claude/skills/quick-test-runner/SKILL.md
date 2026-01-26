---
name: quick-test-runner
description: Run tests impacted by recent changes and show last 20 lines of output. Use when user says "run impacted tests", "test my changes", or "did I break anything".
---

# Quick Test Runner Skill

## 🎯 Purpose
Run only tests affected by recent changes, show failures without full output (~800 tokens).

## 📋 Usage

When user requests impacted test run:

1. **Run the command** to find and execute relevant tests
2. **Show**:
   - List of impacted test files
   - Last 20 lines of test output (failures bubble up)
3. **Offer**: "Want full output or specific test details?"

## Command

```bash
git diff --name-only HEAD~1..HEAD | grep -E '\.(py|js|ts)' | xargs -I{} basename {} .py | xargs -I{} find test -name "*{}*" | head -10 | tee /tmp/impacted && npm test -- --testPathPattern="$(cat /tmp/impacted | tr '\n' '|')" 2>&1 | tail -20
```

## 🎁 Output Format

```
Impacted test files:
[list of test files matching changed source files]

Test results (last 20 lines):
[tail of test output - failures appear here]
```

## How It Works

1. **Find changed files**: `git diff --name-only HEAD~1..HEAD`
2. **Map to test files**: Find `test/*{filename}*`
3. **Run targeted tests**: Pass pattern to test runner
4. **Trim output**: Show last 20 lines (where failures appear)

## Multi-Framework Support

**Node.js (Jest/Vitest)**:
```bash
npm test -- --testPathPattern="pattern"
```

**Python (pytest)** - modify command:
```bash
pytest $(cat /tmp/impacted | tr '\n' ' ') 2>&1 | tail -20
```

**Go** - modify command:
```bash
go test $(cat /tmp/impacted | sed 's/test/./g' | tr '\n' ' ') 2>&1 | tail -20
```

## When to Use Full Output

If last 20 lines don't show the issue:
```bash
npm test -- --testPathPattern="specific_test" --verbose
```

## Token Efficiency

- ~800 tokens for focused test run
- Alternative: running full suite + reading all output (10k-50k tokens)
- 90%+ reduction in test feedback loop

## 🎛️ Parameters

This skill does not require parameters. It operates based on the current project context.

## 💡 Examples

### Basic Usage

User: "Use this skill"

Claude: Demonstrates the skill's functionality with example output.

## 🎁 Output

The skill produces relevant output based on the task performed.

## ⚠️ Important Notes

- Review output carefully before taking action
- Consider edge cases and potential side effects
- Consult documentation when needed
