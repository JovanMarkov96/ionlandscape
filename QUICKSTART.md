# Quick Start: Profile Ingestion Workflow

This guide demonstrates a typical workflow for ingesting and verifying profiles.

## Initial Setup

```bash
# Clone the repository (if not already done)
git clone https://github.com/JovanMarkov96/ionlandscape.git
cd ionlandscape

# Install Python dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r scripts/requirements.txt

# Create a working branch
git checkout -b auto/ionlandscape-ingestion
```

## Workflow 1: Automated Ingestion (when website is accessible)

```bash
# Dry run first to see what would change
python scripts/ingest_profiles.py --dry-run --limit 10

# Review the logs
cat scripts/logs/ingestion_*.log

# Run for real (start with a small limit)
python scripts/ingest_profiles.py --limit 5

# Verify the changes
python scripts/verify_profile_data.py --all

# Commit and push
git add content/people/
git commit -m "data: automated ingestion - batch 1"
git push origin auto/ionlandscape-ingestion
```

## Workflow 2: Manual Enrichment with JSON Data

When the authoritative website is not accessible, or you have data from other sources:

### Step 1: Create a JSON file with verified data

Create `scripts/data/my_enrichment_data.json`:

```json
[
  {
    "name": "PI Name",
    "institution": "University Name",
    "homepage": "https://verified-url.edu",
    "country": "Country",
    "verified_sources": [
      "https://source1.edu/faculty/pi-name",
      "https://orcid.org/0000-..."
    ]
  }
]
```

### Step 2: Run batch enrichment

```bash
# Dry run to preview
python scripts/batch_enrich_profiles.py scripts/data/my_enrichment_data.json --dry-run

# Apply changes
python scripts/batch_enrich_profiles.py scripts/data/my_enrichment_data.json

# Verify
python scripts/verify_profile_data.py --all
```

### Step 3: Commit with sources

```bash
git add content/people/
git commit -m "data: enrich profiles with verified metadata

Sources documented in scripts/data/my_enrichment_data.json"
git push origin auto/ionlandscape-ingestion
```

## Workflow 3: Creating a New Profile

### Interactive Method

```bash
python scripts/create_profile_template.py
```

Follow the prompts, filling only verified information. The tool will:
- Generate a proper ID
- Validate required fields
- Create minimal frontmatter
- Save to `content/people/`

### Manual Method

1. Copy an existing profile as template
2. Update all fields with verified data
3. Remove or set to `null` any fields you cannot verify
4. Add a `note` field explaining verification attempts

Example:
```yaml
thesis:
  title: null
  year: null
  link: null
  note: "Attempted to find in Oxford ORA and ProQuest; not publicly available"
```

## Verification Checklist

Before committing any profile changes:

```bash
# 1. Verify the specific profile
python scripts/verify_profile_data.py <person-id>

# 2. Ensure build still works
python scripts/build_index.py

# 3. Check what will be committed
git status
git diff content/people/

# 4. Verify no temporary files are staged
git status --ignored
```

## Example: Complete Enrichment of Jonathan Home's Profile

```bash
# Step 1: Research sources
# - ETH Zurich faculty page: https://www.phys.ethz.ch/.../jhome.html
# - Oxford thesis repository: https://ora.ox.ac.uk/...
# - ORCID: https://orcid.org/0000-0002-4093-1550

# Step 2: Create enrichment data
cat > scripts/data/home_enrichment.json << 'EOF'
[
  {
    "name": "Jonathan P. Home",
    "institution": "ETH Zürich",
    "homepage": "https://iqe.phys.ethz.ch/...",
    "thesis_title": "High Fidelity Operations for Quantum Information...",
    "thesis_year": 2006,
    "thesis_link": "https://ora.ox.ac.uk/objects/uuid:...",
    "verified_sources": [
      "https://www.phys.ethz.ch/.../jhome.html",
      "https://ora.ox.ac.uk/...",
      "https://orcid.org/0000-0002-4093-1550"
    ]
  }
]
EOF

# Step 3: Apply enrichment (dry-run first)
python scripts/batch_enrich_profiles.py scripts/data/home_enrichment.json --dry-run

# Step 4: Apply for real
python scripts/batch_enrich_profiles.py scripts/data/home_enrichment.json

# Step 5: Verify
python scripts/verify_profile_data.py 016-jonathan-home

# Step 6: Commit with sources
git add content/people/016-jonathan-home.md
git commit -m "data: verify & enrich profile — Jonathan P. Home

Sources:
- https://www.phys.ethz.ch/.../jhome.html
- https://ora.ox.ac.uk/...
- https://orcid.org/0000-0002-4093-1550"
```

## Common Issues and Solutions

### Issue: Website not accessible

**Solution:** Use batch enrichment with manually curated JSON data.

```bash
# Download HTML manually and save to scripts/data/
# Then create JSON from the HTML

# Or use batch enrichment with verified data from other sources
python scripts/batch_enrich_profiles.py scripts/data/manual_data.json
```

### Issue: Cannot verify advisor information

**Solution:** Leave fields as `null` and add explanatory note.

```yaml
education:
  - degree: "PhD (Physics)"
    institution: "University Name"
    year: 2006
    advisor: null
    confidence: "not_found"
    note: "Checked university website and AcademicTree; no advisor listed"
```

### Issue: Profile verification fails

**Solution:** Run verification to see specific issues.

```bash
python scripts/verify_profile_data.py <person-id>

# Fix issues in the markdown file
# Re-run verification
python scripts/verify_profile_data.py <person-id>
```

### Issue: Multiple people with similar names

**Solution:** Use institution to disambiguate.

```python
# The tools will use both name and institution to match
# If still ambiguous, create new profile with unique ID
```

## Best Practices

1. **Always start with dry-run** to preview changes
2. **Verify sources** before adding any data
3. **Document sources** in commit messages
4. **Small batches** - process 5-10 profiles at a time
5. **Test build** after each batch to catch issues early
6. **Use confidence levels** appropriately:
   - `confirmed` - verified from authoritative source
   - `academictree_only` - found only on AcademicTree
   - `not_found` - attempted verification but not found
7. **Never guess** - if uncertain, leave as `null` with note

## Quality Gates

Before opening a PR:

```bash
# 1. All profiles validate
python scripts/verify_profile_data.py --all

# 2. Build succeeds
python scripts/build_index.py

# 3. Review all changes
git diff main...auto/ionlandscape-ingestion

# 4. Check for accidental commits
git status --ignored

# 5. All commits have source documentation
git log --oneline
```

## Summary

The ingestion system provides:

- ✅ Automated fetching from authoritative sources
- ✅ Profile matching and enrichment
- ✅ Strict verification rules
- ✅ Source tracking
- ✅ Quality validation
- ✅ Prevents hallucination

Always prioritize data quality over quantity. Better to have 10 well-verified profiles than 100 with questionable data.
