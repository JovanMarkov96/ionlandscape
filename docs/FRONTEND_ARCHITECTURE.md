---
id: frontend-architecture
title: Frontend Architecture
sidebar_label: Frontend Architecture
---

# Ion Landscape Frontend Architecture

This document serves as the technical guide to the Ion Landscape frontend, built with Docusaurus, React, and Leaflet.

## 1. Directory Structure

- **`src/pages/`**: Top-level routes.
  - `index.js`: The main landing page containing the Map.
  - `groups.js`: The "Search Research Groups" page with filtering logic.
- **`src/components/`**: Reusable UI components.
  - `PersonPanel.jsx`: The slide-out sidebar displaying researcher profiles.
  - `MapPanel.jsx`: (Internal) Wrapper for the Leaflet map logic.
- **`src/css/`**: Global styles.
  - `custom.css`: The core design system and overrides.
- **`static/data/`**: Data source.
  - `people.json`: The master dataset of researchers (generated from Markdown profiles).

## 2. Design System (`custom.css`)

We use a polished, custom CSS system on top of Docusaurus's Infima theme.

### Color Palette ("Pleasant Blue")
- **Primary**: Indigo/Slate (`#4f46e5`) - Used for active states, primary buttons.
- **Search Page Primary**: Pleasant Blue (`#3b82f6`) - Used for buttons and badges on the Search page.
- **Surface**: Off-white (`#f8fafc`) for backgrounds, light gray (`#e2e8f0`) for borders.
- **Text**: Dark Slate (`#0f172a`) for high contrast in light mode.

### Key CSS Variables
| Variable | Description |
| :--- | :--- |
| `--ion-surface` | Background color for panels and cards (Light: `#f8fafc`). |
| `--ion-border` | Border color for separators and inputs (Light: `#e2e8f0`). |
| `--ion-accent` | Primary accent color (`#4f46e5`). |
| `--ion-radius` | Standard border radius (`12px`). |
| `--ion-shadow-lg` | Large shadow for floating elements (popups, side panel). |

### Typography
- **Font**: [Inter](https://fonts.google.com/specimen/Inter) (Google Fonts).
- **Scale**: Standardized headers (`h1`-`h4`) and body text via Docusaurus defaults, customized for legibility.

### Utility Classes
- `.navbar-custom-btn`: Styles for the icon-only navbar buttons.
- `.panel-link`: Styles for the emoji-prefixed link cards in the Person Panel.
- `.advisor-link`: Styled links for advisors within the academic trajectory.
- `.location-view-container`: Container for the "Location View" content.

## 3. Component Architecture

### `PersonPanel.jsx`
Responsible for displaying the details of a selected researcher.

- **Props**:
  - `personId`: The ID (or markdown filename) of the person to display.
  - `onClose`: Callback to close the panel.
- **Data Loading**: Fetches `people.json` on mount and finds the person matching `personId`.
- **Key Features**:
  - **Badges**: Renders "Trapped Ions" / "Neutral Atoms" badges with specific gradients.
  - **Trajectory**: Maps over `education` and `postdocs` arrays to render a timeline.
  - **Affiliations**: "Card-style" layout for current affiliations.
  - **Links**: Renders Homepage, Google Scholar, and ORCID as styled cards.

### `groups.js` (Search Page)
A searchable, filterable list of all researchers.

- **State Management**: active filters are synced with the **URL Query Parameters** (`?q=...&label=...`). This ensures searches are shareable.
- **Filtering Logic**:
  - **Category**: "All", "Trapped Ions", or "Neutral Atoms".
  - **Search**: Fuzzy text search on names.
  - **Dropdowns**: Filter by Label, Ion Species, Institution, and Country.
  - **Logic**: Filters are additive (AND logic).
- **Responsive Layout**: Adapts from a grid view (Desktop) to a stacked view (Mobile).

### `index.js` (Map Page)
The entry point.

- **Layout**: Renders the `MapPanel` (Leaflet) and `PersonPanel` side-by-side.
- **Interaction**: Clicking a map marker updates the URL hash or local state, triggering `PersonPanel` to open.

## 4. Navbar Customization

The navbar is heavily customized in `docusaurus.config.js` and `custom.css`.

- **Icon-Only Buttons**: Home, Search, GitHub, and Share are rendered as HTML items containing SVG icons.
- **Hover Reveal**: CSS transitions expand the buttons to reveal text labels on hover.
- **Light Mode Contrast**: Specific CSS overrides force navbar items to be Dark Slate (`#0f172a`) in light mode to ensure visibility against the glassmorphic background.

## 5. Data Flow

1.  **Ingestion**: Python scripts process `data/people/*.md` files.
2.  **Generation**: `scripts/generate_json.py` builds `static/data/people.json`.
3.  **Consumption**: The frontend (`PersonPanel`, `Groups`, `Map`) fetches this single JSON file at runtime to populate the UI.

## 6. Development Workflow

- **Start Dev Server**: `npm start` (or `npx docusaurus start`).
- **Build**: `npm run build`.
- **Lint/Format**: Standard Prettier configuration.
