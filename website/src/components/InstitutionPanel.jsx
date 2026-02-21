// website/src/components/InstitutionPanel.jsx
import React, { useEffect, useState } from 'react';
import Link from '@docusaurus/Link';

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
function InstitutionPanel({ institutionId, onPersonSelect, onClose }) {
    const [institutions, setInstitutions] = useState([]);
    const [people, setPeople] = useState([]);
    const [institution, setInstitution] = useState(null);
    const [showAlumni, setShowAlumni] = useState(false);

    useEffect(() => {
        // Fetch institutions
        fetch('/ionlandscape/data/institutions.json')
            .then(res => res.json())
            .then(setInstitutions)
            .catch(() => {
                fetch('/data/institutions.json')
                    .then(res => res.json())
                    .then(setInstitutions)
                    .catch(e => console.warn("Could not load institutions.json", e));
            });

        // Fetch people for name lookups in directories
        fetch('/ionlandscape/data/people.json')
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
                    {p.name}
                </span>
            );
        }
        return <span key={pid} style={{ display: 'block', marginBottom: '4px' }}>{pid}</span>;
    };

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

            <div className="person-panel-header" style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                {media?.logo_path ? (
                    <img
                        src={media.logo_path.startsWith('http') ? media.logo_path : `/ionlandscape${media.logo_path}`}
                        alt={`${name} logo`}
                        style={{ width: '50px', height: '50px', objectFit: 'contain', backgroundColor: 'white', padding: '4px', borderRadius: '4px' }}
                        onError={(e) => {
                            if (e.target.src.includes('/ionlandscape')) {
                                e.target.src = media.logo_path;
                            }
                        }}
                    />
                ) : (
                    <div style={{
                        width: '50px', height: '50px',
                        backgroundColor: 'var(--institution-color, #14B8A6)',
                        color: 'white',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: '24px', fontWeight: 'bold', borderRadius: '4px'
                    }}>
                        {name.charAt(0)}
                    </div>
                )}
                <h2 style={{ margin: 0 }}>{name}</h2>
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

            {directory && directory.member_count > 0 && (
                <>
                    <div className="panel-divider" />
                    <h4 className="section-header">Current Members ({directory.member_count})</h4>
                    <div style={{ margin: '10px 0' }}>
                        {directory.current_members.map(pid => renderPersonLink(pid))}
                    </div>
                </>
            )}

            {directory && directory.alumni_count > 0 && (
                <>
                    <div className="panel-divider" />
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }} onClick={() => setShowAlumni(!showAlumni)}>
                        <h4 className="section-header" style={{ margin: 0 }}>Alumni ({directory.alumni_count})</h4>
                        <span>{showAlumni ? '▲' : '▼'}</span>
                    </div>
                    {showAlumni && (
                        <div style={{ margin: '10px 0', maxHeight: '200px', overflowY: 'auto' }}>
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
                    <ul style={{ fontSize: '0.8em', paddingLeft: '20px' }}>
                        {sources.map((src, i) => (
                            <li key={i}>
                                <a href={src.url} target="_blank" rel="noopener noreferrer">Source {i + 1}</a>
                                {src.note && `: ${src.note}`}
                            </li>
                        ))}
                    </ul>
                </>
            )}
        </div>
    );
}

export default InstitutionPanel;
