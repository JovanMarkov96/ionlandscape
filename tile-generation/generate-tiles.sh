#!/bin/bash
# ============================================================================
# Ion Landscape Tile Generation Pipeline
# Generates vector tiles with Serbian worldview (Kosovo as admin-4)
# ============================================================================

set -e

echo "==========================================="
echo "Ion Landscape Tile Generation Pipeline"
echo "Worldview: RS (Serbia)"
echo "==========================================="

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/output"
DATA_DIR="$SCRIPT_DIR/data"

mkdir -p "$OUTPUT_DIR" "$DATA_DIR"

# ============================================================================
# STEP 1: Download OSM Data
# Options:
#   A) Full planet (~70GB) - uncomment for production
#   B) Europe extract (~25GB) - good for testing
#   C) Serbia + neighbors (~500MB) - fast testing
# ============================================================================

echo ""
echo "Step 1: Downloading OSM data..."

# Option C: Serbia + neighbors (recommended for testing)
if [ ! -f "$DATA_DIR/serbia.osm.pbf" ]; then
    echo "Downloading Serbia region extract..."
    wget -O "$DATA_DIR/serbia.osm.pbf" \
        "https://download.geofabrik.de/europe/serbia-latest.osm.pbf"
fi

# Also download Kosovo separately (it's often in a separate extract)
if [ ! -f "$DATA_DIR/kosovo.osm.pbf" ]; then
    echo "Downloading Kosovo region data..."
    # Note: Some sources list Kosovo separately, some include it with Serbia
    # Geofabrik treats them separately, so we merge
    wget -O "$DATA_DIR/kosovo.osm.pbf" \
        "https://download.geofabrik.de/europe/kosovo-latest.osm.pbf" || true
fi

# For full planet (production):
# wget -O "$DATA_DIR/planet.osm.pbf" "https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf"

# ============================================================================
# STEP 2: Merge Serbia + Kosovo data (if both exist)
# ============================================================================

echo ""
echo "Step 2: Preparing data..."

INPUT_FILE="$DATA_DIR/serbia.osm.pbf"

if [ -f "$DATA_DIR/kosovo.osm.pbf" ]; then
    echo "Merging Serbia and Kosovo data..."
    # Requires osmium-tool
    if command -v osmium &> /dev/null; then
        osmium merge "$DATA_DIR/serbia.osm.pbf" "$DATA_DIR/kosovo.osm.pbf" \
            -o "$DATA_DIR/serbia-merged.osm.pbf" --overwrite
        INPUT_FILE="$DATA_DIR/serbia-merged.osm.pbf"
    else
        echo "Warning: osmium-tool not found. Using Serbia data only."
        echo "Install with: apt install osmium-tool"
    fi
fi

# ============================================================================
# STEP 3: Generate Vector Tiles with Tilemaker
# ============================================================================

echo ""
echo "Step 3: Generating vector tiles with Tilemaker..."
echo "This applies the Kosovo → admin-4 downgrade..."

tilemaker \
    --input "$INPUT_FILE" \
    --output "$OUTPUT_DIR/tiles.mbtiles" \
    --config "$SCRIPT_DIR/config.json" \
    --process "$SCRIPT_DIR/process.lua" \
    --verbose

echo "MBTiles generated: $OUTPUT_DIR/tiles.mbtiles"

# ============================================================================
# STEP 4: Convert MBTiles → PMTiles
# ============================================================================

echo ""
echo "Step 4: Converting to PMTiles format..."

# Requires pmtiles CLI: npm install -g pmtiles OR go install github.com/protomaps/go-pmtiles/cmd/pmtiles@latest
if command -v pmtiles &> /dev/null; then
    pmtiles convert "$OUTPUT_DIR/tiles.mbtiles" "$OUTPUT_DIR/world.pmtiles"
    echo "PMTiles generated: $OUTPUT_DIR/world.pmtiles"
else
    echo "Warning: pmtiles CLI not found."
    echo "Install with: npm install -g pmtiles"
    echo "Then run: pmtiles convert $OUTPUT_DIR/tiles.mbtiles $OUTPUT_DIR/world.pmtiles"
fi

# ============================================================================
# STEP 5: Copy to website static folder
# ============================================================================

echo ""
echo "Step 5: Deploying to website..."

WEBSITE_MAP_DIR="$SCRIPT_DIR/../website/static/map"
mkdir -p "$WEBSITE_MAP_DIR"

if [ -f "$OUTPUT_DIR/world.pmtiles" ]; then
    cp "$OUTPUT_DIR/world.pmtiles" "$WEBSITE_MAP_DIR/"
    echo "Deployed: $WEBSITE_MAP_DIR/world.pmtiles"
fi

echo ""
echo "==========================================="
echo "✅ Tile generation complete!"
echo ""
echo "Files generated:"
ls -lh "$OUTPUT_DIR/"
echo ""
echo "Kosovo has been downgraded from admin-0 to admin-4."
echo "No international border will appear between Serbia and Kosovo."
echo "==========================================="
