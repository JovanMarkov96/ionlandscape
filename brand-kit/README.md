# Quantum Landscape Logo Assets v2

This is a corrected logo asset pack for Quantum Landscape.

## Important correction

The earlier SVG approximation used thick strokes and did not match the selected logo. This pack separates the assets clearly:

- `svg/mark-exact-raster-embedded.svg` preserves the selected logo exactly as a cleaned transparent raster embedded inside an SVG wrapper. Use this for the website when you want an SVG file that visually matches the chosen logo.
- `png/mark-transparent-tight-2048.png` and `png/mark-transparent-square-2048.png` are high-resolution transparent PNG exports of the selected logo.
- `svg/mark-vector-clean-approximation.svg` is a clean pure-vector approximation. It is useful for simple icons, monochrome versions, or later manual editing, but it is not claimed to be the exact generated logo.

## Recommended website files

- Header logo on dark UI: `svg/wordmark-horizontal-exact-dark-text.svg`
- Header logo on light UI: `svg/wordmark-horizontal-exact-light-text.svg`
- Logo-only mark: `svg/mark-exact-raster-embedded.svg`
- PNG fallback: `png/mark-transparent-tight-2048.png`
- Favicon: `favicon/favicon.ico`, `favicon/favicon-192.png`, `favicon/apple-touch-icon.png`
- CSS tokens: `brand.css`
- JSON tokens: `theme-tokens.json`

## Colors

- Dark background: `#020B1C`
- Dark-mode text: `#F7FBFF`
- Light-mode text: `#071225`
- Gradient: `#15D5FF -> #2E7CFF -> #6E8CFF -> #8A5CF6`

## Typography

Recommended display font: Space Grotesk or Inter Display.  
Recommended body/UI font: Inter or Manrope.

Font files are not included.

## Notes

The original logo was generated as raster artwork, so a mathematically exact pure-vector reconstruction is not available from the image alone. The exact SVG files therefore embed the cleaned raster logo. This is normal for preserving a generated/painted mark while keeping an SVG-based web workflow.
