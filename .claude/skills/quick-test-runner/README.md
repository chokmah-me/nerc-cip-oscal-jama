# Quick Test Runner Skill - Usage Guide

## Overview

The `quick-test-runner` skill provides fast, focused test execution for rapid development feedback. Optimizes for speed over comprehensiveness - perfect for iterative development and immediate validation.

**Token Efficiency**: ~300 tokens vs ~1K full test suite (70% reduction)

## Quick Start

### Natural Language Invocation
```
"Run quick tests for this module"
"Give me fast feedback on these changes"
"Test only what's most likely to break"
```

### Direct Skill Invocation
```
/quick-test-runner
```

## When to Use

✅ **Rapid Development**:
- Iterative code changes
- Frequent validation needed
- Tight feedback loops
- Prototype development

✅ **Time-Conscious Testing**:
- Quick confidence checks
- Immediate validation
- Pre-commit verification
- Token budget constraints

✅ **Selective Validation**:
- Changed code areas
- High-risk components
- Critical functionality
- Likely failure points

## Testing Strategy

### Phase 1: Risk Assessment
Identifies what to test first:
- Recently modified files
- High-complexity functions
- Critical business logic
- Historical failure points

### Phase 2: Test Selection
Chooses optimal test subset:
- Fastest executing tests
- Highest coverage impact
- Most relevant scenarios
- Best failure detection

### Phase 3: Parallel Execution
Optimizes for speed:
- Concurrent test execution
- Resource utilization
- Priority scheduling
- Result aggregation

### Phase 4: Smart Filtering
Reduces noise:
- Relevant failures only
- Summary reporting
- Actionable feedback
- Next step suggestions

## Example Usage

### Example 1: Development Iteration
```
User: "Run quick tests after my changes"

Claude: ⚡ Executing quick test suite...

🎯 Smart Test Selection:
- Modified files: src/auth.py, src/user.py
- High-risk areas: Authentication, validation
- Historical failures: auth tests (3 recent)
- Selection time: 2.1 seconds

🏃‍♂️ Quick Test Execution:
✅ auth/test_login.py (0.8s) - 8 tests passed
✅ auth/test_validation.py (1.2s) - 12 tests passed  
✅ user/test_model.py (0.5s) - 15 tests passed
⚠️ user/test_api.py (2.1s) - 14 passed, 1 failed

❌ Failure Details:
test_user_creation_with_long_email - AssertionError
Expected: ValidationError raised
Actual: User created successfully
Location: user/test_api.py:89

💡 Immediate Actions:
1. Check email validation in user creation
2. Review User model validation rules
3. Verify database constraints

⏱️ Total time: 4.6 seconds
🎯 Coverage: Core functionality validated
📊 Full suite would take: 45 seconds
```

### Example 2: Pre-Commit Validation
```
User: "Quick test before I commit these changes"

Claude: ⚡ Running pre-commit quick tests...

🎯 Risk-Based Selection:
- Changed areas: Payment processing, validation
- Complexity score: High (new payment integration)
- Security relevance: Critical (financial)
- Test selection: 15 most relevant tests

🏃‍♂️ Priority Test Results:
✅ payment/test_validation.py (1.1s) - Payment validation
✅ payment/test_processing.py (2.3s) - Payment processing
✅ security/test_encryption.py (0.9s) - Data encryption
⚠️ payment/test_integration.py (3.2s) - Integration test

⚠️ Integration Warning:
test_payment_gateway_timeout - Slow response (4.2s)
Expected: <2s response time
Actual: 4.2s (may indicate performance issue)

🚦 Commit Recommendation:
⚠️ PROCEED WITH CAUTION
- Core functionality: ✅ Validated
- Performance: ⚠️ Monitor gateway timeouts
- Security: ✅ Critical areas tested

💡 Next Steps:
1. Commit current changes
2. Monitor payment performance in staging
3. Consider timeout configuration review

📊 Confidence Level: 85% (proceed with monitoring)
```

### Example 3: Bug Fix Verification
```
User: "Test that my bug fix actually works"

Claude: 🐛 Running targeted tests for bug fix verification...

🎯 Bug Fix Test Strategy:
- Bug: Race condition in cache update
- Fix: Added mutex locking
- Related tests: Cache consistency, concurrent access
- Historical failures: 5 cache-related test failures

🏃‍♂️ Targeted Test Execution:
✅ cache/test_concurrent.py (2.1s) - Concurrent cache access
✅ cache/test_consistency.py (1.8s) - Cache consistency checks
✅ cache/test_race_conditions.py (3.4s) - Race condition specific tests
✅ integration/test_cache_behavior.py (2.9s) - Integration behavior

🧪 Bug Fix Validation:
- Race condition tests: ✅ PASSED (previously failed)
- Concurrent access: ✅ STABLE (no timeouts)
- Consistency checks: ✅ VALIDATED
- Integration behavior: ✅ PRESERVED

📊 Before vs After Comparison:
Before fix: 3/7 race condition tests failed
After fix: 0/7 race condition tests failed
Improvement: 100% success rate

🎉 Fix Verification: SUCCESSFUL
- Root cause addressed: ✅ Mutex prevents concurrent modification
- No regressions: ✅ All related functionality preserved
- Performance acceptable: ✅ Slight overhead expected and acceptable

💾 Recommended: Commit this fix
```

## Test Selection Strategy

### 🔍 Risk-Based Selection
Prioritizes by failure likelihood:
```
1. Modified code areas (highest priority)
2. High-complexity functions
3. Critical business logic
4. Historical failure points
5. Integration boundaries
```

### ⚡ Speed Optimization
Optimizes for fast feedback:
```
1. Unit tests over integration tests
2. Fast assertions first
3. Parallel execution when possible
4. Minimal setup/teardown
5. Focused test scenarios
```

### 🎯 Impact Focus
Maximizes validation value:
```
1. Core functionality validation
2. Critical path coverage
3. High-risk scenario testing
4. Boundary condition checks
5. Error handling verification
```

## Test Categories

### 🏃‍♂️ Lightning Tests (<1s)
Ultra-fast validation:
- Unit tests for changed functions
- Basic assertion checks
- Syntax validation
- Import verification

### ⚡ Quick Tests (1-5s)
Fast functional validation:
- Model validation tests
- Service method tests
- Basic integration tests
- Security assertion tests

### 🎯 Focus Tests (5-15s)
Targeted deep validation:
- Complex business logic
- Integration critical paths
- Performance baseline tests
- Security vulnerability tests

### ❌ Skip for Speed
Omit to maximize velocity:
- Full integration suites
- Performance benchmarks
- UI/end-to-end tests
- Large dataset tests

## Configuration Options

**Speed vs Coverage**:
- `--lightning`: Ultra-fast (<10s total)
- `--quick`: Fast feedback (10-30s)
- `--balanced`: Moderate coverage (30-60s)

**Selection Strategy**:
- `--changed-only`: Only modified areas
- `--risk-based`: Risk-weighted selection
- `--smart`: AI-optimized selection

**Scope Control**:
- `--file=specific.py`: Single file focus
- `--module=auth`: Module-level testing
- `--project-wide`: Cross-module impact

## Integration with Development

**Tight Feedback Loop**:
```
1. Make small change
2. /quick-test-runner
3. Fix any issues immediately
4. Continue development
5. Repeat frequently
```

**Pre-Commit Workflow**:
```
1. Complete code changes
2. Run quick validation
3. Fix any failures
4. Run comprehensive tests if needed
5. Commit with confidence
```

**Continuous Validation**:
```
1. Set up automatic quick tests
2. Run on every file save
3. Get immediate feedback
4. Maintain development flow
5. Address issues instantly
```

## Performance Optimization

### Parallel Execution
Maximize concurrency:
```python
# Run independent tests in parallel
async def run_quick_tests(tests):
    results = await asyncio.gather(*[
        run_test(test) for test in tests
    ])
    return results
```

### Smart Caching
Avoid redundant work:
- Cache test discovery
- Reuse test fixtures
- Skip unchanged areas
- Remember previous results

### Selective Loading
Minimize startup time:
- Lazy import strategies
- Minimal fixture setup
- Targeted database access
- Optimized configuration

## Quality Assurance

### Risk Management
Balance speed with safety:
- Never skip critical security tests
- Always validate core functionality
- Maintain regression detection
- Include boundary condition tests

### Confidence Levels
Communicate certainty:
```
95%+: Safe to commit
85-94%: Proceed with monitoring
70-84%: Additional testing recommended
<70%: Run comprehensive tests
```

### Regression Detection
Ensure nothing breaks:
- Include historical failure points
- Test related functionality
- Validate integration points
- Check error handling

## Best Practices

### 1. Run Frequently
Integrate into development flow:
- After every meaningful change
- Before committing code
- When switching contexts
- Before pushing to shared branches

### 2. Act on Results
Respond immediately:
- Fix failures right away
- Investigate performance changes
- Address security warnings
- Document unexpected behaviors

### 3. Maintain Balance
Don't over-optimize for speed:
- Include critical validations
- Test important edge cases
- Validate security properties
- Check integration points

### 4. Continuously Improve
Refine based on experience:
- Track false positive rates
- Monitor missed regressions
- Adjust selection algorithms
- Update risk assessments

## Common Issues & Solutions

### Issue 1: Tests taking too long
**Solution**: Reduce scope or optimize selection algorithm

### Issue 2: Missing important failures
**Solution**: Improve risk assessment and selection criteria

### Issue 3: Too many false positives
**Solution**: Refine test selection and filtering

### Issue 4: Inconsistent results
**Solution**: Improve test isolation and determinism

## Token Efficiency

- Lightning mode: ~50 tokens
- Quick mode: ~150 tokens
- Balanced mode: ~300 tokens
- Analysis and selection: ~100 tokens

## Related Skills

- `development/lean-plan` - Plan rapid development
- `development/refactoring` - Make changes safely
- `analysis/code/dead-code-hunter` - Clean up after changes
- `git/diff-summariser` - Review changes before testing

---

**Ready for rapid feedback?** Just tell Claude: "Run quick tests" or "Give me fast validation"!