<#
.SYNOPSIS
Ion Landscape Tile Generation Script (Windows/PowerShell)
Generates vector tiles with Serbian worldview (Kosovo as admin-4).

.DESCRIPTION
This script automates the tile generation pipeline on Windows:
1. Downloads OSM data (Serbia/Kosovo or Planet)
2. Runs Tilemaker to generate vector tiles
3. Converts to PMTiles (optional)
4. Deploys to website

.NOTES
Requires 'tilemaker.exe' to be in the path or in the script directory.
#>

$ScriptDir = $PSScriptRoot
$DataDir = Join-Path $ScriptDir "data"
$OutputDir = Join-Path $ScriptDir "output"
$WebsiteMapDir = Join-Path $ScriptDir "..\website\static\map"

# Ensure directories exist
Non-TerminatingError -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $DataDir | Out-Null
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
New-Item -ItemType Directory -Force -Path $WebsiteMapDir | Out-Null

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Ion Landscape Tile Generation (Windows)" -ForegroundColor Cyan
Write-Host "Worldview: RS (Serbia)" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

# ============================================================================
# CHECK PREREQUISITES
# ============================================================================

if (-not (Get-Command "tilemaker" -ErrorAction SilentlyContinue)) {
    Write-Warning "Tilemaker not found in PATH."
    Write-Host "Please download the latest Windows release from:"
    Write-Host "https://github.com/systemed/tilemaker/releases"
    Write-Host "And unzip 'tilemaker.exe' into: $ScriptDir"
    
    if (-not (Test-Path (Join-Path $ScriptDir "tilemaker.exe"))) {
        Write-Error "tilemaker.exe not found. Aborting."
        exit 1
    }
    $TilemakerCmd = Join-Path $ScriptDir "tilemaker.exe"
} else {
    $TilemakerCmd = "tilemaker"
}

# ============================================================================
# STEP 1: DOWNLOAD DATA
# ============================================================================
Write-Host "`nStep 1: Downloading OSM Data..." -ForegroundColor Green

$SerbiaPbf = Join-Path $DataDir "serbia-latest.osm.pbf"
if (-not (Test-Path $SerbiaPbf)) {
    Write-Host "Downloading Serbia data..."
    Invoke-WebRequest -Uri "https://download.geofabrik.de/europe/serbia-latest.osm.pbf" -OutFile $SerbiaPbf
}

$KosovoPbf = Join-Path $DataDir "kosovo-latest.osm.pbf"
if (-not (Test-Path $KosovoPbf)) {
    Write-Host "Downloading Kosovo data..."
    try {
        Invoke-WebRequest -Uri "https://download.geofabrik.de/europe/kosovo-latest.osm.pbf" -OutFile $KosovoPbf
    } catch {
        Write-Warning "Could not download Kosovo data (might be merged in Serbia already). Continuing..."
    }
}

# NOTE: Merging requires 'osmium'. Assuming individual processing or pre-merged for now.
# For simplicity in this Windows script, we'll process just Serbia (which often contains Kosovo data in some extracts)
# or just run on Serbia.osm.pbf
$InputFile = $SerbiaPbf

# ============================================================================
# STEP 2: GENERATE TILES
# ============================================================================
Write-Host "`nStep 2: Generating Vector Tiles..." -ForegroundColor Green
Write-Host "Applying Kosovo -> admin-4 downgrade..."

$ConfigFile = Join-Path $ScriptDir "config.json"
$ProcessFile = Join-Path $ScriptDir "process.lua"
$OutputMbtiles = Join-Path $OutputDir "tiles.mbtiles"

& $TilemakerCmd --input $InputFile --output $OutputMbtiles --config $ConfigFile --process $ProcessFile --verbose

if (-not (Test-Path $OutputMbtiles)) {
    Write-Error "Tile generation failed."
    exit 1
}

# ============================================================================
# STEP 3: CONVERT TO PMTILES
# ============================================================================
Write-Host "`nStep 3: Converting to PMTiles..." -ForegroundColor Green

$OutputPmtiles = Join-Path $OutputDir "world.pmtiles"

if (Get-Command "pmtiles" -ErrorAction SilentlyContinue) {
    pmtiles convert $OutputMbtiles $OutputPmtiles
} else {
    Write-Warning "pmtiles CLI not found."
    Write-Host "Skipping conversion. You can create PMTiles later."
    Write-Host "Install with: 'npm install -g pmtiles' or 'go install github.com/protomaps/go-pmtiles/cmd/pmtiles@latest'"
    # Fallback: Just copy .mbtiles if MapLibre supported it (it doesn't directly without server)
    # But we need PMTiles for static hosting.
}

# ============================================================================
# STEP 4: DEPLOY
# ============================================================================
Write-Host "`nStep 4: Deploying..." -ForegroundColor Green

if (Test-Path $OutputPmtiles) {
    Copy-Item -Path $OutputPmtiles -Destination $WebsiteMapDir -Force
    Write-Host "Deployed to: $WebsiteMapDir\world.pmtiles" -ForegroundColor Cyan
}

Write-Host "`nDONE! Tile generation complete." -ForegroundColor Green
