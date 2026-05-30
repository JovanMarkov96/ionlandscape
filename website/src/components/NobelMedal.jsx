import React from 'react';

/**
 * NobelMedal — inline gold medallion shown after a Nobel laureate's name.
 *
 * Renders nothing unless `prize` is provided (the person's `nobel_prize`
 * frontmatter object: { year, category }).
 */
export default function NobelMedal({ prize, size = '0.85em' }) {
    if (!prize) return null;
    const label = `Nobel Laureate in ${prize.category || 'Physics'}${prize.year ? `, ${prize.year}` : ''}`;
    return (
        <img
            src="/ionlandscape/img/nobel-medal.png"
            className="nobel-medal"
            style={{ width: size, height: size }}
            alt="🏅"
            title={label}
            aria-label={label}
        />
    );
}
