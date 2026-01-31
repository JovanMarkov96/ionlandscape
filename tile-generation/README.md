# Ion Landscape Self-Hosted Tile Generation

## Overview

This directory contains everything needed to generate **fully self-hosted vector tiles** with the **Serbian worldview** (Kosovo rendered as part of Serbia).

## Architecture

```
OSM Data (PBF) → Tilemaker + process.lua → MBTiles → PMTiles → Website Static
                          ↓
              Kosovo admin-0 → admin-4 downgrade
```

## How Kosovo is Fixed

The `process.lua` script contains a `is_kosovo_admin0()` function that:
1. Detects Kosovo boundary relations by name, ISO code (XK), or Wikidata ID
2. Downgrades them from `admin_level=2` (country) to `admin_level=4` (region)

**Result**: No international border line is generated between Serbia and Kosovo.

## Prerequisites

Install these tools:

```bash
# Tilemaker (tile generator)
# Ubuntu/Debian:
sudo apt install tilemaker

# Or build from source:
git clone https://github.com/systemed/tilemaker.git
cd tilemaker && make && sudo make install

# PMTiles CLI (for conversion)
npm install -g pmtiles

# Osmium (for merging PBF files)
sudo apt install osmium-tool
```

## Troubleshooting

If the script says "Tilemaker not found":
1. Download `tilemaker-windows.zip` directly from [GitHub Releases](https://github.com/systemed/tilemaker/releases/latest)
2. Extract it and copy `tilemaker.exe` (and the `resources` folder if present) directly into this `tile-generation` folder.
3. Run `.\generate-tiles.ps1` again.

If `pmtiles` is not found:
1. Run `npm install -g pmtiles` 
2. Or let the script use `npx pmtiles` (it attempts this automatically).

## Full Planet Generation

For production with full global coverage:

1. Download planet PBF (~70GB):
```bash
wget -O data/planet.osm.pbf https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf
```

2. Edit `generate-tiles.sh` to use planet file

3. Run (takes 6-12 hours, needs ~200GB disk):
```bash
./generate-tiles.sh
```

## Output

- `output/tiles.mbtiles` - Intermediate MBTiles file
- `output/world.pmtiles` - Final PMTiles for static hosting
- Auto-copied to `../website/static/map/world.pmtiles`

## Using in MapPanel.jsx

The website's MapPanel component is already configured to use PMTiles:

```javascript
// Uses PMTiles protocol for self-hosted tiles
import { Protocol } from 'pmtiles';
maplibregl.addProtocol('pmtiles', new Protocol().tile);

// Source configuration
sources: {
  'basemap': {
    type: 'vector',
    url: 'pmtiles:///ionlandscape/map/world.pmtiles'
  }
}
```

## Attribution

Required attribution (ODbL compliance):
```
© OpenStreetMap contributors
```

## Worldview Options

The current configuration implements **RS (Serbia)** worldview. To change:

1. Edit `process.lua`
2. Modify `is_kosovo_admin0()` to return `false` (neutral view)
3. Or add similar logic for other disputed regions

## File Sizes (Approximate)

| Scope | PBF Input | MBTiles Output | PMTiles Output |
|-------|-----------|----------------|----------------|
| Serbia only | 500MB | 200MB | 150MB |
| Europe | 25GB | 10GB | 8GB |
| Full Planet | 70GB | 80GB | 60GB |
