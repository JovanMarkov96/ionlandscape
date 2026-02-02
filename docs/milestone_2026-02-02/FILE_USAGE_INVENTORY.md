# File Usage Inventory

**Legend**:
- **USED**: Critical for App Runtime, Build, or Content.
- **UNUSED**: Safe to delete or archive (Legacy, One-off, Dead).
- **CONFIDENCE**: High (Proven via trace), Med (Strong inference), Low (Guess).

| Path | Category | Used? | Confidence | Why / Evidence | Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Active Codebase** | | | | | |
| `website/docusaurus.config.js` | Config | **YES** | High | App Key Config | Keep |
| `website/package.json` | Config | **YES** | High | Build scripts, dependencies | Keep |
| `website/src/pages/index.js` | Frontend | **YES** | High | Main Entry Point (Route `/`) | Keep |
| `website/src/pages/groups.js` | Frontend | **YES** | High | Route `/groups` | Keep |
| `website/src/components/MapPanel.jsx` | Frontend | **YES** | High | Imported by `index.js` | Keep |
| `website/src/components/PersonPanel.jsx` | Frontend | **YES** | High | Imported by `index.js` | Keep |
| `website/src/css/custom.css` | Frontend | **YES** | High | Main Styling | Keep |
| `website/static/map/serbia.pmtiles` | Asset | **YES** | High | Loaded by MapPanel at runtime | Keep |
| `scripts/build_index.py` | Pipeline | **YES** | High | CI Build Step | Keep |
| `scripts/verify_profile_data.py` | Pipeline | **YES** | High | CI Validation Step | Keep |
| `scripts/ingest_profiles.py` | Utility | **YES** | High | Active Maintenance Tool | Keep |
| `scripts/create_profile_template.py` | Utility | **YES** | High | Active Maintenance Tool | Keep |
| `scripts/batch_enrich_profiles.py` | Utility | **YES** | High | Active Maintenance Tool | Keep |
| `scripts/cite_sources.py` | Utility | **YES** | High | Active Maintenance Tool | Keep |
| `scripts/normalize_markdown.py` | Utility | **YES** | Med | Linting tool (Manual) | Keep |
| `content/people/*.md` | Data | **YES** | High | Source of Truth | Keep |
| **Legacy / Unused** | | | | | |
| `scripts/add_labels_and_ion_species.py` | Script | **NO** | High | One-off migration (Legacy) | **Deprecate** |
| `scripts/apply_phd_updates.py` | Script | **NO** | High | One-off enrichment (Legacy) | **Deprecate** |
| `scripts/cleanup_people.py` | Script | **NO** | High | One-off deduplication (Legacy) | **Deprecate** |
| `scripts/find_missing_phd.py` | Script | **NO** | High | One-off enrichment (Legacy) | **Deprecate** |
| `scripts/renumber_profiles.py` | Script | **NO** | High | One-off fix (Completed Feb 2026) | **Deprecate** |
| `scripts/analyze_affiliations.py` | Script | **NO** | Med | Ad-hoc analysis script | **Deprecate** |
| `website/test-layout.js` | Test | **NO** | High | Not in CI, manual only | **Deprecate** |
| `website/test-mobile.js` | Test | **NO** | High | Not in CI, manual only | **Deprecate** |
| `website/test-dark-mode.js` | Test | **NO** | High | Not in CI, manual only | **Deprecate** |
| `website/test-*.png` | Artifact | **NO** | High | Stale test outputs | **Deprecate** |
| `reflog_dump.txt` | Artifact | **NO** | High | Debug artifact | **Delete** |
| `file_inventory.txt` | Artifact | **NO** | High | Debug artifact | **Delete** |
