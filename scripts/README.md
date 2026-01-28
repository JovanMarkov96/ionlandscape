# Ion Landscape Scripts

This directory contains automation tools for profile ingestion, verification, and maintenance.

## Quick Reference

### Profile Management

| Script | Purpose | Usage |
|--------|---------|-------|
| `create_profile_template.py` | Create new profile interactively | `python scripts/create_profile_template.py` |
| `verify_profile_data.py` | Validate profile schema | `python scripts/verify_profile_data.py --all` |
| `ingest_profiles.py` | Automated ingestion from web | `python scripts/ingest_profiles.py --dry-run` |
| `batch_enrich_profiles.py` | Bulk update from JSON | `python scripts/batch_enrich_profiles.py data.json` |
| `cite_sources.py` | Document sources | `python scripts/cite_sources.py <id> --add` |

### Build & Maintenance

| Script | Purpose | Usage |
|--------|---------|-------|
| `build_index.py` | Generate JSON/GeoJSON from MD | `python scripts/build_index.py` |
| `normalize_markdown.py` | Normalize frontmatter | `python scripts/normalize_markdown.py` |

### Legacy Scripts

| Script | Purpose | Note |
|--------|---------|------|
| `add_labels_and_ion_species.py` | Historical data migration | One-time use |
| `apply_phd_updates.py` | Historical data migration | One-time use |
| `cleanup_people.py` | Historical cleanup | One-time use |

## Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r scripts/requirements.txt
```

## Common Workflows

### 1. Create New Profile

```bash
# Interactive creation with validation
python scripts/create_profile_template.py

# Verify the new profile
python scripts/verify_profile_data.py <person-id>

# Test build
python scripts/build_index.py
```

### 2. Enrich Existing Profile

```bash
# Document sources as you go
python scripts/cite_sources.py <person-id> --add

# Manually edit the profile file
# content/people/<person-id>.md

# Verify changes
python scripts/verify_profile_data.py <person-id>

# Generate commit message with sources
python scripts/cite_sources.py <person-id> --commit-msg --name "Person Name"
```

### 3. Batch Enrichment

```bash
# Create JSON with verified data
cat > scripts/data/batch.json << 'EOF'
[
  {
    "name": "PI Name",
    "institution": "University",
    "homepage": "https://...",
    "verified_sources": ["https://..."]
  }
]
EOF

# Dry run to preview
python scripts/batch_enrich_profiles.py scripts/data/batch.json --dry-run

# Apply changes
python scripts/batch_enrich_profiles.py scripts/data/batch.json
```

### 4. Automated Ingestion

```bash
# Fetch from authoritative website (requires internet)
python scripts/ingest_profiles.py --dry-run --limit 10

# Process for real
python scripts/ingest_profiles.py --limit 10

# Review logs
cat scripts/logs/ingestion_*.log
```

### 5. Verify All Profiles

```bash
# Check all profiles for schema compliance
python scripts/verify_profile_data.py --all

# Expected exit code:
# 0 = all passed
# 1 = errors found
```

## Output Locations

### Generated Data
- `website/static/data/people.json` - All profiles as JSON
- `website/static/data/people.geojson` - Geospatial data
- `website/static/data/edges.csv` - Relationship graph

### Logs and Reports
- `scripts/logs/ingestion_*.log` - Ingestion activity logs
- `scripts/logs/sources_*.json` - Source tracking per session

### Working Data
- `scripts/data/` - Input JSON files, cached HTML, etc.
- `.gitignore` excludes logs and temporary files

## Dependencies

From `requirements.txt`:
- `python-frontmatter` - Parse/write YAML frontmatter
- `PyYAML` - YAML processing
- `geojson` - GeoJSON generation
- `beautifulsoup4` - HTML parsing for web scraping
- `requests` - HTTP client for fetching sources

## Environment Variables

None required. All configuration is in the scripts themselves.

## Testing

### Unit Tests
Currently no unit tests. Scripts are designed for manual use with verification.

### Integration Testing
```bash
# Full workflow test
python scripts/verify_profile_data.py --all && \
python scripts/build_index.py && \
echo "All systems go!"
```

## Troubleshooting

### "Module not found"
```bash
pip install -r scripts/requirements.txt
```

### "Permission denied"
```bash
chmod +x scripts/*.py
```

### "Website not accessible"
Use batch enrichment with manual JSON data:
```bash
python scripts/batch_enrich_profiles.py scripts/data/manual_data.json
```

### "Verification fails"
Check specific errors:
```bash
python scripts/verify_profile_data.py <person-id>
```

## Development

### Adding New Scripts

1. Add shebang: `#!/usr/bin/env python3`
2. Add docstring with usage
3. Make executable: `chmod +x scripts/new_script.py`
4. Update this README
5. Add to `.gitignore` if generates temp files

### Modifying Existing Scripts

1. Test changes locally first
2. Run verification: `python scripts/verify_profile_data.py --all`
3. Test build: `python scripts/build_index.py`
4. Document changes in commit message

## Documentation

See the project root for detailed guides:

- **[INGESTION_GUIDE.md](../INGESTION_GUIDE.md)** - Complete ingestion workflow
- **[QUICKSTART.md](../QUICKSTART.md)** - Quick start examples
- **[SCHEMA.md](../SCHEMA.md)** - Field reference documentation
- **[EXAMPLE_WORKFLOW.md](../EXAMPLE_WORKFLOW.md)** - End-to-end example

## Support

For issues or questions:
1. Check documentation above
2. Review existing profiles for examples
3. Open an issue on GitHub

## License

Same as the main repository (see ../LICENSE).
