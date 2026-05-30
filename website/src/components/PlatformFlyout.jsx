import React from 'react';

/**
 * PlatformFlyout — a liquid-glass flyout of square "tech tiles" for filtering
 * the map by qubit platform. Multi-select: any number of tiles can be active;
 * the map shows markers whose platforms intersect the union of active tiles.
 * No tiles active = show all.
 *
 * Props:
 *   open       — whether the flyout is visible
 *   active     — array of active group keys
 *   onToggle   — (groupKey) => void
 *   counts     — { rawPlatformValue: number } for showing per-tile counts
 */

// Grouping of raw platform values into user-facing categories.
// Rydberg arrays fold into Neutral Atoms; NV folds into Color Centers.
export const PLATFORM_GROUPS = [
    { key: 'trapped_ion', label: 'Trapped Ions', values: ['trapped_ion'] },
    { key: 'neutral_atom', label: 'Neutral Atoms', values: ['neutral_atom', 'rydberg_array'] },
    { key: 'superconducting', label: 'Superconducting', values: ['superconducting'] },
    { key: 'photonic', label: 'Photonic', values: ['photonic'] },
    { key: 'color_center', label: 'Color Centers', values: ['nv_center', 'color_center'] },
    { key: 'quantum_dot', label: 'Quantum Dots', values: ['quantum_dot'] },
    { key: 'trapped_molecule', label: 'Trapped Molecules', values: ['trapped_molecule'] },
    { key: 'silicon_spin', label: 'Silicon Spin', values: ['silicon_spin'] },
    { key: 'cavity_qed_hybrid', label: 'Hybrid / Cavity QED', values: ['cavity_qed_hybrid'] },
];

// ── Custom line-art platform icons (24×24, stroke = currentColor) ───────────
const ICON = {
    // Surface (chip) ion trap: segmented electrodes + a single charged atomic ion
    // floating above. The ring-with-"+" marks one positive atomic ion (not a molecule).
    trapped_ion: (
        <>
            <circle cx="12" cy="7" r="3" />
            <path d="M12 5.6 V8.4 M10.6 7 H13.4" />
            <rect x="3.4" y="15.4" width="3.2" height="3" rx="0.6" />
            <rect x="7.9" y="15.4" width="3.2" height="3" rx="0.6" />
            <rect x="12.9" y="15.4" width="3.2" height="3" rx="0.6" />
            <rect x="17.4" y="15.4" width="3.2" height="3" rx="0.6" />
            <path d="M3 20 H21" />
        </>
    ),
    // Optical-tweezer array: 3×3 grid of atoms
    neutral_atom: (
        <>
            {[6, 12, 18].map(y => [6, 12, 18].map(x => (
                <circle key={`${x}-${y}`} cx={x} cy={y} r="1.7" fill="currentColor" stroke="none" />
            )))}
        </>
    ),
    // Transmon: a Josephson junction (boxed ×) shunted by a capacitor (two plates),
    // wired in a loop — the canonical superconducting-qubit circuit symbol.
    superconducting: (
        <>
            <path d="M8 5.5 H16 M8 18.5 H16" />
            <path d="M8 5.5 V10" />
            <path d="M5.5 10 H10.5 M5.5 12.4 H10.5" />
            <path d="M8 12.4 V18.5" />
            <path d="M16 5.5 V9" />
            <path d="M14 9 H18 V13 H14 Z" />
            <path d="M14 9 L18 13 M18 9 L14 13" />
            <path d="M16 13 V18.5" />
        </>
    ),
    // Photon: a propagating wave-packet (Feynman wavy line) with a direction arrow.
    photonic: (
        <>
            <path d="M2 13 Q5 6 8 13 T14 13 T20 13" />
            <path d="M18.3 11 L20.6 13 L18.3 15" />
        </>
    ),
    // Color center: lattice ring of atoms with a bright vacancy at the centre
    color_center: (
        <>
            <path d="M12 4.5 L18.5 8.2 V15.8 L12 19.5 L5.5 15.8 V8.2 Z" />
            {[[12, 4.5], [18.5, 8.2], [18.5, 15.8], [12, 19.5], [5.5, 15.8], [5.5, 8.2]].map(([x, y], i) => (
                <circle key={i} cx={x} cy={y} r="1.3" fill="currentColor" stroke="none" />
            ))}
            <circle cx="12" cy="12" r="2.4" fill="currentColor" stroke="none" />
        </>
    ),
    // Quantum dot: confined box with discrete energy levels
    quantum_dot: (
        <>
            <rect x="5" y="5" width="14" height="14" rx="3" />
            <path d="M9 9.5 H15" />
            <path d="M9 12 H15" />
            <path d="M9 14.5 H15" />
        </>
    ),
    // Trapped molecule: a diatomic pair (two bonded atoms) inside a trapping well
    trapped_molecule: (
        <>
            <path d="M4 9 Q12 21 20 9" />
            <circle cx="9.5" cy="11" r="2" fill="currentColor" stroke="none" />
            <circle cx="14.5" cy="11" r="2" fill="currentColor" stroke="none" />
            <path d="M11.5 11 H12.5" strokeWidth="1.9" />
        </>
    ),
    // Silicon spin: spin-up arrow inside a potential well
    silicon_spin: (
        <>
            <rect x="5" y="5" width="14" height="14" rx="3" />
            <path d="M12 16 V8.5" />
            <path d="M9.5 11 L12 8.2 L14.5 11" />
        </>
    ),
    // Cavity QED hybrid: an atom between two cavity mirrors with photons
    cavity_qed_hybrid: (
        <>
            <path d="M6 5 Q3 12 6 19" />
            <path d="M18 5 Q21 12 18 19" />
            <circle cx="12" cy="12" r="2.2" fill="currentColor" stroke="none" />
            <circle cx="8.5" cy="12" r="0.9" fill="currentColor" stroke="none" />
            <circle cx="15.5" cy="12" r="0.9" fill="currentColor" stroke="none" />
        </>
    ),
};

function PlatformIcon({ name }) {
    return (
        <svg viewBox="0 0 24 24" width="28" height="28" fill="none"
            stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
            {ICON[name]}
        </svg>
    );
}

export default function PlatformFlyout({ open, active, onToggle, counts = {} }) {
    return (
        <div className={`platform-flyout ${open ? 'is-open' : ''}`} role="menu" aria-hidden={!open}>
            <div className="platform-flyout-title">
                Platforms
                {active.length > 0 && <span className="platform-flyout-count">{active.length} selected</span>}
            </div>
            <div className="platform-grid">
                {PLATFORM_GROUPS.map(g => {
                    const n = g.values.reduce((s, v) => s + (counts[v] || 0), 0);
                    const isActive = active.includes(g.key);
                    return (
                        <button
                            key={g.key}
                            className={`platform-tile ${isActive ? 'is-active' : ''}`}
                            onClick={() => onToggle(g.key)}
                            title={`${g.label} — ${n} on map`}
                            aria-pressed={isActive}
                        >
                            <span className="platform-tile-icon"><PlatformIcon name={g.key} /></span>
                            <span className="platform-tile-label">{g.label}</span>
                            {n > 0 && <span className="platform-tile-count">{n}</span>}
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
