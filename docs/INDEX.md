# Documentation Index

Complete guide to all documentation in the NERC-CIP to OSCAL Toolkit.

---

## Quick Links

### Getting Started
- **New Users:** [GETTING-STARTED.md](GETTING-STARTED.md)
- **Installation Guide:** [GETTING-STARTED.md#installation](GETTING-STARTED.md#installation)
- **First Steps:** [GETTING-STARTED.md#first-steps](GETTING-STARTED.md#first-steps)

### Core Documentation
- **Main README:** [../README.md](../README.md)
- **Technical Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Dataset Guide:** [OSCAL-DATASET-GUIDE.md](OSCAL-DATASET-GUIDE.md)
- **Release History:** [RELEASES.md](RELEASES.md)

### Additional Resources
- **Schema Fix Details:** [SCHEMA-FIX-SUMMARY.md](SCHEMA-FIX-SUMMARY.md)
- **Verification Report:** [VERIFICATION-COMPLETE.md](VERIFICATION-COMPLETE.md)

---

## Documentation by Role

### For Users / Compliance Teams

Start here if you want to:
- Use the dataset for compliance work
- Export to JAMA or other GRC systems
- Validate the dataset

**Recommended Reading:**
1. [../README.md](../README.md) - Overview
2. [GETTING-STARTED.md](GETTING-STARTED.md) - Installation
3. [OSCAL-DATASET-GUIDE.md](OSCAL-DATASET-GUIDE.md) - Understanding the data

### For Developers

Start here if you want to:
- Understand the architecture
- Regenerate the dataset
- Extend or modify the tools

**Recommended Reading:**
1. [ARCHITECTURE.md](ARCHITECTURE.md) - System design
2. [GETTING-STARTED.md#regenerate-oscal-dataset](GETTING-STARTED.md) - Data generation
3. [../CLAUDE.md](../CLAUDE.md) - Development workflows

### For GRC Engineers

Start here if you want to:
- Integrate with enterprise systems
- Export data to JAMA/ServiceNow/Tableau
- Map requirements to controls

**Recommended Reading:**
1. [GETTING-STARTED.md](GETTING-STARTED.md) - Quick setup
2. [OSCAL-DATASET-GUIDE.md](OSCAL-DATASET-GUIDE.md) - Data structure
3. [RELEASES.md](RELEASES.md) - Version information

### For Project Managers / Decision Makers

Start here if you want to:
- Understand project status
- Review verification results
- Check production readiness

**Recommended Reading:**
1. [../README.md](../README.md) - Executive summary
2. [VERIFICATION-COMPLETE.md](VERIFICATION-COMPLETE.md) - Quality assurance
3. [RELEASES.md](RELEASES.md) - Version history

### For Security/Compliance Auditors

Start here if you want to:
- Verify data quality
- Review requirements traceability
- Check against standards

**Recommended Reading:**
1. [VERIFICATION-COMPLETE.md](VERIFICATION-COMPLETE.md) - Full verification
2. [OSCAL-DATASET-GUIDE.md](OSCAL-DATASET-GUIDE.md) - Data structure
3. [ARCHITECTURE.md](ARCHITECTURE.md) - Processing methodology

---

## Document Overview

### [README.md](../README.md)
**Location:** Repository root
**Length:** 200 lines
**Purpose:** Quick overview and entry point

**Contains:**
- Project description
- Quick start commands
- Feature highlights
- Requirements coverage table
- Use case examples
- Links to detailed documentation

### [GETTING-STARTED.md](GETTING-STARTED.md)
**Location:** docs/
**Length:** 200 lines
**Purpose:** Installation and first use guide

**Contains:**
- Installation steps
- Setup verification
- Common tasks
- Data structure overview
- Troubleshooting
- Next steps

### [ARCHITECTURE.md](ARCHITECTURE.md)
**Location:** docs/
**Length:** 400 lines
**Purpose:** Technical system design

**Contains:**
- System overview diagram
- Component descriptions
- Data flow
- Schema design
- Performance metrics
- Error handling
- Development workflows
- Integration points

### [RELEASES.md](RELEASES.md)
**Location:** docs/
**Length:** 350 lines
**Purpose:** Version history and release notes

**Contains:**
- v1.1.1 release notes
- v1.1.0 release notes
- v1.0.0 archive
- Version comparison
- Migration guide
- Breaking changes
- Upcoming features
- Changelog

### [OSCAL-DATASET-GUIDE.md](OSCAL-DATASET-GUIDE.md)
**Location:** docs/
**Length:** 530 lines
**Purpose:** Complete dataset structure reference

**Contains:**
- Dataset overview
- OSCAL structure details
- Component definitions
- Property descriptions
- Query examples
- Integration patterns
- Troubleshooting
- References

### [SCHEMA-FIX-SUMMARY.md](SCHEMA-FIX-SUMMARY.md)
**Location:** docs/
**Length:** 120 lines
**Purpose:** Technical details of v1.1.1 schema fix

**Contains:**
- Problem description
- Solution approach
- Code changes
- Results before/after
- Verification results
- Deployment status

### [VERIFICATION-COMPLETE.md](VERIFICATION-COMPLETE.md)
**Location:** docs/
**Length:** 800+ lines
**Purpose:** Complete verification and validation report

**Contains:**
- Executive summary
- Claim-by-claim verification
- Test results
- Data quality metrics
- GRC integration status
- Quality assurance details
- Technical appendix

---

## Documentation Statistics

| Document | Lines | Size | Purpose |
|----------|-------|------|---------|
| README.md | 200 | 6 KB | Quick overview |
| GETTING-STARTED.md | 200 | 4.4 KB | Installation guide |
| ARCHITECTURE.md | 400 | 10 KB | Technical design |
| RELEASES.md | 350 | 7.2 KB | Version history |
| OSCAL-DATASET-GUIDE.md | 530 | 13.3 KB | Dataset reference |
| SCHEMA-FIX-SUMMARY.md | 120 | 3.7 KB | Technical fix |
| VERIFICATION-COMPLETE.md | 800+ | 15.8 KB | Verification report |
| **TOTAL** | **2,600+** | **60+ KB** | Complete documentation |

---

## Navigation Tips

### Finding Specific Information

**For quick answers:**
- README.md Quick Start section
- GETTING-STARTED.md Common Tasks section

**For detailed info:**
- ARCHITECTURE.md for how things work
- OSCAL-DATASET-GUIDE.md for data structure
- VERIFICATION-COMPLETE.md for quality assurance

**For release info:**
- RELEASES.md for version history
- SCHEMA-FIX-SUMMARY.md for v1.1.1 details

**For troubleshooting:**
- GETTING-STARTED.md Troubleshooting section
- ARCHITECTURE.md Error Handling section
- OSCAL-DATASET-GUIDE.md Troubleshooting section

### Cross-References

Documents link to each other for easy navigation:
- README.md → Links to all detailed docs
- GETTING-STARTED.md → Links to architecture and dataset guide
- ARCHITECTURE.md → Links to component details
- RELEASES.md → Links to current documentation
- Each doc has footer links to related content

---

## Document Map

```
Repository Root
├── README.md (200 lines) - Quick overview
├── CLAUDE.md (400 lines) - Development guide
├── NERC-CIP/ (29 PDFs) - Source documents
├── nerc_raw_text/ (30 files) - Extracted text
├── nerc-oscal.json (OSCAL data)
├── nerc-oscal.csv (JAMA export)
└── docs/ (Documentation)
    ├── INDEX.md (this file)
    ├── GETTING-STARTED.md (200 lines)
    ├── ARCHITECTURE.md (400 lines)
    ├── RELEASES.md (350 lines)
    ├── OSCAL-DATASET-GUIDE.md (530 lines)
    ├── SCHEMA-FIX-SUMMARY.md (120 lines)
    └── VERIFICATION-COMPLETE.md (800+ lines)
```

---

## Recommended Reading Order

### First Time Users
1. [README.md](../README.md) - 5 minutes
2. [GETTING-STARTED.md](GETTING-STARTED.md) - 10 minutes
3. [OSCAL-DATASET-GUIDE.md](OSCAL-DATASET-GUIDE.md) - 15 minutes

### Developers
1. [README.md](../README.md) - 5 minutes
2. [ARCHITECTURE.md](ARCHITECTURE.md) - 20 minutes
3. [../CLAUDE.md](../CLAUDE.md) - 15 minutes

### Enterprise Teams
1. [README.md](../README.md) - 5 minutes
2. [VERIFICATION-COMPLETE.md](VERIFICATION-COMPLETE.md) - 20 minutes
3. [RELEASES.md](RELEASES.md) - 10 minutes

### Compliance Auditors
1. [VERIFICATION-COMPLETE.md](VERIFICATION-COMPLETE.md) - 30 minutes
2. [OSCAL-DATASET-GUIDE.md](OSCAL-DATASET-GUIDE.md) - 20 minutes
3. [ARCHITECTURE.md](ARCHITECTURE.md) - 15 minutes

---

## Search Tips

**Looking for:**
- Installation steps? → GETTING-STARTED.md
- Data structure? → OSCAL-DATASET-GUIDE.md
- How it works? → ARCHITECTURE.md
- Version info? → RELEASES.md
- Quality assurance? → VERIFICATION-COMPLETE.md
- Bug fixes? → SCHEMA-FIX-SUMMARY.md

---

## Keeping Documentation Current

Last Updated: January 25, 2026
Version: v1.1.1

All documentation has been verified and updated for v1.1.1 release.

---

**Complete, organized, and ready to use.** 📚
