// website/src/components/PersonPanel.jsx
import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import Link from '@docusaurus/Link';

/**
 * PersonPanel Component
 * 
 * Displays detailed information about a selected researcher/group.
 * fetched from `people.json`.
 * 
 * Features:
 * - Shows Bio, Affiliations, Education, Postdocs.
 * - Displays active research tags (Labels, Ion Species) with links to filter on Groups page.
 * - Includes a "Back" button (Close) to return to the map.
 * 
 * @param {Object} props
 * @param {string} props.personId - ID or md_filename of the person to display
 * @param {Function} props.onClose - Callback to close the panel
 */
function PersonPanel({ personId, location, onPersonSelect, onClose }) {
    const [people, setPeople] = useState([]);
    const [person, setPerson] = useState(null);
    const [mdBody, setMdBody] = useState("");

    useEffect(() => {
        fetch('/ionlandscape/data/people.json')
            .then(res => res.json())
            .then(setPeople)
            .catch(err => {
                // fallback
                fetch('/data/people.json')
                    .then(res => res.json())
                    .then(setPeople)
                    .catch(e => console.warn("Could not load people.json", e));
            });
    }, []);

    useEffect(() => {
        if (!personId) {
            setPerson(null);
            setMdBody("");
            return;
        }
        // personId is stored as md_filename by MapPanel. Find the object.
        const p = people.find(x => x.md_filename === personId) || people.find(x => x.id === personId);
        if (p) {
            setPerson(p);
            // Use the short_bio from JSON instead of fetching raw markdown
            setMdBody(p.short_bio || "No biography available.");
        } else {
            setPerson(null);
        }
    }, [personId, people]);

    // Helper to render advisor link or text
    const renderAdvisor = (advisorName) => {
        if (!advisorName) return null;

        const advisor = people.find(p =>
            (p.name && p.name.toLowerCase() === advisorName.toLowerCase()) ||
            (p.sort_name && p.sort_name.toLowerCase() === advisorName.toLowerCase()) ||
            (p.id === advisorName)
        );

        if (advisor && onPersonSelect) {
            return (
                <span
                    style={{ color: '#007bff', cursor: 'pointer', textDecoration: 'underline' }}
                    onClick={() => onPersonSelect(advisor.md_filename)}
                >
                    {advisorName}
                </span>
            );
        }
        return <span>{advisorName}</span>;
    };

    const handleClose = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (onClose) onClose();
    };

    // --- Content Rendering Checks ---

    // 1. Location View (No person selected, but location selected)
    if (location && !person) {
        return (
            <div style={{ padding: 16, position: 'relative' }}>
                {onClose && (
                    <button
                        className="close-panel-btn"
                        onClick={handleClose}
                        aria-label="Close location view"
                    >
                        ✕
                    </button>
                )}
                <h3>{location.city}, {location.country}</h3>
                <p>People at this location (click a marker):</p>
                {/* List people at this location if desired */}
            </div>
        );
    }

    // 2. Initial / Empty View
    if (!person) {
        return (
            <div style={{ padding: 16 }}>
                <h3>Ion Landscape</h3>
                <p>Click a marker on the map to view a person profile.</p>
            </div>
        );
    }

    // 3. Person Profile View
    return (
        <div style={{ padding: 16, position: 'relative' }}>
            {onClose && (
                <button
                    className="close-panel-btn"
                    onClick={handleClose}
                    aria-label="Close profile"
                >
                    ✕
                </button>
            )}
            <div className="person-panel-header">
                <h2>{person.name}</h2>
            </div>
            <p><em>{person.current_position && person.current_position.title} — {person.current_position && person.current_position.institution}</em></p>
            <p><strong>Platforms:</strong> {(person.platforms || []).join(', ')}</p>
            <p><strong>Keywords:</strong> {(person.keywords || []).join(', ')}</p>

            <div style={{ marginBottom: 12 }}>
                {person.labels?.map(l => (
                    <Link
                        key={l}
                        to={`/groups?label=${encodeURIComponent(l)}`}
                        className="badge badge--primary margin-right--xs"
                        style={{ textDecoration: 'none', color: 'white' }}
                    >
                        {l}
                    </Link>
                ))}
                {person.ion_species?.map(s => (
                    <Link
                        key={s}
                        to={`/groups?ion=${encodeURIComponent(s)}`}
                        className="badge badge--secondary margin-right--xs"
                        style={{ textDecoration: 'none', color: 'black' }}
                    >
                        {s}
                    </Link>
                ))}
            </div>

            {person.affiliations && person.affiliations.length > 0 && (
                <div style={{ marginTop: 12, marginBottom: 12, padding: '8px 12px', backgroundColor: '#f5f5f5', borderRadius: 4 }}>
                    <h4 style={{ margin: '0 0 4px 0', fontSize: '1em', color: '#333' }}>Affiliations</h4>
                    {person.affiliations.map((aff, i) => (
                        <div key={i} style={{ fontSize: '0.9em' }}>
                            <strong>{aff.name}</strong> — {aff.role}
                        </div>
                    ))}
                </div>
            )}

            <hr />
            <div className="person-bio">
                <ReactMarkdown>{mdBody}</ReactMarkdown>
            </div>

            {(person.education?.length > 0 || person.postdocs?.length > 0) && (
                <>
                    <hr />
                    <h3>Academic Trajectory</h3>

                    {person.education && person.education.length > 0 && (
                        <div style={{ marginBottom: 16 }}>
                            <h4 style={{ marginBottom: 8, fontSize: '1.1em', color: '#555' }}>Education</h4>
                            {person.education.map((edu, idx) => (
                                <div key={idx} style={{ marginBottom: 12, paddingLeft: 8, borderLeft: '2px solid #eee' }}>
                                    <div style={{ fontWeight: 600 }}>{edu.degree} — {edu.institution}</div>
                                    <div style={{ fontSize: '0.9em', color: '#666' }}>
                                        {edu.year && <span>({edu.year}) </span>}
                                        {edu.advisor && (
                                            <>
                                                Advisor: {renderAdvisor(edu.advisor)}
                                            </>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {person.postdocs && person.postdocs.length > 0 && (
                        <div>
                            <h4 style={{ marginBottom: 8, fontSize: '1.1em', color: '#555' }}>Postdoctoral Training</h4>
                            {person.postdocs.map((pd, idx) => (
                                <div key={idx} style={{ marginBottom: 12, paddingLeft: 8, borderLeft: '2px solid #eee' }}>
                                    <div style={{ fontWeight: 600 }}>{pd.institution}</div>
                                    <div style={{ fontSize: '0.9em', color: '#666' }}>
                                        {pd.advisor && (
                                            <>
                                                Advisor: {renderAdvisor(pd.advisor)}
                                            </>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </>
            )}

            <hr />
            <p><strong>Links</strong></p>
            <ul style={{ paddingLeft: 20 }}>
                {person.links && person.links.homepage ? <li><a href={person.links.homepage} target="_blank" rel="noopener noreferrer">Homepage</a></li> : null}
                {person.links && person.links.google_scholar ? <li><a href={person.links.google_scholar} target="_blank" rel="noopener noreferrer">Google Scholar</a></li> : null}
                {person.links && person.links.orcid ? <li><a href={person.links.orcid} target="_blank" rel="noopener noreferrer">ORCID</a></li> : null}
            </ul>
        </div>
    );
}

export default PersonPanel;
