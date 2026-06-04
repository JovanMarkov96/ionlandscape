// website/src/components/InstitutionPanel.jsx
import React, { useEffect, useState } from 'react';
import Link from '@docusaurus/Link';
import FeedbackForm from './FeedbackForm';
import NobelMedal from './NobelMedal';

/**
 * Produce a clean, professional label for a source reference.
 * Wikipedia URLs -> "Wikipedia"; otherwise the bare hostname (e.g. "au.dk").
 */
export function formatSourceLabel(src) {
    const url = src?.url || '';
    if (/wikipedia\.org/i.test(url)) return 'Wikipedia';
    try {
        const host = new URL(url).hostname.replace(/^www\./, '');
        return host || 'Official source';
    } catch (e) {
        // Fall back to a cleaned note if URL is unparseable
        const note = (src?.note || '').replace(/^Imported short_description from\s*/i, '').trim();
        return note || 'Source';
    }
}

/**
 * InstitutionPanel Component
 * 
 * Displays detailed information about a selected institution.
 * 
 * @param {Object} props
 * @param {string} props.institutionId - ID or md_filename of the institution to display
 * @param {Function} props.onPersonSelect - Callback to select a person from the membership lists
 * @param {Function} props.onClose - Callback to close the panel
 * @returns {JSX.Element|null} Institution Profile visual component
 */
function InstitutionPanel({ institutionId, onPersonSelect, onClose, onShowInMap }) {
    const [institutions, setInstitutions] = useState([]);
    const [people, setPeople] = useState([]);
    const [institution, setInstitution] = useState(null);
    const [showAlumni, setShowAlumni] = useState(false);

    useEffect(() => {
        // Fetch institutions
        fetch('/quantum-landscape/data/institutions.json')
            .then(res => res.json())
            .then(setInstitutions)
            .catch(() => {
                fetch('/data/institutions.json')
                    .then(res => res.json())
                    .then(setInstitutions)
                    .catch(e => console.warn("Could not load institutions.json", e));
            });

        // Fetch people for name lookups in directories
        fetch('/quantum-landscape/data/people.json')
            .then(res => res.json())
            .then(setPeople)
            .catch(() => {
                fetch('/data/people.json')
                    .then(res => res.json())
                    .then(setPeople)
                    .catch(e => console.warn("Could not load people.json", e));
            });
    }, []);

    useEffect(() => {
        if (!institutionId) {
            setInstitution(null);
            setShowAlumni(false);
            return;
        }
        const inst = institutions.find(x => x.md_filename === institutionId) || institutions.find(x => x.id === institutionId);
        setInstitution(inst || null);
        setShowAlumni(false); // reset toggle
    }, [institutionId, institutions]);

    const handleClose = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (onClose) onClose();
    };

    /**
     * Renders a clickable link for a person based on their ID.
     * Falls back to rendering just the ID string if the person is not found in the database.
     * 
     * @param {string} pid - The person ID or md_filename
     * @returns {JSX.Element} The rendered link or text span
     */
    const renderPersonLink = (pid) => {
        const p = people.find(x => x.md_filename === pid || x.id === pid);
        if (p) {
            return (
                <span
                    key={pid}
                    className="advisor-link"
                    onClick={() => onPersonSelect && onPersonSelect(p.md_filename)}
                    style={{ display: 'block', marginBottom: '4px' }}
                >
                    {p.name}<NobelMedal prize={p.nobel_prize} size="0.8em" />
                </span>
            );
        }
        return <span key={pid} style={{ display: 'block', marginBottom: '4px' }}>{pid}</span>;
    };

    // Group current members by platform
    const groupedMembers = React.useMemo(() => {
        if (!institution || !institution.directory || !institution.directory.current_members) return {};
        const groups = {};
        const platformMap = {
            "trapped_ion": "Trapped Ion",
            "neutral_atom": "Neutral Atom",
            "rydberg_array": "Neutral Atom",
            "superconducting": "Superconducting",
            "photonic": "Photonic",
            "nv_center": "Color Center",
            "color_center": "Color Center",
            "quantum_dot": "Semiconductor",
            "silicon_spin": "Semiconductor",
            "topological": "Topological",
            "trapped_molecule": "Molecule",
            "cavity_qed_hybrid": "Hybrid"
        };
        
        institution.directory.current_members.forEach(pid => {
            const p = people.find(x => x.md_filename === pid || x.id === pid);
            if (p && p.platforms && p.platforms.length > 0) {
                const mapped = platformMap[p.platforms[0]] || "Other";
                if (!groups[mapped]) groups[mapped] = [];
                groups[mapped].push(pid);
            } else {
                if (!groups["Other"]) groups["Other"] = [];
                groups["Other"].push(pid);
            }
        });
        return groups;
    }, [institution, people]);

    if (!institution) {
        return null;
    }

    const { name, location, short_description, focus_areas, directory, links, media, sources } = institution;

    return (
        <div className="person-panel-content">
            {onClose && (
                <button
                    className="close-panel-btn"
                    onClick={handleClose}
                    aria-label="Close profile"
                >
                    ✕
                </button>
            )}

            <div className="person-panel-header panel-flex-header" style={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                {media?.logo_path ? (
                    <img
                        src={media.logo_path.startsWith('http') ? media.logo_path : `/quantum-landscape${media.logo_path}`}
                        alt={`${name} logo`}
                        className="institution-logo-img"
                        onError={(e) => {
                            if (e.target.src.includes('/quantum-landscape')) {
                                e.target.src = media.logo_path;
                            }
                        }}
                    />
                ) : (
                    <div className="institution-logo-placeholder">
                        {name.charAt(0)}
                    </div>
                )}
                <h2 style={{ margin: 0, marginLeft: '12px' }}>{name}</h2>
            </div>

            <p className="person-panel-position" style={{ marginTop: '10px' }}>
                <em>{location?.city}{location?.region ? `, ${location.region}` : ''}{location?.country ? `, ${location.country}` : ''}</em>
            </p>

            {short_description && (
                <p>{short_description}</p>
            )}

            {focus_areas && focus_areas.length > 0 && (
                <div className="person-panel-badges">
                    {focus_areas.map((area, i) => (
                        <span key={i} className="badge badge--secondary margin-right--xs" style={{ marginBottom: '5px' }}>
                            {area}
                        </span>
                    ))}
                </div>
            )}

            {institution.directory && institution.directory.member_count > 0 && (
                <>
                    <div className="panel-divider" />
                    <h4 className="section-header">In-House Groups ({institution.directory.member_count})</h4>
                    <div className="scrollable-list-container">
                        {Object.keys(groupedMembers).sort().map(platform => (
                            <div key={platform} style={{ marginBottom: '12px' }}>
                                <strong style={{ fontSize: '0.9em', color: '#666', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                    {platform}
                                </strong>
                                <div style={{ marginTop: '4px', paddingLeft: '8px', borderLeft: '2px solid #eee' }}>
                                    {groupedMembers[platform].map(pid => renderPersonLink(pid))}
                                </div>
                            </div>
                        ))}
                    </div>
                </>
            )}

            {directory && directory.alumni_count > 0 && (
                <>
                    <div className="panel-divider" />
                    <div className="section-collapse-header" onClick={() => setShowAlumni(!showAlumni)}>
                        <h4 className="section-header" style={{ margin: 0 }}>Alumni ({directory.alumni_count})</h4>
                        <span>{showAlumni ? '▲' : '▼'}</span>
                    </div>
                    {showAlumni && (
                        <div className="scrollable-list-container">
                            {directory.alumni.map(pid => renderPersonLink(pid))}
                        </div>
                    )}
                </>
            )}

            {(links?.website || links?.wikipedia) && (
                <>
                    <div className="panel-divider" />
                    <h4 className="section-header">Links</h4>
                    <div className="links-list" style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                        {links.website && (
                            <a href={links.website} target="_blank" rel="noopener noreferrer" className="badge badge--secondary link-badge">
                                Website
                            </a>
                        )}
                        {links.department && (
                            <a href={links.department} target="_blank" rel="noopener noreferrer" className="badge badge--secondary link-badge">
                                Department
                            </a>
                        )}
                        {links.quantum_center && (
                            <a href={links.quantum_center} target="_blank" rel="noopener noreferrer" className="badge badge--secondary link-badge">
                                Quantum Center
                            </a>
                        )}
                        {links.wikipedia && (
                            <a href={links.wikipedia} target="_blank" rel="noopener noreferrer" className="badge badge--secondary link-badge">
                                Wikipedia
                            </a>
                        )}
                    </div>
                </>
            )}

            {sources && sources.length > 0 && (
                <>
                    <div className="panel-divider" />
                    <h4 className="section-header" style={{ fontSize: '0.9em' }}>Sources</h4>
                    <ul className="panel-sources-list">
                        {sources.map((src, i) => (
                            <li key={i}>
                                <a href={src.url} target="_blank" rel="noopener noreferrer">
                                    {formatSourceLabel(src)}
                                </a>
                            </li>
                        ))}
                    </ul>
                </>
            )}

            {/* Show in Map */}
            {location?.lat && location?.lon && onShowInMap && (
                <>
                    <div className="panel-divider" />
                    <button
                        className="show-in-map-btn"
                        onClick={() => onShowInMap(location.lat, location.lon)}
                    >
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" /></svg>
                        Show in Map
                    </button>
                </>
            )}

            {/* Feedback Form below all content */}
            <div style={{ marginTop: '30px', marginBottom: '10px', display: 'flex', justifyContent: 'flex-start' }}>
                <FeedbackForm
                    entityType="Institution"
                    entityName={name}
                    entityId={institutionId}
                />
            </div>
        </div>
    );
}

export default InstitutionPanel;
