# Deprecation Plan (Safe Archival)

**Strategy**: Move unused files to `deprecated/` instead of deleting them immediately. This preserves history and allows easy rollback.

## 1. Directory Setup
```bash
mkdir -p deprecated/scripts
mkdir -p deprecated/website
```

## 2. Move List

### A. Legacy Scripts (to `deprecated/scripts/`)
These are one-off migration or analysis tools that are no longer part of the active pipeline.
- `scripts/add_labels_and_ion_species.py`
- `scripts/apply_phd_updates.py`
- `scripts/cleanup_people.py`
- `scripts/find_missing_phd.py`
- `scripts/renumber_profiles.py`
- `scripts/analyze_affiliations.py`

### B. Manual Tests & Artifacts (to `deprecated/website/`)
These are manual Puppeteer tests not integrated into CI, and their image artifacts.
- `website/test-layout.js`
- `website/test-mobile.js`
- `website/test-dark-mode.js`
- `website/test-*.png` (Wildcard move)

## 3. Rollback Plan
If something breaks, simply move the file back to its original location:
```bash
# Example
mv deprecated/scripts/renumber_profiles.py scripts/
```

## 4. Execution Commands (PowerShell)
Run this block to execute the cleanup:

```powershell
# Create Archive
New-Item -ItemType Directory -Force -Path deprecated/scripts
New-Item -ItemType Directory -Force -Path deprecated/website

# Move Scripts
Move-Item scripts/add_labels_and_ion_species.py deprecated/scripts/
Move-Item scripts/apply_phd_updates.py deprecated/scripts/
Move-Item scripts/cleanup_people.py deprecated/scripts/
Move-Item scripts/find_missing_phd.py deprecated/scripts/
Move-Item scripts/renumber_profiles.py deprecated/scripts/
Move-Item scripts/analyze_affiliations.py deprecated/scripts/

# Move Website Tests
Move-Item website/test-layout.js deprecated/website/
Move-Item website/test-mobile.js deprecated/website/
Move-Item website/test-dark-mode.js deprecated/website/
Move-Item website/test-*.png deprecated/website/ -ErrorAction SilentlyContinue

# Cleanup Temp Files
Remove-Item reflog_dump.txt -ErrorAction SilentlyContinue
Remove-Item file_inventory.txt -ErrorAction SilentlyContinue
```
