# Architecture Overview

## 1. System Components

```ascii
[ Authoritative Sources ]
        |
    (Manual/Scripted Ingestion)
        v
[ Markdown Content ] <--- Source of Truth (content/people/*.md)
        |
    (scripts/build_index.py)
        v
[ Static JSON/GeoJSON ] (website/static/data/)
        |
        +-----------------------+
        |                       |
[ MapPanel.jsx ]         [ PersonPanel.jsx ]
(visualizes GeoJSON)      (visualizes JSON)
        |                       |
        +-------+       +-------+
                |       |
           [ Docusaurus App ]
                |
           (npm run build)
                v
          [ Static HTML/JS ]
                |
          (GitHub Pages)
```

## 2. Modules & Responsibilities

### A. Data Layer (`content/`)
-   **Responsibility**: Storage of all researcher data.
-   **Format**: Jekyll-style Markdown with YAML Frontmatter.
-   **Validation**: `scripts/verify_profile_data.py`.

### B. Pipeline Layer (`scripts/`)
-   **Responsibility**: ETL (Extract, Transform, Load).
-   **Key Script**: `build_index.py` transforms flat Markdown files into a relational graph (`edges.csv`) and map data (`people.geojson`).

### C. Frontend Layer (`website/src/`)
-   **Framework**: Docusaurus Classic Preset.
-   **Interactive Components**:
    -   `MapPanel`: Handles the MapLibre instance, layers, and markers.
    -   `PersonPanel`: Handles the slide-out detail view, "back" navigation, and academic trajectory rendering.
-   **Integration point**: `website/src/pages/index.js` acts as the controller, managing state between Map and Panel.

### D. Map Layer (`tile-generation/`)
-   **Responsibility**: Serving base map tiles and geopolitical overlays.
-   **Live**: Fetches from OpenFreeMap (remote).
-   **Static**: `serbia.pmtiles` (local) for specific boundary overrides.
