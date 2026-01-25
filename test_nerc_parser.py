"""
Unit tests for NERC PDF Parser
Tests the PDF extraction logic without requiring actual NERC PDF files
"""

import pytest
import json
from nerc_pdf_parser import NERECPDFParser


class TestNERECPDFParser:
    """Test suite for NERC PDF parser."""

    def test_requirement_pattern_matching(self):
        """Test regex pattern matches valid NERC requirement IDs."""
        parser = NERECPDFParser()

        test_cases = [
            ("CIP-005-6 R1", True),
            ("CIP-007-5 R2", True),
            ("CIP-010-2 R1", True),
            ("CIP-003-6 R1", True),
            ("Invalid-005-6 R1", False),
            ("CIP-005 R1", False),  # Missing version digit
            ("R1", False),
        ]

        for text, should_match in test_cases:
            matches = parser.REQUIREMENT_PATTERN.findall(text)
            if should_match:
                assert len(matches) > 0, f"Should match: {text}"
            else:
                assert len(matches) == 0, f"Should not match: {text}"

    def test_subrequirement_pattern_matching(self):
        """Test regex pattern matches subrequirement markers."""
        parser = NERECPDFParser()

        text = """
        a) First subrequirement
        b) Second subrequirement
        c) Third subrequirement
        """

        matches = parser.SUBREQUIREMENT_PATTERN.findall(text)
        assert len(matches) == 3, "Should find 3 subrequirement markers"

    def test_normalize_text(self):
        """Test text normalization removes extra whitespace."""
        parser = NERECPDFParser()

        # Input with multiple spaces and line breaks
        dirty_text = "The   Responsible   Entity\n\n\nshall  implement\n\nprocesses"

        normalized = parser._normalize_text(dirty_text)

        # Check spaces are normalized
        assert "   " not in normalized, "Should remove multiple spaces"
        assert "\n\n\n" not in normalized, "Should normalize consecutive newlines"
        # Should contain cleaned text
        assert "Responsible Entity" in normalized

    def test_extract_title_from_requirement_block(self):
        """Test title extraction from requirement text."""
        parser = NERECPDFParser()

        control_id = "CIP-005-6 R1"
        text = """CIP-005-6 R1: Systems Security Management
The Responsible Entity shall implement one or more documented processes
that collectively include each of the applicable items in CIP-005 R1.

a) The roles and responsibilities
b) The methodology for assessing"""

        title = parser._extract_title(control_id, text)

        # Should extract something reasonable
        assert title, "Should extract a title"
        assert "Systems Security Management" in title or "Responsible Entity" in title

    def test_extract_subrequirements(self):
        """Test extraction of subrequirement text."""
        parser = NERECPDFParser()

        text = """
a) The roles and responsibilities for developing and approving the plan
b) The methodology for assessing the effectiveness of the plan
c) A schedule for reviewing and updating the plan
d) The means to ensure recovery"""

        subrequirements = parser._extract_subrequirements(text)

        assert len(subrequirements) == 4, f"Should extract 4 subrequirements, got {len(subrequirements)}"

        # Check letters
        letters = [letter for letter, _ in subrequirements]
        assert letters == ['a', 'b', 'c', 'd']

        # Check text content
        texts = [text for _, text in subrequirements]
        assert "roles and responsibilities" in texts[0]
        assert "methodology" in texts[1]

    def test_clean_text(self):
        """Test cleaning of requirement text."""
        parser = NERECPDFParser()

        text = """CIP-005-6 R1: Header
Requirement: Some Title
The Responsible Entity shall implement processes
a) Item one
b) Item two"""

        cleaned = parser._clean_text(text)

        # Should remove leading control_id
        assert not cleaned.startswith("CIP-005"), "Should remove control_id prefix"
        # Should preserve core content
        assert "Responsible Entity" in cleaned

    def test_parse_requirement_block(self):
        """Test parsing of a complete requirement block."""
        parser = NERECPDFParser()

        control_id = "CIP-005-6 R1"
        text = """CIP-005-6 R1: Systems Security Management
The Responsible Entity shall implement one or more documented processes.

a) The roles and responsibilities
b) The methodology for assessing
c) A schedule for reviewing"""

        parsed = parser._parse_requirement_block(control_id, text, page_num=5)

        assert parsed is not None
        assert parsed['control_id'] == control_id
        assert parsed['page_number'] == 5
        assert len(parsed['subrequirements']) == 3
        assert parsed['subrequirements'][0][0] == 'a'

    def test_json_output_structure(self):
        """Test JSON output format is correct."""
        parser = NERECPDFParser()

        # Manually add a requirement for testing
        parser.requirements = [
            {
                'control_id': 'CIP-005-6 R1',
                'title': 'Systems Security Management',
                'text': 'The Responsible Entity shall implement processes',
                'subrequirements': [
                    ('a', 'First item'),
                    ('b', 'Second item')
                ],
                'page_number': 5
            }
        ]

        json_output = parser.to_json()

        # Parse JSON to verify structure
        data = json.loads(json_output)

        assert 'metadata' in data
        assert 'requirements' in data
        assert len(data['requirements']) == 1

        req = data['requirements'][0]
        assert req['control_id'] == 'CIP-005-6 R1'
        assert len(req['subrequirements']) == 2
        assert req['subrequirements'][0]['letter'] == 'a'

    def test_get_page_number(self):
        """Test page number mapping."""
        parser = NERECPDFParser()

        page_map = {0: 1, 5000: 2, 10000: 3}

        # Test character positions
        assert parser._get_page_number(100, page_map) == 1
        assert parser._get_page_number(5000, page_map) == 2
        assert parser._get_page_number(10500, page_map) == 3

    def test_requirement_pattern_capture_groups(self):
        """Test that requirement pattern captures correct groups."""
        parser = NERECPDFParser()

        text = "CIP-010-2 R3 Some title"
        match = parser.REQUIREMENT_PATTERN.search(text)

        assert match is not None
        assert match.group(1) == "CIP-010-2"  # Full CIP code with version
        assert match.group(2) == "3"  # Requirement number


class TestBatchParsing:
    """Test batch parsing functionality."""

    def test_batch_parse_requires_directory(self):
        """Test that batch_parse validates directory exists."""
        with pytest.raises(FileNotFoundError):
            NERECPDFParser.batch_parse('/nonexistent/directory')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
