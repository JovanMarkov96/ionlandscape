# Runtime Execution Graph

## 1. Backend Processing (Build Time)

**Entry Point**: `.github/workflows/deploy.yml` -> `python scripts/build_index.py`

1.  **`build_index.py:main()`**
    *   Iterates `content/people/*.md`.
    *   Parses Frontmatter (YAML).
    *   Constructs in-memory graph of People + Relationships.
    *   **Output 1**: `website/static/data/people.json` (Full detail).
    *   **Output 2**: `website/static/data/people.geojson` (Mercator coordinates + ID).

## 2. Frontend Boot (Runtime)

**Entry Point**: Browser navigates to `/ionlandscape/`

1.  **Docusaurus Bootstrap**
    *   Loads `docusaurus.config.js`.
    *   detects route `/`.
    *   Hydrates `website/src/pages/index.js`.

2.  **`HomeContent` Component (`index.js`)**
    *   **State Init**: `selectedPersonId` = null.
    *   **Render**:
        *   `<MapPanel />`
        *   `<PersonPanel />` (Hidden/Collapsed)

3.  **`MapPanel` Lifecycle**
    *   `useEffect` -> fetches `/data/people.geojson`.
    *   `maplibregl.Map` init.
    *   Adds Source `openmaptiles` (Remote).
    *   Adds Source `serbia-boundary` (Local PMTiles).
    *   Renders Markers from GeoJSON.

4.  **User Interaction: Select Person**
    *   User clicks Marker Popup "Open Profile".
    *   `MapPanel` callback `onPersonSelect(id)`.
    *   `HomeContent` updates state `selectedPersonId = id`.
    *   `PersonPanel` receives new prop.

5.  **`PersonPanel` Lifecycle**
    *   `useEffect` -> fetches `/data/people.json`.
    *   Finds object matching `id`.
    *   Renders Bio, Trajectory, Links.
    *   Applies CSS class `.panel-open` (slide-in animation via `custom.css`).

## 3. Static Assets Chain

*   **CSS**: `website/src/css/custom.css` -> Bundled by Webpack -> Injected into `<head>`.
*   **Tiles**: `website/static/map/serbia.pmtiles` -> Served as raw static file -> Fetched by MapLibre via HTTP Range Requests.
