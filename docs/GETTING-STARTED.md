# Getting Started

Quick guide to install and use the NERC-CIP to OSCAL Toolkit.

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/chokmah-me/nerc-cip-oscal-jama.git
cd nerc-cip-oscal-jama
```

### 2. Set Up Python Environment
```bash
# Create virtual environment (optional)
python -m venv venv

# Activate environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install pytest
```

### 4. Verify Installation
```bash
pytest verify_oscal_compliance.py -v
# Expected: 27 passed
```

---

## First Steps

### Step 1: Validate the Dataset
```bash
pytest verify_oscal_compliance.py -v
```
This runs 27 compliance tests to verify the OSCAL dataset is production-ready.

**Expected Result:**
```
27 passed in 0.60s ✅
```

### Step 2: Review the Data
```bash
# View OSCAL structure
cat nerc-oscal.json | head -50

# Count requirements
python -c "import json; data = json.load(open('nerc-oscal.json')); \
           reqs = [c for g in data['catalog']['groups'] for c in g['controls'] \
                   if c.get('class')=='requirement']; print(f'{len(reqs)} requirements')"
```

### Step 3: Export to CSV
```bash
# Generate JAMA-compatible CSV
python oscal_to_jama_csv.py nerc-oscal.json --validate

# Result: nerc-oscal.csv (49 rows)
```

### Step 4: Review Documentation
- Dataset Structure: [OSCAL-DATASET-GUIDE.md](OSCAL-DATASET-GUIDE.md)
- Technical Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- Release Notes: [RELEASES.md](RELEASES.md)

---

## Common Tasks

### Validate the Dataset
```bash
pytest verify_oscal_compliance.py -v
```
Runs all 27 compliance tests.

### Run Specific Tests
```bash
# Test NIST mapping
pytest verify_oscal_compliance.py -k "nist" -v

# Test JAMA integration
pytest verify_oscal_compliance.py -k "jama" -v

# Test CSV export
pytest verify_oscal_compliance.py -k "csv" -v
```

### Export to JAMA
```bash
# Standard export
python oscal_to_jama_csv.py nerc-oscal.json

# With validation
python oscal_to_jama_csv.py nerc-oscal.json --validate

# Custom output file
python oscal_to_jama_csv.py nerc-oscal.json -o my-requirements.csv

# Detailed format (extra columns)
python oscal_to_jama_csv.py nerc-oscal.json --format detailed
```

### Regenerate OSCAL Dataset
```bash
# From source PDF files
python nerc_pdf_parser.py NERC-CIP/*.pdf -o nerc_raw_text/

# Extract requirements text
python extract_nerc_text.py nerc_raw_text/ -o nerc_all_combined.txt

# Generate OSCAL JSON
python generate_oscal.py nerc_all_combined.txt -o nerc-oscal.json

# Validate the output
pytest verify_oscal_compliance.py -v
```

---

## Understanding the Data

### OSCAL Structure
The toolkit generates OSCAL v1.0.0 in **Catalog** format:
```json
{
  "catalog": {
    "uuid": "...",
    "metadata": {...},
    "groups": [
      {
        "id": "cip-002-8",
        "controls": [
          {
            "id": "cip-002-8-r1",
            "class": "requirement",
            "title": "CIP-002-8 R1",
            "parts": [...],
            "props": [...]
          }
        ]
      }
    ]
  }
}
```

### CSV Format
The exported CSV includes:
- JAMA-Requirement-ID
- NERC-Requirement-ID
- NIST-Primary-Control
- NIST-Secondary-Controls
- Title
- Description
- Implementation-Status

See [OSCAL-DATASET-GUIDE.md](OSCAL-DATASET-GUIDE.md) for complete structure.

---

## Troubleshooting

### pytest not found
```bash
pip install pytest
pytest --version  # Verify
```

### Python version error
```bash
python --version  # Check version
# Requires Python 3.8+
```

### JSON parsing error
```bash
# Verify JSON is valid
python -c "import json; json.load(open('nerc-oscal.json'))"
```

### CSV export fails
```bash
# Check file exists
ls -la nerc-oscal.json

# Run with verbose output
python oscal_to_jama_csv.py nerc-oscal.json --validate
```

---

## Next Steps

1. **Review Dataset:** See [OSCAL-DATASET-GUIDE.md](OSCAL-DATASET-GUIDE.md)
2. **Understand Architecture:** See [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Check Version History:** See [RELEASES.md](RELEASES.md)
4. **Integrate with JAMA:** Export CSV and import into JAMA
5. **Deploy to GRC System:** Use nerc-oscal.json or CSV with ServiceNow, Tableau, etc.

---

## Support

- **Documentation:** See [README.md](../README.md)
- **Issues:** Check GitHub repository
- **Questions:** Refer to technical documentation in this directory

---

**Ready to use! All tests passing. Zero known issues.**
