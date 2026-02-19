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
function PersonPanel({ personId, location, onPersonSelect, onCompanySelect, onClose }) {
    const [people, setPeople] = useState([]);
    const [person, setPerson] = useState(null);
    const [mdBody, setMdBody] = useState("");
    const [companies, setCompanies] = useState([]);

    useEffect(() => {
        // Fetch people
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

        // Fetch companies for linking
        fetch('/ionlandscape/data/companies.json')
            .then(res => res.json())
            .then(setCompanies)
            .catch(() => {
                fetch('/data/companies.json')
                    .then(res => res.json())
                    .then(setCompanies)
                    .catch(e => console.warn("Could not load companies.json", e));
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
                    className="advisor-link"
                    onClick={() => onPersonSelect(advisor.md_filename)}
                >
                    {advisorName}
                </span>
            );
        }
        return <span>{advisorName}</span>;
    };

    const renderCompanyLink = (companyName) => {
        if (!companyName) return null;

        // Exact or fuzzy match logic
        // companies have 'name', 'id'
        const comp = companies.find(c =>
            (c.name && c.name.toLowerCase() === companyName.toLowerCase()) ||
            (c.id === companyName) ||
            (c.name && c.name.toLowerCase().includes(companyName.toLowerCase()) && companyName.length > 3) // Basic partial match
        );

        // Note: We need onCompanySelect passed to PersonPanel
        // If passed, use it.
        if (comp && onCompanySelect) {
            return (
                <span
                    className="advisor-link" // reusing style
                    onClick={() => onCompanySelect(comp.md_filename)}
                    title="Open Company Profile"
                >
                    {companyName}
                </span>
            );
        }
        return <span>{companyName}</span>;
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
            <div className="location-view-container">
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
            <div className="panel-empty-state">
                <h3>Ion Landscape</h3>
                <p>Click a marker on the map to view a person profile.</p>
            </div>
        );
    }

    // 3. Person Profile View
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
            <div className="person-panel-header">
                <h2>{person.name}</h2>
            </div>
            <p className="person-panel-position">
                <em>{person.current_position && person.current_position.title} — {person.current_position && person.current_position.institution}</em>
            </p>
            {(person.keywords || []).length > 0 && (
                <p className="person-panel-keywords"><strong>Keywords:</strong> {person.keywords.join(', ')}</p>
            )}

            <div className="person-panel-badges">
                {/* Platforms as Badges */}
                {person.platforms && person.platforms.map((platform, i) => {
                    const getCategory = (p) => {
                        const lower = p.toLowerCase();
                        if (lower.includes('neutral')) return 'Neutral Atoms';
                        if (lower.includes('ion')) return 'Trapped Ions';
                        return p;
                    };
                    const categoryParam = getCategory(platform);

                    return (
                        <a
                            key={i}
                            href={`/ionlandscape/groups?category=${encodeURIComponent(categoryParam)}`}
                            className={`badge ${categoryParam === 'Trapped Ions' ? 'badge-trapped-ions' : categoryParam === 'Neutral Atoms' ? 'badge-neutral-atoms' : 'badge--info'}`}
                        >
                            {platform}
                        </a>
                    )
                })}
                {/* Existing Labels */}
                {person.labels && person.labels.map((label, i) => (
                    <Link
                        key={i}
                        to={`/groups?label=${encodeURIComponent(label)}`}
                        className="badge badge--primary margin-right--xs"
                        style={{ textDecoration: 'none', color: 'white' }}
                    >
                        {label}
                    </Link>
                ))}
                {person.ion_species?.map(s => (
                    <Link
                        key={s}
                        to={`/groups?ion=${encodeURIComponent(s)}`}
                        className="badge badge--secondary margin-right--xs"
                    >
                        {s}
                    </Link>
                ))}
            </div>

            {person.affiliations && person.affiliations.length > 0 && (
                <div className="affiliation-box">
                    <h4 className="affiliation-header">Affiliations</h4>
                    {person.affiliations.map((aff, i) => (
                        <div key={i} className="affiliation-item">
                            <strong>{renderCompanyLink(aff.name)}</strong> — {aff.role}
                        </div>
                    ))}
                </div>
            )}

            <div className="panel-divider" />
            <div className="person-bio">
                <ReactMarkdown>{mdBody}</ReactMarkdown>
            </div>

            {(person.education?.length > 0 || person.postdocs?.length > 0) && (
                <>
                    <div className="panel-divider" />
                    <h3>Academic Trajectory</h3>

                    {person.education && person.education.length > 0 && (
                        <div className="education-section-container">
                            <h4 className="section-header">Education</h4>
                            {person.education.map((edu, idx) => (
                                <div key={idx} className="trajectory-item">
                                    <div className="trajectory-title">{edu.degree} — {edu.institution}</div>
                                    <div className="trajectory-details">
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
                            <h4 className="section-header">Postdoctoral Training</h4>
                            {person.postdocs.map((pd, idx) => (
                                <div key={idx} className="trajectory-item">
                                    <div className="trajectory-title">{pd.institution}</div>
                                    <div className="trajectory-details">
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

            <div className="panel-divider" />
            <h4 className="section-header">Links</h4>
            <div className="links-list">
                {person.links && person.links.homepage ? <a href={person.links.homepage} target="_blank" rel="noopener noreferrer" className="panel-link">🏠 Homepage</a> : null}
                {person.links && person.links.google_scholar ? <a href={person.links.google_scholar} target="_blank" rel="noopener noreferrer" className="panel-link">📚 Google Scholar</a> : null}
                {person.links && person.links.orcid ? <a href={person.links.orcid} target="_blank" rel="noopener noreferrer" className="panel-link">🔬 ORCID</a> : null}
            </div>
        </div>
    );
}

export default PersonPanel;
