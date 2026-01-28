# Ion Landscape Profile Ingestion Guide

This guide explains how to systematically ingest, verify, and classify trapped-ion research groups and PIs using authoritative online sources.

## Overview

The automated ingestion system follows strict rules to ensure data quality:

- ❌ **Do NOT hallucinate facts** - every claim must be backed by a source
- ❌ **Do NOT guess** ion species, advisors, or research focus
- ❌ **Do NOT overwrite** confirmed existing data
- ✅ **Every non-trivial fact must be backed by a source**

## Authoritative Sources (in order of trust)

1. Official group / lab websites
2. Official university faculty pages
3. CV PDFs hosted on institutional domains
4. AcademicTree Physics (as a lead, not final authority)
5. ORCID profiles
6. Google Scholar (for activity verification only)
7. Institutional thesis repositories (ORA, ProQuest, WorldCat)

**Note:** Wikipedia is NOT a primary source.

## Tools

### 1. Automated Ingestion Script

```bash
# Install dependencies first
pip install -r scripts/requirements.txt

# Run automated ingestion (dry-run mode)
python scripts/ingest_profiles.py --dry-run

# Process only first N entries
python scripts/ingest_profiles.py --dry-run --limit 10

# Actually make changes
python scripts/ingest_profiles.py
```

This script:
- Fetches the authoritative list from https://quantumoptics.at/en/links/ion-trapping-worldwide.html
- Matches entries against existing profiles
- Enriches existing profiles with verified data
- Creates logs in `scripts/logs/` with sources used

### 2. Profile Creation Template

For manually creating new profiles with verified data:

```bash
python scripts/create_profile_template.py
```

This interactive tool:
- Prompts for required information
- Validates input
- Only creates fields you can verify
- Generates proper YAML frontmatter

### 3. Profile Verification

Verify existing profiles against the schema:

```bash
# Verify single profile
python scripts/verify_profile_data.py 001-roee-ozeri

# Verify all profiles
python scripts/verify_profile_data.py --all
```

This checks:
- Required fields are present
- Field types match schema
- Links are accessible
- Classifications are valid

## Allowed Frontmatter Fields

You may ONLY modify these YAML frontmatter fields:

### Core Identity
- `group_type`: "experimental" or "theory"
- `labels`: ["Experimental group"] or ["Theory group"]
- `research_focus`: Array of up to 2 from:
  - quantum_computing
  - quantum_simulation
  - optical_clocks
  - metrology
  - quantum_networking
  - quantum_logic_spectroscopy
  - other

### Education (PhD block only)
```yaml
education:
  - degree: "PhD (Physics)"
    institution: string | null
    year: int | null
    advisor: string | null
    confidence: confirmed | academictree_only | not_found | ambiguous
    note: string | null
```

### Thesis
```yaml
thesis:
  title: string | null
  year: int | null
  link: string | null
  note: string | null  # Explain verification attempts
```

### Links
- `homepage`: Personal/group homepage
- `group_page`: University group page
- `google_scholar`: Google Scholar profile
- `orcid`: ORCID profile
- `institution_profile`: University profile page

### Activity Status
- `active`: true/false (true = recent publications or active group page in last ~5 years)

### Ion Species (OPTIONAL - high verification bar)
```yaml
ion_species:
  - Ca+
  - Yb+
```

**Only add if explicitly stated on group website, thesis, or multiple experimental papers.**

## Classification Rules

### Experimental vs Theory

**Experimental** if:
- Lab photos, apparatus, vacuum systems, lasers visible
- Students/postdocs listed
- Papers describe measurements or hardware

**Theory** if:
- No lab infrastructure visible
- Publications are analytical/numerical only

### Research Focus

Assign ONLY if clearly stated on:
- Group website
- Multiple recent publications
- Official bios

If mixed → choose dominant focus or use "other".

## Workflow for Each Person

1. **Extract** PI name + institution from source list
2. **Check** if Markdown file already exists in `content/people/`
3. **If exists:**
   - Verify PhD info against authoritative sources
   - Verify group type & focus
   - Add missing ORCID / links
   - Document sources used
4. **If does not exist:**
   - Use `create_profile_template.py` to create minimal profile
   - Fill ONLY verified fields
   - Add source citations
   - Flag any uncertain information
5. **Commit** with descriptive message: `data: verify & enrich profile — Name`

## Output Format

For each processed person, document:

### 1. Updated YAML frontmatter ONLY
(Do not modify prose unless instructed)

### 2. Sources used
```
Sources:
- https://tiqi.ethz.ch/people/person-detail.jhome.html
- https://academictree.org/physics/tree.php?pid=...
- https://orcid.org/0000-0002-4093-1550
```

## Example: Manual Profile Enhancement

Let's say you're enriching the profile for Jonathan P. Home:

1. **Check existing profile:**
   ```bash
   cat content/people/016-jonathan-home.md
   ```

2. **Research authoritative sources:**
   - Check https://www.phys.ethz.ch/the-department/people/person-detail.jhome.html
   - Look for thesis at Oxford: https://ora.ox.ac.uk/
   - Check ORCID for verified data

3. **Find verified information:**
   - Thesis title: "High Fidelity Operations for Quantum Information Processing with Trapped Ions" (from ORA)
   - Thesis year: 2006 (from ORA)
   - Advisor: Andrew Steane (confirmed on faculty page and thesis)

4. **Update profile:**
   ```yaml
   thesis:
     title: "High Fidelity Operations for Quantum Information Processing with Trapped Ions"
     year: 2006
     link: "https://ora.ox.ac.uk/objects/uuid:..."
     note: null
   
   education:
     - degree: "PhD (Physics)"
       institution: "University of Oxford"
       year: 2006
       advisor: "Andrew Steane"
       confidence: "confirmed"
       note: "Verified from Oxford ORA and department records"
   ```

5. **Commit with sources:**
   ```bash
   git add content/people/016-jonathan-home.md
   git commit -m "data: verify & enrich profile — Jonathan P. Home

   Sources:
   - https://ora.ox.ac.uk/objects/uuid:...
   - https://www.phys.ethz.ch/the-department/people/person-detail.jhome.html
   - https://orcid.org/0000-0002-4093-1550"
   ```

## Branch and PR Workflow

1. **Create branch:**
   ```bash
   git checkout -b auto/ionlandscape-ingestion
   ```

2. **Make changes:**
   - Process groups one by one
   - Commit after each person: `data: verify & enrich profile — Name`

3. **Open PR** summarizing:
   - Number of people updated
   - New people added
   - Entries requiring manual review
   - Sources used

## Stop Conditions

- Stop when all groups from the website have been evaluated
- Flag unresolved cases for human review instead of guessing
- Never proceed without verified sources

## Quality Checks

Before committing:

1. **Run verification:**
   ```bash
   python scripts/verify_profile_data.py <person-id>
   ```

2. **Test build:**
   ```bash
   python scripts/build_index.py
   ```

3. **Review changes:**
   ```bash
   git diff content/people/
   ```

## Troubleshooting

### Website not accessible
If the authoritative website is not accessible:
1. Manually download the HTML
2. Place in `scripts/data/ion-trapping-worldwide.html`
3. Modify `ingest_profiles.py` to read from local file

### Cannot verify information
If you cannot verify a field:
- Leave it as `null`
- Add a `note` field explaining what was attempted
- Flag for manual review

Example:
```yaml
thesis:
  title: null
  year: null
  link: null
  note: "Thesis title/PDF not found in Oxford ORA or WorldCat; may require direct request"
```

### Conflicting sources
If sources disagree:
- Use the most authoritative source (see source hierarchy above)
- Add a note explaining the discrepancy
- Set confidence level appropriately

## Goal State

When complete, the repository should be:
- ✅ Source-verifiable (every fact backed by documented source)
- ✅ Consistent (following schema and conventions)
- ✅ Clearly classified (experimental/theory, research focus)
- ✅ Ready for public browsing and expansion

## Logs and Reports

All automation generates logs in `scripts/logs/`:
- `ingestion_TIMESTAMP.log` - Processing log
- `sources_TIMESTAMP.json` - Source tracking per person

These should be reviewed and archived for transparency.
