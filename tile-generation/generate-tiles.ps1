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
# $ErrorActionPreference = "SilentlyContinue" <--- REMOVED
$ErrorActionPreference = "Stop" # Fail fast

New-Item -ItemType Directory -Force -Path $DataDir | Out-Null
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
New-Item -ItemType Directory -Force -Path $WebsiteMapDir | Out-Null

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Ion Landscape Tile Generation (Windows)" -ForegroundColor Cyan
Write-Host "Worldview: RS (Serbia)" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

# Enable TLS 1.2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# ============================================================================
# CHECK PREREQUISITES
# ============================================================================

# TOOLING URLS
$TilemakerUrl = "https://github.com/systemed/tilemaker/releases/download/v2.4.0/tilemaker-windows.zip"
# Corrected URL for v1.29.1
$PmtilesUrl = "https://github.com/protomaps/go-pmtiles/releases/download/v1.29.1/go-pmtiles_1.29.1_Windows_x86_64.zip"

# Function to Download and Extract
function Install-Tool ($Name, $Url, $DestDir) {
    Write-Host "Installing $Name..." -ForegroundColor Yellow
    $ZipPath = Join-Path $DestDir "$Name.zip"
    
    # Try using curl.exe first (more reliable on some Windows setups)
    if (Get-Command "curl.exe" -ErrorAction SilentlyContinue) {
        Write-Host "Downloading with curl.exe..."
        & curl.exe -L -o $ZipPath $Url
        if ($LASTEXITCODE -ne 0) {
            Write-Error "curl failed to download $Name"
            exit 1
        }
    }
    else {
        # Fallback to Invoke-WebRequest
        Write-Host "Downloading with Invoke-WebRequest..."
        try {
            Invoke-WebRequest -Uri $Url -OutFile $ZipPath -UseBasicParsing
        }
        catch {
            Write-Error "Failed to download $Name from $Url. Error: $_"
            exit 1
        }
    }
    
    try {
        Expand-Archive -Path $ZipPath -DestinationPath $DestDir -Force
    }
    catch {
        Write-Error "Failed to extract $Name.zip. Error: $_"
        exit 1
    }
    
    Remove-Item $ZipPath
}

# 1. TILEMAKER
$TilemakerCmd = "tilemaker"
$TilemakerPath = Get-Command "tilemaker" -ErrorAction SilentlyContinue

if (-not $TilemakerPath) {
    # Check if we already downloaded it (subdir or root)
    $LocalTilemakerSubdir = Join-Path $ScriptDir "tilemaker-windows\tilemaker.exe"
    $LocalTilemakerRoot = Join-Path $ScriptDir "tilemaker.exe"

    if (-not (Test-Path $LocalTilemakerSubdir) -and -not (Test-Path $LocalTilemakerRoot)) {
        Install-Tool "tilemaker" $TilemakerUrl $ScriptDir
    }
    
    if (Test-Path $LocalTilemakerSubdir) {
        $TilemakerCmd = $LocalTilemakerSubdir
        Write-Host "Using local tilemaker (subdir): $TilemakerCmd" -ForegroundColor Green
    }
    elseif (Test-Path $LocalTilemakerRoot) {
        $TilemakerCmd = $LocalTilemakerRoot
        Write-Host "Using local tilemaker (root): $TilemakerCmd" -ForegroundColor Green
    }
    else {
        Write-Error "Could not find tilemaker.exe after download attempt."
        exit 1
    }
}

# 2. PMTILES
$PmtilesCmd = "pmtiles"
if (-not (Get-Command "pmtiles" -ErrorAction SilentlyContinue)) {
    $LocalPmtilesRoot = Join-Path $ScriptDir "pmtiles.exe"
    
    # Check if we have it anywhere (recurse)
    $FoundPmtiles = Get-ChildItem -Path $ScriptDir -Include "pmtiles.exe", "go-pmtiles.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

    if (-not $FoundPmtiles) {
        Install-Tool "pmtiles" $PmtilesUrl $ScriptDir
        $FoundPmtiles = Get-ChildItem -Path $ScriptDir -Include "pmtiles.exe", "go-pmtiles.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    }
    
    if ($FoundPmtiles) {
        $PmtilesCmd = $FoundPmtiles.FullName
        Write-Host "Using local pmtiles: $PmtilesCmd" -ForegroundColor Green
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

$ConfigFile = Resolve-Path (Join-Path $ScriptDir "config.json")
$ProcessFile = Resolve-Path (Join-Path $ScriptDir "process.lua")
$OutputMbtiles = Join-Path $OutputDir "tiles.mbtiles"
$Simplification = "" # Optional

# Create temp store dir if needed
$StoreDir = Join-Path $ScriptDir "store"
New-Item -ItemType Directory -Force -Path $StoreDir | Out-Null

# Use absolute paths for everything to avoid confusion
$AbsInput = Resolve-Path $InputFile
$AbsOutput = $OutputMbtiles # Can't resolve non-existent
$AbsConfig = $ConfigFile
$AbsProcess = $ProcessFile
$AbsStore = $StoreDir

Write-Host "Running Tilemaker..."
& $TilemakerCmd --input $AbsInput --output $AbsOutput --config $AbsConfig --process $AbsProcess --store $AbsStore --verbose

if (-not (Test-Path $OutputMbtiles)) {
    Write-Error "Tile generation failed. Output file not found."
    exit 1
}

# ============================================================================
# STEP 3: CONVERT TO PMTILES
# ============================================================================
Write-Host "`nStep 3: Converting to PMTiles..." -ForegroundColor Green

$OutputPmtiles = Join-Path $OutputDir "serbia.pmtiles"

if (Test-Path $PmtilesCmd) {
    & $PmtilesCmd convert $OutputMbtiles $OutputPmtiles
}
elseif (Get-Command "pmtiles" -ErrorAction SilentlyContinue) {
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
    Write-Host "Deployed to: $WebsiteMapDir\serbia.pmtiles" -ForegroundColor Cyan
}

Write-Host "`nDONE! Tile generation complete." -ForegroundColor Green
