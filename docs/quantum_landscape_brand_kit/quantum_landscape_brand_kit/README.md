# Quantum Landscape brand kit

This package contains the selected Quantum Landscape logo system and web-ready assets.

## What is inside

- `png/exact-selected-mark-transparent-*.png`: the closest transparent raster extraction of the selected logo, exported up to **4096 px**.
- `png/exact-wordmark-horizontal-*.png`: high-resolution transparent and card versions of the selected mark with the Quantum Landscape wordmark.
- `svg/quantum-landscape-mark.svg`: an editable clean vector approximation of the selected mark.
- `svg/quantum-landscape-wordmark-horizontal-on-dark.svg` and `...on-light.svg`: transparent vector wordmarks.
- `svg/quantum-landscape-mark-exact-raster-embedded.svg`: SVG wrapper around the exact raster mark. This preserves the exact selected visual but is not a true vector trace.
- `favicon/`: browser icons, including exact-raster favicon variants.
- `brand.css` and `theme-tokens.json`: CSS variables and design tokens.
- `preview/quantum-landscape-brand-board.png`: visual brand board.

## Recommended production use

For the most faithful visual match, use:

- Main site logo mark: `png/exact-selected-mark-transparent-2048.png` or `png/exact-selected-mark-transparent-4096.png`.
- Browser icon: `favicon/favicon-exact.ico` or `favicon/favicon-exact-512.png`.
- Header wordmark on dark UI: `png/exact-wordmark-horizontal-on-dark-transparent-2560.png`.
- Header wordmark on light UI: `png/exact-wordmark-horizontal-on-light-transparent-2560.png`.

For fully scalable editable assets, use the `svg/` files. The clean SVG mark is a vector approximation, not an exact trace of the raster image.

## Typography

- **Wordmark / headings:** Space Grotesk, Sora, or Inter. Recommended first choice: `Space Grotesk`.
- **Body UI:** Inter or Manrope.
- **Technical labels / coordinates:** IBM Plex Mono or JetBrains Mono.

Do not bundle or redistribute font files unless their licenses allow it. Load fonts through your normal web-font pipeline or use system fallbacks.

## Palette

| Token | Hex |
|---|---:|
| Quantum Navy | `#020B1C` |
| Deep Ink | `#071225` |
| Quantum Cyan | `#15D5FF` |
| Azure Blue | `#2E7CFF` |
| Periwinkle | `#6E8CFF` |
| Quantum Violet | `#8A5CF6` |
| Soft Lilac | `#C7B7FF` |
| Paper / light background | `#F6F8FC` |
| Text on dark | `#F7FBFF` |
| Text on light | `#071225` |
| Muted text on dark | `#8EA3C2` |

## Usage notes

- The gradient mark can stay the same in both dark and light mode.
- Use white text `#F7FBFF` on dark navy backgrounds.
- Use deep navy text `#071225` on light backgrounds.
- Keep clear space around the logo equal to at least **25% of the mark height**.
- Below about **160 px total width**, use the mark only and omit the wordmark.
