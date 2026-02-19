# Repo Audit

Key existing files relied upon:

1.  `scripts/core/build_index.py`: The central build script for generating data artifacts. Modified to scan `content/companies/` and output `companies.json` / `companies.geojson`.
2.  `website/src/components/PersonPanel.jsx`: The canonical UI for displaying entity details. Used as a template for `CompanyPanel.jsx` to ensure consistent styling, typography, and layout.
3.  `website/src/components/MapPanel.jsx`: The map rendering component. Updated to load company data, render distinct markers (orange), and provides a filtering UI.
4.  `website/src/pages/index.js`: The main entry point managing application state. Updated to handle mutual exclusivity between selected Person and Company.
