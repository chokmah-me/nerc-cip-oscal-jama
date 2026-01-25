import re
import json
import uuid
from datetime import datetime

# CONFIGURATION
INPUT_FILE = "nerc_all_combined.txt"
OUTPUT_FILE = "nerc-oscal.json"

def clean_text(text):
    """
    Cleans up PDF artifacts.
    """
    # Remove "Page X of Y" lines
    text = re.sub(r"Page \d+ of \d+", "", text)
    # Remove lines that are just the document title repeated (common header artifact)
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if "CIP-" in line and " — " in line: # rough check for header repetition
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip()

def parse_requirements_state_machine(req_block):
    """
    Iterates line by line to capture Requirements (R) and ignore Measures (M).
    Robust against weird spacing and formatting.
    """
    requirements = []
    lines = req_block.split('\n')
    
    current_req_id = None
    current_req_text = []
    
    # Regex to detect start of a requirement (e.g., "R1.", "R10.")
    # We look for start of line or small whitespace indent
    req_start_pattern = re.compile(r"^\s*(R\d+)\.")
    # Regex to detect start of a measure (e.g., "M1.", "M10.") - Signals stop
    measure_start_pattern = re.compile(r"^\s*(M\d+)\.")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check for new Requirement start
        req_match = req_start_pattern.match(line)
        if req_match:
            # If we were building a requirement, save it
            if current_req_id:
                requirements.append({
                    "id": current_req_id,
                    "text": " ".join(current_req_text).strip()
                })
            
            # Start new requirement
            current_req_id = req_match.group(1) # e.g., "R1"
            # Remove the "R1." from the text start
            clean_line = line[len(req_match.group(0)):].strip()
            current_req_text = [clean_line]
            continue

        # Check for Measure start (Stop capturing)
        measure_match = measure_start_pattern.match(line)
        if measure_match:
            # If we were building a requirement, save it and stop capturing
            if current_req_id:
                requirements.append({
                    "id": current_req_id,
                    "text": " ".join(current_req_text).strip()
                })
                current_req_id = None # Reset
                current_req_text = []
            continue

        # If we are inside a requirement, append the line
        if current_req_id:
            current_req_text.append(line)

    # Catch the last one if file ended
    if current_req_id and current_req_text:
        requirements.append({
            "id": current_req_id,
            "text": " ".join(current_req_text).strip()
        })

    return requirements

def parse_nerc_standards(text):
    raw_docs = text.split("--- START DOCUMENT:")
    standards = {}

    print(f"🔍 Analyzing {len(raw_docs)} documents...")

    for doc in raw_docs:
        if not doc.strip(): continue

        # 1. Identify CIP Number
        match = re.search(r"(CIP-\d{3}-\d+[a-z]?)", doc)
        if not match: continue
        
        full_cip_id = match.group(1)
        cip_family = full_cip_id.split('-')[1]
        version_str = full_cip_id.split('-')[2]
        version_num = float(re.sub(r'[a-zA-Z]', '', version_str))

        # 2. Metadata
        title_match = re.search(r"Title:\s*(.+)", doc)
        title = title_match.group(1).strip() if title_match else "Unknown Title"

        purpose_match = re.search(r"Purpose:\s*(.+?)(?=\n\s*4\.)", doc, re.DOTALL)
        purpose = purpose_match.group(1).replace('\n', ' ').strip() if purpose_match else "No purpose defined."
        purpose = re.sub(r"Page \d+ of \d+", "", purpose)

        # 3. Extract Requirement Block
        # Grab text between "B. Requirements" and "C. Compliance" (or VSL table)
        req_section_match = re.search(
            r"B\.\s*Requirements and Measures(.*?)(?=C\.\s*Compliance|Violation Severity Levels)", 
            doc, 
            re.DOTALL
        )
        
        reqs = []
        if req_section_match:
            raw_req_block = req_section_match.group(1)
            # Clean page numbers BEFORE processing logic
            clean_block = re.sub(r"Page \d+ of \d+", "", raw_req_block)
            reqs = parse_requirements_state_machine(clean_block)

        standard_obj = {
            "id": full_cip_id,
            "family": cip_family,
            "version": version_num,
            "original_version_string": version_str,
            "title": title,
            "purpose": purpose,
            "requirements": reqs
        }

        # 4. Deduplication
        if cip_family in standards:
            if version_num > standards[cip_family]['version']:
                print(f"   🔄 Upgrading CIP-{cip_family} from v{standards[cip_family]['original_version_string']} to v{version_str}")
                standards[cip_family] = standard_obj
        else:
            standards[cip_family] = standard_obj
            print(f"   ✅ Found: {full_cip_id}")

    return standards

def generate_oscal_catalog(standards):
    catalog = {
        "catalog": {
            "uuid": str(uuid.uuid4()),
            "metadata": {
                "title": "NERC CIP OSCAL Catalog",
                "last-modified": datetime.now().isoformat(),
                "version": "1.1.0",
                "oscal-version": "1.0.0",
                "notes": "Generated with NovaKit v3 State Machine Logic."
            },
            "groups": []
        }
    }

    for family in sorted(standards.keys()):
        std = standards[family]
        group = {
            "id": std['id'].lower(),
            "class": "standard",
            "title": f"{std['id']} - {std['title']}",
            "controls": [
                {
                    "id": f"{std['id'].lower()}-purpose",
                    "class": "purpose",
                    "title": "Purpose",
                    "parts": [{"id": f"{std['id'].lower()}-purpose-smt", "name": "statement", "prose": std['purpose']}]
                }
            ]
        }

        for req in std['requirements']:
            group['controls'].append({
                "id": f"{std['id'].lower()}-{req['id'].lower()}",
                "class": "requirement",
                "title": f"{std['id']} {req['id']}",
                "parts": [{"id": f"{std['id'].lower()}-{req['id'].lower()}-smt", "name": "statement", "prose": req['text']}],
                "props": [{"name": "label", "value": req['id']}, {"name": "status", "value": "active"}]
            })

        catalog['catalog']['groups'].append(group)

    return catalog

if __name__ == "__main__":
    print("🚀 Phase 3.5 (State Machine): Generating OSCAL...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            text = f.read()
        data = parse_nerc_standards(text)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(generate_oscal_catalog(data), f, indent=2)
        print(f"\n✨ DONE. Validated OSCAL catalog saved to: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Error: {e}")
