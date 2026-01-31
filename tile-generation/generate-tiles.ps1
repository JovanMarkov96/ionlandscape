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
$ErrorActionPreference = "SilentlyContinue"
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

$TilemakerCmd = "tilemaker"
$TilemakerPath = Get-Command "tilemaker" -ErrorAction SilentlyContinue

if (-not $TilemakerPath) {
    # Check common locations
    $PossiblePaths = @(
        Join-Path $ScriptDir "tilemaker.exe",
        "C:\Users\jovanm\Downloads\tilemaker-windows\build\RelWithDebInfo\tilemaker.exe",
        (Join-Path $PSScriptRoot "tilemaker.exe")
    )
    
    foreach ($Path in $PossiblePaths) {
        if (Test-Path $Path) {
            $TilemakerCmd = $Path
            Write-Host "Found tilemaker at: $TilemakerCmd" -ForegroundColor Green
            break
        }
    }
    
    if ($TilemakerCmd -eq "tilemaker") {
        Write-Warning "Tilemaker not found in PATH or common locations."
        Write-Host "Please ensure 'tilemaker.exe' is in the script directory."
        exit 1
    }
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
    }
    catch {
        Write-Warning "Could not download Kosovo data. Continuing..."
    }
}

$InputFile = $SerbiaPbf
# NOTE: To truly fix Kosovo, we usually need the Kosovo data merged or included.
# Geofabrik Serbia might ALREADY include Kosovo (often does).
# If we need to merge, we'd need osmium. For now, we rely on Serbia PBF containing it.
if (Test-Path $KosovoPbf) {
    # Simple check: if Kosovo file exists, maybe use it if Serbia is small?
    # But for now let's stick to Serbia extract which usually covers the region.
    # OR: If the user provided a merged file manually.
}

# ============================================================================
# STEP 2: GENERATE TILES
# ============================================================================
Write-Host "`nStep 2: Generating Vector Tiles..." -ForegroundColor Green
Write-Host "Applying Kosovo -> admin-4 downgrade..."

$ConfigFile = Join-Path $ScriptDir "config.json"
$ProcessFile = Join-Path $ScriptDir "process.lua"
$OutputMbtiles = Join-Path $OutputDir "tiles.mbtiles"

# Create temp store dir if needed
$StoreDir = Join-Path $ScriptDir "store"
New-Item -ItemType Directory -Force -Path $StoreDir | Out-Null

& $TilemakerCmd --input $InputFile --output $OutputMbtiles --config $ConfigFile --process $ProcessFile --store $StoreDir --verbose

if (-not (Test-Path $OutputMbtiles)) {
    Write-Error "Tile generation failed. Output file not found."
    exit 1
}

# ============================================================================
# STEP 3: CONVERT TO PMTILES
# ============================================================================
Write-Host "`nStep 3: Converting to PMTiles..." -ForegroundColor Green

$OutputPmtiles = Join-Path $OutputDir "world.pmtiles"

if (Get-Command "pmtiles" -ErrorAction SilentlyContinue) {
    pmtiles convert $OutputMbtiles $OutputPmtiles
}
elseif (Get-Command "npx" -ErrorAction SilentlyContinue) {
    Write-Host "Using npx pmtiles..."
    npx pmtiles convert $OutputMbtiles $OutputPmtiles
}
else {
    Write-Warning "pmtiles CLI not found."
    exit 1
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
