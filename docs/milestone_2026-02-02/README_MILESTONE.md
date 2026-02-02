# Ion Landscape - Milestone Audit (2026-02-02)

**Status**: "Last Known Good"
**Auditor**: Antigravity (AI System)
**Date**: 2026-02-02

## 1. Summary
This snapshot captures the Ion Landscape working state after the "Map UI Polish" and "Profile Renumbering" phases. The system is fully functional, deploying to GitHub Pages via Actions.

## 2. Running Locally

### Prerequisites
- Node.js v20+
- Python 3.10+

### Commands
```bash
# 1. Install Dependencies
pip install -r scripts/requirements.txt
cd website && npm install

# 2. Re-generate Data (if markdown changed)
python ../scripts/build_index.py

# 3. Start Dev Server
npm run start
# Opens http://localhost:3000/ionlandscape/
```

## 3. Deployment
- **Trigger**: Push to `main` branch.
- **Workflow**: `.github/workflows/deploy.yml`
- **Steps**:
    1.  Install Python deps.
    2.  Run `scripts/build_index.py`.
    3.  Install Node deps.
    4.  Run `npm run build`.
    5.  Push `website/build` artifact to `gh-pages`.

## 4. Key Configurations
- **Site Config**: `website/docusaurus.config.js`
- **Map Styling**: `website/src/css/custom.css` (Contains MapLibre overrides & mobile logic)
- **Data Schema**: `SCHEMA.md` (Enforced by `verify_profile_data.py`)

## 5. Known Limitations
- **Tile Generation**: Requires manual execution of `tile-generation/generate-tiles.ps1` on Windows if administrative boundaries need updates.
- **Mobile**: Profile panel interaction relies on CSS overlays (`PersonPanel.jsx` + `custom.css`) specific to screen width <600px.
