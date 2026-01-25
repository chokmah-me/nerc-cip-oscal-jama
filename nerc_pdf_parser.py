"""
NERC-CIP PDF Parser
Extracts NERC-CIP requirements from PDF documents and structures them for OSCAL conversion.

This module handles:
- Loading NERC-CIP PDF files
- Extracting requirement tables (CIP-XXX-Y Table R1, R2, etc.)
- Parsing table columns: Part, Applicable Systems, Requirements, Measures
- Normalizing formatting and whitespace
- Outputting structured requirement data for batch OSCAL generation

Typical usage:
    parser = NERECPDFParser()
    requirements = parser.parse_pdf('cip-005-7.pdf')
    for req in requirements:
        print(req['control_id'], req['table_rows'])
"""

import re
import json
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
import pdfplumber


class NERECPDFParser:
    """Parse NERC-CIP PDF documents and extract requirement tables."""

    # Regex pattern for table title: CIP-005-7 Table R1 – Electronic Security Perimeter
    TABLE_TITLE_PATTERN = re.compile(
        r'CIP-(\d{3})-(\d+)\s+Table\s+R(\d+)\s+[–\-]?\s*(.+)',
        re.IGNORECASE
    )

    # Pattern to extract CIP standard code from filename (e.g., cip-005-7.pdf → CIP-005-7)
    FILENAME_PATTERN = re.compile(r'cip-(\d{3})-(\d+)', re.IGNORECASE)

    def __init__(self):
        """Initialize the parser."""
        self.requirements: List[Dict] = []
        self.pdf_filename: str = ""

    def parse_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Parse a NERC-CIP PDF file and extract requirement tables.

        Args:
            pdf_path: Path to the NERC-CIP PDF file

        Returns:
            List of requirement dictionaries with keys:
            - control_id: e.g., "CIP-005-7 R1"
            - title: Requirement table title (e.g., "Electronic Security Perimeter")
            - table_rows: List of dicts with keys: part, applicable_systems, requirements, measures
            - page_number: Page in PDF where table starts

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            pdfplumber.PDFException: If PDF is corrupted
        """
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        self.pdf_filename = pdf_file.name
        requirements = []

        with pdfplumber.open(pdf_path) as pdf:
            # Extract tables from all pages
            for page_num, page in enumerate(pdf.pages, 1):
                tables = page.extract_tables()

                if not tables:
                    continue

                # Process each table on this page
                for table in tables:
                    parsed_req = self._parse_requirement_table(table, page_num)
                    if parsed_req:
                        requirements.append(parsed_req)

        self.requirements = requirements
        return requirements

    def _parse_requirement_table(self, table: List[List[Optional[str]]], page_num: int) -> Optional[Dict]:
        """
        Parse a requirement table into structured data.

        Expects table format:
        Row 0: [empty, "CIP-005-7 Table R1 – Electronic Security Perimeter", ...]
        Row 1: [empty, "Part", empty, empty, "Applicable Systems", ..., "Requirements", ..., "Measures", ...]
        Row 2+: [part_id, None, None, systems_text, ..., requirements_text, ..., measures_text, ...]

        Args:
            table: 2D list of table cells from pdfplumber
            page_num: Page number where table appears

        Returns:
            Dictionary with control_id, title, table_rows, page_number; or None if not a requirement table
        """
        if not table or len(table) < 3:
            return None

        # Extract table title from first row
        title_cell = None
        for cell in table[0]:
            if cell and 'Table R' in cell:
                title_cell = cell
                break

        if not title_cell:
            # Not a requirement table, skip it
            return None

        # Parse table title: "CIP-005-7 Table R1 – Electronic Security Perimeter"
        match = self.TABLE_TITLE_PATTERN.search(title_cell)
        if not match:
            return None

        cip_num = match.group(1)
        cip_version = match.group(2)
        req_number = match.group(3)
        req_title = match.group(4).strip()

        control_id = f"CIP-{cip_num}-{cip_version} R{req_number}"

        # Find header row (row with "Part", "Requirements", "Measures", etc.)
        header_row_idx = None
        for i, row in enumerate(table):
            row_str = ' '.join([cell.lower() if cell else '' for cell in row])
            if 'part' in row_str and 'requirements' in row_str:
                header_row_idx = i
                break

        if header_row_idx is None:
            return None

        # Extract column positions
        header_row = table[header_row_idx]
        col_positions = self._find_table_columns(header_row)

        # Parse data rows
        table_rows = []
        for row_idx in range(header_row_idx + 1, len(table)):
            row = table[row_idx]

            # Skip severity level rows and other non-data rows
            if self._is_severity_row(row):
                continue

            parsed_row = self._parse_table_row(row, col_positions)
            if parsed_row and parsed_row.get('part'):
                table_rows.append(parsed_row)

        if not table_rows:
            return None

        return {
            'control_id': control_id,
            'title': req_title,
            'table_rows': table_rows,
            'page_number': page_num
        }

    def _find_table_columns(self, header_row: List[Optional[str]]) -> Dict[str, Optional[int]]:
        """
        Find the column indices for Part, Applicable Systems, Requirements, Measures.

        Args:
            header_row: Header row from table

        Returns:
            Dictionary mapping column name to column index
        """
        columns: Dict[str, Optional[int]] = {
            'part': None,
            'applicable_systems': None,
            'requirements': None,
            'measures': None
        }

        for i, cell in enumerate(header_row):
            if not cell:
                continue

            cell_lower = cell.lower().strip()

            if 'part' in cell_lower:
                columns['part'] = i
            elif 'applicable' in cell_lower or 'systems' in cell_lower:
                columns['applicable_systems'] = i
            elif 'requirement' in cell_lower and 'measures' not in cell_lower:
                columns['requirements'] = i
            elif 'measure' in cell_lower:
                columns['measures'] = i

        return columns

    def _is_severity_row(self, row: List[Optional[str]]) -> bool:
        """Check if row is a severity level row (not a requirement row)."""
        row_str = ' '.join([cell.lower() if cell else '' for cell in row])
        return any(x in row_str for x in ['severity', 'violation', 'vsl', 'version', 'date', 'action'])

    def _parse_table_row(self, row: List[Optional[str]], col_positions: Dict[str, int]) -> Optional[Dict]:
        """
        Parse a single table row into requirement data.

        Args:
            row: Table row cells
            col_positions: Dictionary mapping column names to indices

        Returns:
            Dictionary with part, applicable_systems, requirements, measures; or None if empty
        """
        if not row:
            return None

        # Extract values from appropriate columns
        def get_cell(col_name: str) -> str:
            idx = col_positions.get(col_name)
            if idx is not None and idx < len(row):
                cell = row[idx]
                return self._clean_cell_text(cell) if cell else ""
            return ""

        part = get_cell('part')
        systems = get_cell('applicable_systems')
        requirements = get_cell('requirements')
        measures = get_cell('measures')

        if not part or not requirements:
            return None

        return {
            'part': part,
            'applicable_systems': systems,
            'requirements': requirements,
            'measures': measures
        }

    def _clean_cell_text(self, text: Optional[str]) -> str:
        """Clean and normalize text from table cell."""
        if not text:
            return ""

        # Remove extra whitespace, including newlines
        text = ' '.join(text.split())

        return text.strip()

    def to_json(self, output_path: Optional[str] = None) -> str:
        """
        Convert parsed requirements to JSON format.

        Args:
            output_path: Optional path to save JSON file

        Returns:
            JSON string representation of requirements

        Example output:
            {
              "metadata": {
                "source_pdf": "cip-005-7.pdf",
                "total_requirements": 3,
                "total_table_rows": 12,
                "parser_version": "2.0.0"
              },
              "requirements": [
                {
                  "control_id": "CIP-005-7 R1",
                  "title": "Electronic Security Perimeter",
                  "table_rows": [
                    {"part": "1.1", "applicable_systems": "High Impact BES",
                     "requirements": "All applicable Cyber Assets connected to...",
                     "measures": "An example of evidence..."}
                  ],
                  "page_number": 6
                }
              ]
            }
        """
        total_rows = sum(len(req.get('table_rows', [])) for req in self.requirements)

        output_data = {
            'metadata': {
                'source_pdf': self.pdf_filename,
                'total_requirements': len(self.requirements),
                'total_table_rows': total_rows,
                'parser_version': '2.0.0'
            },
            'requirements': [
                {
                    'control_id': req['control_id'],
                    'title': req['title'],
                    'table_rows': req.get('table_rows', []),
                    'page_number': req['page_number']
                }
                for req in self.requirements
            ]
        }

        json_str = json.dumps(output_data, indent=2)

        if output_path:
            Path(output_path).write_text(json_str)

        return json_str

    @classmethod
    def batch_parse(cls, pdf_directory: str) -> Dict[str, List[Dict]]:
        """
        Parse all NERC-CIP PDFs in a directory.

        Args:
            pdf_directory: Directory containing NERC-CIP PDF files

        Returns:
            Dictionary mapping PDF filename to list of requirements
        """
        pdf_dir = Path(pdf_directory)
        if not pdf_dir.exists():
            raise FileNotFoundError(f"Directory not found: {pdf_directory}")

        all_requirements = {}
        parser = cls()

        for pdf_file in pdf_dir.glob('*.pdf'):
            try:
                requirements = parser.parse_pdf(str(pdf_file))
                all_requirements[pdf_file.name] = requirements
            except Exception as e:
                print(f"Error parsing {pdf_file.name}: {e}")
                all_requirements[pdf_file.name] = []

        return all_requirements


if __name__ == '__main__':
    # Example usage
    import sys

    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        parser = NERECPDFParser()
        requirements = parser.parse_pdf(pdf_path)

        print(f"Parsed {len(requirements)} requirements from {pdf_path}\n")
        for req in requirements:
            print(f"{req['control_id']}: {req['title']}")
            print(f"  Subrequirements: {[letter for letter, _ in req['subrequirements']]}")
            print(f"  Page: {req['page_number']}\n")

        # Save to JSON
        output_file = pdf_path.replace('.pdf', '-extracted.json')
        parser.to_json(output_file)
        print(f"Saved structured requirements to {output_file}")
    else:
        print("Usage: python nerc_pdf_parser.py <pdf_file>")
        print("Example: python nerc_pdf_parser.py cip-005-6.pdf")
