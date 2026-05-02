# Complete Example: Enriching a Profile with Sources

This example demonstrates the complete workflow for enriching Jonathan Home's profile with verified data from authoritative sources.

## Step 1: Research Phase

### Sources Found:
1. **ETH Zurich Faculty Page**
   - URL: https://www.phys.ethz.ch/the-department/people/person-detail.jhome.html
   - Contains: Current position, contact, research overview

2. **Group Website**
   - URL: https://iqe.phys.ethz.ch/research/trapped-ion-quantum-information.html
   - Contains: Research focus, group members, ion species (Ca+)

3. **Oxford University Research Archive (ORA)**
   - URL: https://ora.ox.ac.uk/objects/uuid:xxxx
   - Contains: PhD thesis title, year (2006), advisor (Andrew Steane)

4. **ORCID Profile**
   - URL: https://orcid.org/0000-0002-4093-1550
   - Contains: Publications, affiliations (self-reported)

5. **Google Scholar**
   - URL: https://scholar.google.com/citations?user=hIVXn-EAAAAJ
   - Contains: Publication list, citation metrics, recent activity

## Step 2: Document Sources with Citation Tool

```bash
# Start citation tracking
python scripts/cite_sources.py 016-jonathan-home --add

# Interactive prompts:
# Field: education[0].advisor
# URL: https://ora.ox.ac.uk/objects/uuid:xxxx
# Note: Verified from thesis PDF title page

# Field: education[0].institution
# URL: https://ora.ox.ac.uk/objects/uuid:xxxx
# Note: Verified from thesis metadata

# Field: thesis.title
# URL: https://ora.ox.ac.uk/objects/uuid:xxxx
# Note: Full title from ORA

# Field: links.homepage
# URL: https://iqe.phys.ethz.ch/research/trapped-ion-quantum-information.html
# Note: Current group website

# Field: ion_species
# URL: https://iqe.phys.ethz.ch/research/trapped-ion-quantum-information.html
# Note: Explicitly stated on group website
```

## Step 3: Update Profile Manually

Edit `content/people/016-jonathan-home.md`:

```yaml
---
# ... existing fields ...

education:
  - degree: "PhD (Physics)"
    institution: "University of Oxford"
    year: 2006
    advisor: "Andrew Steane"
    confidence: "confirmed"  # CHANGED from null
    note: null

thesis:
  title: "High Fidelity Operations for Quantum Information Processing with Trapped Ions"  # ADDED
  year: 2006  # ADDED
  link: "https://ora.ox.ac.uk/objects/uuid:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"  # ADDED
  note: null

ion_species:  # ADDED
  - Ca+

research_focus:  # ADDED
  - quantum_computing

links:
  homepage: "https://iqe.phys.ethz.ch/research/trapped-ion-quantum-information.html"  # UPDATED
  group_page: "https://www.phys.ethz.ch/the-department/people/person-detail.jhome.html"
  google_scholar: "https://scholar.google.com/citations?user=hIVXn-EAAAAJ&hl=en"
  orcid: "https://orcid.org/0000-0002-4093-1550"
  eth_profile: "https://www.phys.ethz.ch/the-department/people/person-detail.jhome.html"

updated_at: '2026-01-28'  # UPDATED
---
```

## Step 4: Verify Changes

```bash
# Validate the profile
python scripts/verify_profile_data.py 016-jonathan-home

# Expected output:
# ================================================================================
# Verifying: Jonathan P. Home (016-jonathan-home)
# ================================================================================
# 
# Checks passed:
#   ✓ Has id
#   ✓ Has name
#   ✓ Has current_position
#   ✓ Has location
#   ✓ Has group_type
#   ✓ education[0] has all fields
#   ✓ thesis has title and link
# 
# ✅ All checks passed!
```

## Step 5: Generate Commit Message

```bash
# Generate commit message with sources
python scripts/cite_sources.py 016-jonathan-home --commit-msg --name "Jonathan P. Home"

# Output (automatically copied to clipboard if pyperclip available):
```

```
data: verify & enrich profile — Jonathan P. Home

Updated fields:
- education[0].advisor
- education[0].confidence
- ion_species
- links.homepage
- research_focus
- thesis.link
- thesis.title
- thesis.year

Sources:
- https://iqe.phys.ethz.ch/research/trapped-ion-quantum-information.html
- https://ora.ox.ac.uk/objects/uuid:xxxx
- https://orcid.org/0000-0002-4093-1550
- https://www.phys.ethz.ch/the-department/people/person-detail.jhome.html

Notes:
- education[0].advisor: Verified from thesis PDF title page
- ion_species: Explicitly stated on group website
- thesis.title: Full title from Oxford Research Archive
```

## Step 6: Commit Changes

```bash
# Stage the change
git add content/people/016-jonathan-home.md

# Commit with the generated message
git commit -m "data: verify & enrich profile — Jonathan P. Home

Updated fields:
- education[0].advisor
- education[0].confidence
- ion_species
- links.homepage
- research_focus
- thesis.link
- thesis.title
- thesis.year

Sources:
- https://iqe.phys.ethz.ch/research/trapped-ion-quantum-information.html
- https://ora.ox.ac.uk/objects/uuid:xxxx
- https://orcid.org/0000-0002-4093-1550
- https://www.phys.ethz.ch/the-department/people/person-detail.jhome.html

Notes:
- education[0].advisor: Verified from thesis PDF title page
- ion_species: Explicitly stated on group website
- thesis.title: Full title from Oxford Research Archive"

# Push to branch
git push origin auto/ionlandscape-ingestion
```

## Step 7: Quality Check

```bash
# Verify build still works
python scripts/build_index.py

# Expected output:
# Wrote: /path/to/website/static/data/people.json
# Wrote: /path/to/website/static/data/people.geojson
# Wrote: /path/to/website/static/data/edges.csv

# Check the generated data
jq '.[] | select(.id == "016-jonathan-home")' website/static/data/people.json

# Verify education edge was created for advisor
grep "andrew-steane,016-jonathan-home,advisor" website/static/data/edges.csv
```

## Alternative: Using Batch Enrichment

For the same update, you could use the batch enrichment tool:

### Create JSON file:

`scripts/data/home_update.json`:
```json
[
  {
    "name": "Jonathan P. Home",
    "institution": "ETH Zürich",
    "homepage": "https://iqe.phys.ethz.ch/research/trapped-ion-quantum-information.html",
    "group_page": "https://www.phys.ethz.ch/the-department/people/person-detail.jhome.html",
    "verified_sources": [
      "https://www.phys.ethz.ch/the-department/people/person-detail.jhome.html",
      "https://iqe.phys.ethz.ch/research/trapped-ion-quantum-information.html",
      "https://ora.ox.ac.uk/objects/uuid:xxxx",
      "https://orcid.org/0000-0002-4093-1550"
    ]
  }
]
```

### Run batch update:

```bash
# Dry run first
python scripts/batch_enrich_profiles.py scripts/data/home_update.json --dry-run

# Apply changes
python scripts/batch_enrich_profiles.py scripts/data/home_update.json

# Commit
git add content/people/016-jonathan-home.md
git commit -m "data: update links for Jonathan P. Home

Sources documented in scripts/data/home_update.json"
```

## Lessons Learned

### ✅ Do's:
1. **Research first** - Gather all sources before editing
2. **Document sources** - Use citation tool or JSON files
3. **Verify everything** - Run validation before committing
4. **Small changes** - One person at a time for clarity
5. **Test build** - Ensure data generation still works

### ❌ Don'ts:
1. **Don't guess** - If uncertain, leave as `null` with note
2. **Don't use Wikipedia** - Not a primary source
3. **Don't trust single source** - Verify from multiple sources when possible
4. **Don't skip verification** - Always run verify script
5. **Don't batch too many** - Process in small batches for easier debugging

## Common Verification Patterns

### Pattern 1: Thesis from Institutional Repository

```yaml
thesis:
  title: "Full Thesis Title"
  year: 2006
  link: "https://repository.university.edu/..."
  note: null

education:
  - degree: "PhD (Physics)"
    advisor: "Advisor Name"  # From thesis title page
    confidence: "confirmed"
    note: "Verified from institutional repository"
```

### Pattern 2: Advisor from AcademicTree Only

```yaml
education:
  - degree: "PhD (Physics)"
    advisor: "Advisor Name"
    confidence: "academictree_only"
    note: "Found on AcademicTree; not independently verified"
```

### Pattern 3: Missing Thesis

```yaml
thesis:
  title: null
  year: 2006  # If year known from CV
  link: null
  note: "Thesis not available in Oxford ORA; may require direct library request"
```

### Pattern 4: Ion Species from Papers

```yaml
ion_species:
  - Ca+
  - Sr+

# Only add if MULTIPLE recent papers use these ions
# Source in commit: "https://doi.org/... and https://doi.org/..."
```

## Timeline Estimate

For one profile with good sources available:
- Research: 15-30 minutes
- Documentation: 5-10 minutes
- Editing: 5-10 minutes
- Verification: 2-3 minutes
- Commit: 2-3 minutes

**Total: 30-60 minutes per profile**

Budget more time for:
- Hard-to-find sources
- Ambiguous information
- First few profiles (learning curve)

## Summary

This example shows:
- ✅ Proper source documentation
- ✅ Appropriate confidence levels
- ✅ Verification before commit
- ✅ Clear commit messages
- ✅ Incremental, traceable changes

Follow this pattern for consistent, high-quality profile enrichment.
