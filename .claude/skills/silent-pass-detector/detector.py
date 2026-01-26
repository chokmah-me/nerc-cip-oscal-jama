"""
Silent Pass Test Detector - AST-based detection of tests that pass silently.

Identifies tests that pass because they validated zero items rather than
validating successfully. Detects patterns like:
  - Assertions inside conditional blocks that may never execute
  - Assertions inside loops that may be empty
  - Optional validation without minimum count checks

Usage:
    python detector.py test_file.py
    python detector.py test_file.py --output json
    python detector.py test_file.py --severity HIGH
"""

import ast
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Dict, Set


@dataclass
class Detection:
    """A detected silent pass risk in a test."""
    test_name: str
    line_number: int
    risk_level: str  # HIGH, MEDIUM, LOW
    pattern: str
    issue: str
    fix_suggestion: str


class SilentPassDetector(ast.NodeVisitor):
    """AST visitor to detect silent pass patterns in test files."""

    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.detections: List[Detection] = []
        self.in_test_function = False
        self.current_test_name = ""
        self.current_test_line = 0

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions, tracking test functions."""
        if node.name.startswith('test_'):
            old_in_test = self.in_test_function
            old_test_name = self.current_test_name
            old_test_line = self.current_test_line

            self.in_test_function = True
            self.current_test_name = node.name
            self.current_test_line = node.lineno

            # Analyze the test function
            self._analyze_test_function(node)

            # Restore state
            self.in_test_function = old_in_test
            self.current_test_name = old_test_name
            self.current_test_line = old_test_line
        else:
            self.generic_visit(node)

    def _analyze_test_function(self, node: ast.FunctionDef) -> None:
        """Analyze a test function for silent pass patterns."""
        # Check for early pytest.skip() - if test skips early, it's safe
        if self._has_early_skip(node):
            return

        # Check for conditional assertions
        has_cond_assert = self._has_conditional_assertions(node)
        has_count_check = self._has_count_check(node)

        # Pattern 1: Conditional assertions in loops without count check
        if has_cond_assert and not has_count_check:
            self.detections.append(Detection(
                test_name=node.name,
                line_number=node.lineno,
                risk_level="HIGH",
                pattern="conditional_assertion_in_loop",
                issue="All assertions are inside conditional blocks that may not execute",
                fix_suggestion=self._suggest_fix_conditional_assert(node)
            ))
        # Pattern 2: Early continue/return in loop
        elif self._has_early_continue_in_loop(node) and not has_count_check:
            self.detections.append(Detection(
                test_name=node.name,
                line_number=node.lineno,
                risk_level="MEDIUM",
                pattern="early_continue_in_loop",
                issue="Loop has early continue/return that skips all validations",
                fix_suggestion=self._suggest_fix_early_continue(node)
            ))
        # Pattern 3: Nested empty loops
        elif self._has_nested_empty_loops(node) and not has_count_check:
            self.detections.append(Detection(
                test_name=node.name,
                line_number=node.lineno,
                risk_level="LOW",
                pattern="nested_empty_loops",
                issue="Nested loops could both be empty, executing 0 assertions",
                fix_suggestion=self._suggest_fix_nested_loops(node)
            ))

    def _has_conditional_assertions(self, node: ast.AST) -> bool:
        """Check if function has assertions inside conditional blocks.

        Ignores pytest.skip() calls as they're acceptable in conditionals.
        """
        for child in ast.walk(node):
            # Look for If nodes that contain Assert nodes
            if isinstance(child, ast.If):
                # Check if this if block only contains skip/continue
                has_skip = False
                has_assert = False

                for item in child.body:
                    # Check for pytest.skip() or similar
                    if isinstance(item, ast.Expr):
                        if isinstance(item.value, ast.Call):
                            call_name = self._get_call_name(item.value)
                            if call_name in ['skip', 'pytest.skip']:
                                has_skip = True
                    if isinstance(item, ast.Assert):
                        has_assert = True

                # Only flag if we have asserts without skip handling
                if has_assert and not has_skip:
                    return True

            # Look for conditional expressions with asserts
            if isinstance(child, ast.IfExp):
                for item in ast.walk(child):
                    if isinstance(item, ast.Assert):
                        return True
        return False

    def _get_call_name(self, call: ast.Call) -> str:
        """Extract function name from a call node."""
        if isinstance(call.func, ast.Name):
            return call.func.id
        elif isinstance(call.func, ast.Attribute):
            parts = []
            node = call.func
            while isinstance(node, ast.Attribute):
                parts.insert(0, node.attr)
                node = node.value
            if isinstance(node, ast.Name):
                parts.insert(0, node.id)
            return ".".join(parts)
        return ""

    def _has_early_skip(self, func: ast.FunctionDef) -> bool:
        """Check if test has early pytest.skip() call.

        If a test skips early (e.g., missing required data), it's safe
        from silent pass risks - it won't reach assertions.
        """
        for stmt in func.body:
            # Check if statement is pytest.skip()
            if isinstance(stmt, ast.Expr):
                if isinstance(stmt.value, ast.Call):
                    call_name = self._get_call_name(stmt.value)
                    if call_name in ['skip', 'pytest.skip']:
                        return True

            # Check if any early return
            if isinstance(stmt, ast.Return):
                return True

        return False

    def _has_count_check(self, node: ast.FunctionDef) -> bool:
        """Check if function has validation counter + assertion pattern."""
        body_str = ast.unparse(node) if hasattr(ast, 'unparse') else ""

        # Look for patterns like:
        # count = 0
        # ... loop with count += 1 ...
        # assert count > 0
        has_counter = False
        has_increment = False
        has_assertion = False

        for child in ast.walk(node):
            # Look for assignments: counter = 0
            if isinstance(child, ast.Assign):
                for target in child.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        if 'count' in name.lower() or 'validated' in name.lower():
                            has_counter = True

            # Look for augmented assignments: counter += 1
            if isinstance(child, ast.AugAssign):
                if isinstance(child.target, ast.Name):
                    name = child.target.id
                    if 'count' in name.lower() or 'validated' in name.lower():
                        has_increment = True

            # Look for assertions on counter
            if isinstance(child, ast.Assert):
                test_str = ast.unparse(child.test) if hasattr(ast, 'unparse') else ""
                if ('count' in test_str.lower() or 'validated' in test_str.lower()) \
                   and ('>' in test_str or '>=' in test_str or '==' in test_str):
                    has_assertion = True

        return has_counter and has_increment and has_assertion

    def _has_early_continue_in_loop(self, node: ast.FunctionDef) -> bool:
        """Check if loop has early continue/return that skips assertions."""
        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)):
                # Check if loop body has continue/return before assertions
                has_continue = False
                has_assertion = False

                for item in child.body:
                    if isinstance(item, (ast.Continue, ast.Return)):
                        has_continue = True
                    if isinstance(item, ast.Assert):
                        has_assertion = True

                if has_continue and has_assertion:
                    return True
        return False

    def _has_nested_empty_loops(self, node: ast.FunctionDef) -> bool:
        """Check for nested loops that could both be empty."""
        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)):
                for inner in ast.walk(child):
                    if inner != child and isinstance(inner, (ast.For, ast.While)):
                        # Found nested loop, check for assertions inside
                        for assertion in ast.walk(inner):
                            if isinstance(assertion, ast.Assert):
                                return True
        return False

    def _suggest_fix_conditional_assert(self, node: ast.FunctionDef) -> str:
        """Generate fix suggestion for conditional assertions."""
        return """Add validation counter after loop:

    validation_count = 0

    # ... keep your loop and assertions ...
    if condition:
        assert validation_check()
        validation_count += 1  # ← ADD THIS

    # ← ADD AFTER LOOP:
    assert validation_count > 0, \\
        "No validations performed - check your data!"

This guarantees the test fails if no items were validated."""

    def _suggest_fix_early_continue(self, node: ast.FunctionDef) -> str:
        """Generate fix suggestion for early continue in loops."""
        return """Add counter for non-skipped items:

    validated_items = 0

    for item in items:
        if should_skip(item):
            continue

        assert validate(item)
        validated_items += 1  # ← ADD THIS

    # ← ADD AFTER LOOP:
    assert validated_items > 0, \\
        "All items were skipped - no validation performed!"

Alternatively, use pytest.skip() if all items are expected to be skipped."""

    def _suggest_fix_nested_loops(self, node: ast.FunctionDef) -> str:
        """Generate fix suggestion for nested empty loops."""
        return """Add explicit length checks:

    # Before loop, verify outer loop will iterate
    items = get_items()
    if not items:
        pytest.skip("No items to validate")

    # Or add validation counter
    validation_count = 0

    for item in items:
        for sub in item.get('sub_items', []):
            assert validate(sub)
            validation_count += 1

    assert validation_count > 0, \\
        "No sub-items found to validate"

This ensures the test fails if no assertions actually execute."""


def analyze_test_file(file_path: str) -> List[Detection]:
    """Analyze a Python test file and return detected silent pass risks."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
            source_lines = source.split('\n')

        tree = ast.parse(source, filename=file_path)
        detector = SilentPassDetector(source_lines)
        detector.visit(tree)

        return detector.detections
    except SyntaxError as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}", file=sys.stderr)
        return []


def format_text_report(file_path: str, detections: List[Detection]) -> str:
    """Format detections as human-readable text report."""
    lines = []
    lines.append("=" * 60)
    lines.append("Silent Pass Test Detection Report")
    lines.append("=" * 60)
    lines.append(f"\nFile: {file_path}")
    lines.append(f"Silent pass risks detected: {len(detections)}")
    lines.append("")

    if not detections:
        lines.append("OK - No silent pass risks detected!")
        return "\n".join(lines)

    # Sort by risk level
    risk_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    sorted_detections = sorted(
        detections,
        key=lambda x: (risk_order.get(x.risk_level, 3), x.line_number)
    )

    # Group by risk level
    by_risk: Dict[str, List[Detection]] = {}
    for d in sorted_detections:
        if d.risk_level not in by_risk:
            by_risk[d.risk_level] = []
        by_risk[d.risk_level].append(d)

    # Display detections
    for risk_level in ["HIGH", "MEDIUM", "LOW"]:
        if risk_level in by_risk:
            for detection in by_risk[risk_level]:
                lines.append("-" * 60)
                lines.append(f"[{detection.risk_level}] {detection.test_name} "
                           f"(line {detection.line_number})")
                lines.append(f"Pattern: {detection.pattern}")
                lines.append("")
                lines.append(f"Issue: {detection.issue}")
                lines.append("")
                lines.append("Suggested fix:")
                for fix_line in detection.fix_suggestion.split('\n'):
                    lines.append(f"  {fix_line}")
                lines.append("")

    # Summary
    lines.append("=" * 60)
    lines.append("Summary")
    lines.append("=" * 60)
    for risk in ["HIGH", "MEDIUM", "LOW"]:
        count = len(by_risk.get(risk, []))
        if count > 0:
            lines.append(f"  {risk:6s}: {count} test(s)")

    return "\n".join(lines)


def format_json_report(detections: List[Detection]) -> str:
    """Format detections as JSON."""
    data = [asdict(d) for d in detections]
    return json.dumps(data, indent=2)


def main():
    """Command-line interface."""
    if len(sys.argv) < 2:
        print("Usage: python detector.py <test_file.py> [options]")
        print("")
        print("Options:")
        print("  --output json     Output as JSON (default: text)")
        print("  --severity LEVEL  Filter by HIGH, MEDIUM, LOW")
        sys.exit(1)

    file_path = sys.argv[1]
    output_format = "text"
    severity_filter = None

    # Parse options
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_format = sys.argv[i + 1]
        elif sys.argv[i] == "--severity" and i + 1 < len(sys.argv):
            severity_filter = sys.argv[i + 1].upper()

    # Check file exists
    if not Path(file_path).exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Analyze
    detections = analyze_test_file(file_path)

    # Filter by severity
    if severity_filter:
        detections = [d for d in detections if d.risk_level == severity_filter]

    # Format output
    if output_format.lower() == "json":
        output = format_json_report(detections)
    else:
        output = format_text_report(file_path, detections)

    # Use utf-8 encoding for output
    if sys.stdout.encoding.lower() not in ['utf-8', 'utf8']:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print(output)

    # Exit with error code if HIGH risk found
    high_risk = any(d.risk_level == "HIGH" for d in detections)
    sys.exit(1 if high_risk else 0)


if __name__ == '__main__':
    main()
