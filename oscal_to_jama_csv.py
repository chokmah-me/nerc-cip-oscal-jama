"""
Convert OSCAL Component Definition JSON to JAMA-compatible CSV traceability matrix.

This utility exports OSCAL JSON component definitions to a CSV format suitable
for import into JAMA Software's Requirements and Traceability management system.

Usage:
    python oscal_to_jama_csv.py nerc-oscal.json
    python oscal_to_jama_csv.py nerc-oscal.json --output custom-matrix.csv
    python oscal_to_jama_csv.py nerc-oscal.json --format detailed

The generated CSV includes:
- JAMA-Requirement-ID: Unique ID for JAMA import (e.g., CIP-005-R1-a)
- NERC-Requirement-ID: Source NERC requirement (e.g., CIP-005-6 R1)
- NIST-Primary-Control: Primary NIST 800-53 control (e.g., SC-7)
- NIST-Secondary-Controls: Comma-separated secondary controls (e.g., CA-3, PL-2)
- Title: Component title
- Description: Component description
- Implementation-Status: Current status (Draft, Implemented, etc.)
"""

import json
import csv
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional


def load_oscal_json(oscal_file: Path) -> dict:
    """
    Load and validate OSCAL JSON file.

    Args:
        oscal_file: Path to OSCAL JSON file

    Returns:
        Parsed OSCAL data

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    if not oscal_file.exists():
        raise FileNotFoundError(f"OSCAL file not found: {oscal_file}")

    with open(oscal_file, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in {oscal_file}: {e.msg}", e.doc, e.pos)


def _extract_components_from_oscal(oscal_data: dict) -> List[dict]:
    """
    Extract components from OSCAL data (handles both catalog and component-definition schemas).

    Catalog format: groups[].controls[] where class='requirement' becomes components
    Component-definition format: components[]

    Args:
        oscal_data: Parsed OSCAL JSON data

    Returns:
        List of component-like objects
    """
    # Try component-definition first
    comp_def = oscal_data.get('component-definition', {})
    if comp_def and 'components' in comp_def:
        return comp_def.get('components', [])

    # Fall back to catalog format
    catalog = oscal_data.get('catalog', {})
    if catalog and 'groups' in catalog:
        components = []
        for group in catalog.get('groups', []):
            # Each requirement control becomes a component
            for control in group.get('controls', []):
                if control.get('class') == 'requirement':
                    # Extract prose/description from parts
                    description = ''
                    parts = control.get('parts', [])
                    if parts and isinstance(parts[0], dict):
                        description = parts[0].get('prose', '')

                    # Convert control to component-like structure
                    component = {
                        'id': control.get('id', ''),
                        'title': control.get('title', ''),
                        'uuid': str(__import__('uuid').uuid4()),  # Generate since catalog doesn't have it
                        'description': description,
                        'properties': control.get('props', []) or [],
                        'group_id': group.get('id', '')
                    }
                    components.append(component)
        return components

    return []


def extract_component_properties(component: dict) -> Dict[str, str]:
    """
    Extract named properties from OSCAL component as dict.

    Args:
        component: OSCAL component object

    Returns:
        Dictionary mapping property names to values
    """
    props = {}
    for prop in component.get('properties', []):
        if isinstance(prop, dict):
            name = prop.get('name', '')
            value = prop.get('value', '')
            props[name] = value

    return props


def normalize_control_id(control_id: str) -> str:
    """
    Normalize NIST control ID to standard format.

    Args:
        control_id: Control ID (e.g., 'SC-7', 'sc-7')

    Returns:
        Normalized control ID (e.g., 'SC-7')
    """
    if not control_id:
        return ''

    return control_id.strip().upper()


def oscal_to_jama_csv(oscal_file: Path, output_csv: Optional[Path] = None,
                       format_type: str = 'standard') -> List[Dict[str, str]]:
    """
    Convert OSCAL (Catalog or Component Definition) to JAMA CSV format.

    Args:
        oscal_file: Path to input OSCAL JSON file
        output_csv: Path to output CSV file (if None, derives from oscal_file)
        format_type: CSV format ('standard' or 'detailed')

    Returns:
        List of CSV row dictionaries
    """
    # Load OSCAL JSON
    oscal_data = load_oscal_json(oscal_file)

    # Extract components from either schema
    components = _extract_components_from_oscal(oscal_data)

    if not components:
        raise ValueError("OSCAL JSON has no requirements/components to export")

    # Build CSV rows
    rows = []

    for component in components:
        # Extract properties
        props = extract_component_properties(component)

        # Build base row
        row = {
            'JAMA-Requirement-ID': props.get('JAMA-Requirement-ID', ''),
            'NERC-Requirement-ID': props.get('NERC-Requirement-ID', ''),
            'NIST-Primary-Control': normalize_control_id(props.get('NIST-800-53-Primary-Control', '')),
            'NIST-Secondary-Controls': props.get('NIST-800-53-Secondary-Controls', ''),
            'Title': component.get('title', ''),
            'Description': component.get('description', ''),
            'Implementation-Status': props.get('Implementation-Status', 'Draft'),
        }

        # Add detailed fields if requested
        if format_type == 'detailed':
            row.update({
                'Component-UUID': component.get('uuid', ''),
                'Component-Type': component.get('type', 'software'),
                'Control-Count': str(len(component.get('control-implementations', []))),
            })

        rows.append(row)

    # Determine output path
    if output_csv is None:
        output_csv = oscal_file.with_suffix('.csv')

    # Write CSV
    if rows:
        fieldnames = list(rows[0].keys())
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)

        print(f"[OK] Successfully exported {len(rows)} components to {output_csv}")
    else:
        print("[WARN] No components to export")

    return rows


def validate_csv_format(csv_file: Path) -> bool:
    """
    Validate that CSV file has expected JAMA format.

    Args:
        csv_file: Path to CSV file to validate

    Returns:
        True if valid, False otherwise
    """
    required_columns = [
        'JAMA-Requirement-ID',
        'NERC-Requirement-ID',
        'NIST-Primary-Control',
        'Title',
        'Description'
    ]

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Check headers
            if reader.fieldnames is None:
                print("[ERR] CSV file is empty")
                return False

            missing_columns = set(required_columns) - set(reader.fieldnames)
            if missing_columns:
                print(f"[ERR] CSV missing required columns: {missing_columns}")
                return False

            # Check data
            row_count = 0
            for row in reader:
                row_count += 1

                # Validate non-empty JAMA IDs
                if not row.get('JAMA-Requirement-ID', '').strip():
                    print(f"[ERR] Row {row_count}: Empty JAMA-Requirement-ID")
                    return False

                # Validate non-empty NERC IDs
                if not row.get('NERC-Requirement-ID', '').strip():
                    print(f"[ERR] Row {row_count}: Empty NERC-Requirement-ID")
                    return False

            if row_count == 0:
                print("[ERR] CSV file has no data rows")
                return False

            print(f"[OK] CSV validation passed ({row_count} rows)")
            return True

    except Exception as e:
        print(f"[ERR] Error validating CSV: {e}")
        return False


def main():
    """Command-line interface for OSCAL to JAMA CSV conversion."""
    parser = argparse.ArgumentParser(
        description='Convert OSCAL Component Definition JSON to JAMA CSV traceability matrix',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s nerc-oscal.json
  %(prog)s nerc-oscal.json --output my-matrix.csv
  %(prog)s nerc-oscal.json --format detailed
  %(prog)s nerc-oscal.json --validate
        """
    )

    parser.add_argument(
        'oscal_file',
        type=Path,
        help='Path to OSCAL Component Definition JSON file'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output CSV file path (default: <oscal_file>.csv)'
    )

    parser.add_argument(
        '--format',
        choices=['standard', 'detailed'],
        default='standard',
        help='CSV format: standard (basic fields) or detailed (with metadata)'
    )

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate output CSV file after export'
    )

    args = parser.parse_args()

    try:
        # Convert OSCAL to CSV
        rows = oscal_to_jama_csv(args.oscal_file, args.output, args.format)

        # Validate if requested
        if args.validate:
            output_path = args.output or args.oscal_file.with_suffix('.csv')
            if validate_csv_format(output_path):
                print(f"[OK] JAMA export is valid and ready for import")
            else:
                print(f"[WARN] CSV validation found issues")
                sys.exit(1)

    except FileNotFoundError as e:
        print(f"[ERR] Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERR] JSON parsing error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"[ERR] Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERR] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
