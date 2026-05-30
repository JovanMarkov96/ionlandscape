// website/src/components/PersonPanel.jsx
import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import Link from '@docusaurus/Link';
import FeedbackForm from './FeedbackForm';
import NobelMedal from './NobelMedal';

/**
 * PersonPanel Component
 * 
 * Displays detailed information about a selected researcher/group
 * fetched from `people.json`.
 * 
 * Features:
 * - Shows Bio, Affiliations, Education, Postdocs
 * - Displays active research tags (Labels, Ion Species) with links to filter on Groups page
 * - Includes a "Back" button (Close) to return to the map
 * 
 * @param {Object} props
 * @param {string} props.personId - ID or md_filename of the person to display
 * @param {Object} [props.location] - Selected map location (unused in typical fallback scope)
 * @param {Function} props.onPersonSelect - Callback to select another person from within the profile
 * @param {Function} props.onCompanySelect - Callback to select a company from an affiliation link
 * @param {Function} props.onClose - Callback to close the panel
 * @returns {JSX.Element|null} Person Profile visual component
 */
function PersonPanel({ personId, location, onPersonSelect, onCompanySelect, onInstitutionSelect, onClose, onShowInMap }) {
    const [people, setPeople] = useState([]);
    const [person, setPerson] = useState(null);
    const [mdBody, setMdBody] = useState("");
    const [companies, setCompanies] = useState([]);
    const [institutions, setInstitutions] = useState([]);

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

        // Fetch institutions for linking
        fetch('/ionlandscape/data/institutions.json')
            .then(res => res.json())
            .then(setInstitutions)
            .catch(() => {
                fetch('/data/institutions.json')
                    .then(res => res.json())
                    .then(setInstitutions)
                    .catch(e => console.warn("Could not load institutions.json", e));
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

    /**
     * Resolves an advisor name string into an interactive profile link if 
     * the advisor exists in the known `people.json` dataset.
     * 
     * @param {string} advisorName - Real name or ID string
     * @returns {JSX.Element} A clickable link or plain text span fallback
     */
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

    /**
     * Resolves a company or institution name string into an interactive profile link if
     * the entity exists in the known datasets. Uses fuzzy matching.
     * 
     * @param {string} entityName - Company or Institution name, acronym, or entity ID
     * @returns {JSX.Element} A clickable link or plain text span fallback
     */
    const renderEntityLink = (entityName) => {
        if (!entityName) return null;

        // Normalize: lowercase, strip punctuation/brackets, collapse whitespace
        const normalize = (s) => (s || '').toLowerCase().replace(/[().,\-–—/]/g, ' ').replace(/\s+/g, ' ').trim();
        const ne = normalize(entityName);
        // Acronyms in the person's institution string, e.g. "(NIST)", "(SKKU)"
        const acronyms = (entityName.match(/\b[A-Z]{2,}\b/g) || []).map(a => a.toLowerCase());

        const matchesInst = (i) => {
            if (!i.name) return false;
            const ni = normalize(i.name);
            if (ni === ne) return true;
            if (i.id === entityName) return true;
            if (i.aliases && i.aliases.some(a => normalize(a) === ne)) return true;
            if (i.abbreviations && i.abbreviations.some(a => acronyms.includes(a.toLowerCase()))) return true;
            // One name fully contains the other (guard against trivially short names)
            if (ni.length > 6 && ne.includes(ni)) return true;
            if (ne.length > 6 && ni.includes(ne)) return true;
            // Shared distinctive acronym appears as a token in the institution name
            const niTokens = ni.split(' ');
            if (acronyms.some(a => a.length >= 3 && niTokens.includes(a))) return true;
            return false;
        };

        // Try Institution first
        const inst = institutions.find(matchesInst);

        if (inst && onInstitutionSelect) {
            return (
                <span
                    className="advisor-link"
                    onClick={() => onInstitutionSelect(inst.md_filename)}
                    title="Open Institution Profile"
                >
                    {entityName}
                </span>
            );
        }

        // Try Company
        const comp = companies.find(c =>
            (c.name && c.name.toLowerCase() === entityName.toLowerCase()) ||
            (c.id === entityName) ||
            (c.name && c.name.toLowerCase().includes(entityName.toLowerCase()) && entityName.length > 3)
        );

        if (comp && onCompanySelect) {
            return (
                <span
                    className="advisor-link" // reusing style
                    onClick={() => onCompanySelect(comp.md_filename)}
                    title="Open Company Profile"
                >
                    {entityName}
                </span>
            );
        }
        return <span>{entityName}</span>;
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
        return null;
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
                <h2>{person.name}<NobelMedal prize={person.nobel_prize} size="0.7em" /></h2>
            </div>
            <p className="person-panel-position">
                <em>{person.current_position && person.current_position.title} — {person.current_position && renderEntityLink(person.current_position.institution)}</em>
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

                    const humanize = (p) => p.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

                    return (
                        <a
                            key={i}
                            href={`/ionlandscape/groups?category=${encodeURIComponent(categoryParam)}`}
                            className={`badge ${categoryParam === 'Trapped Ions' ? 'badge-trapped-ions' : categoryParam === 'Neutral Atoms' ? 'badge-neutral-atoms' : 'badge--info'}`}
                        >
                            {humanize(platform)}
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
                            <strong>{renderEntityLink(aff.name)}</strong> — {aff.role}
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
                                    <div className="trajectory-title">{edu.degree} — {renderEntityLink(edu.institution)}</div>
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
                                    <div className="trajectory-title">{renderEntityLink(pd.institution)}</div>
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
            <div className="links-list" style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                {person.links && person.links.homepage ? (
                    <a href={person.links.homepage} target="_blank" rel="noopener noreferrer" className="badge badge--secondary link-badge">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" /></svg>
                        Homepage
                    </a>
                ) : null}
                {person.links && person.links.google_scholar ? (
                    <a href={person.links.google_scholar} target="_blank" rel="noopener noreferrer" className="badge badge--secondary link-badge">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 3L1 9l11 6 9-4.91V17h2V9M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z" /></svg>
                        Google Scholar
                    </a>
                ) : null}
                {person.links && person.links.orcid ? (
                    <a href={person.links.orcid} target="_blank" rel="noopener noreferrer" className="badge badge--secondary link-badge">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zM7.369 4.378c.525 0 .947.431.947.947s-.422.947-.947.947a.95.95 0 0 1-.947-.947c0-.525.422-.947.947-.947zm-.722 3.038h1.444v10.041H6.647V7.416zm3.562 0h3.9c3.712 0 5.344 2.653 5.344 5.025 0 2.578-2.016 5.025-5.325 5.025h-3.919V7.416zm1.444 1.306v7.444h2.297c1.472 0 2.453-.941 2.453-3.712 0-2.316-.909-3.731-2.434-3.731h-2.316z" /></svg>
                        ORCID
                    </a>
                ) : null}
            </div>

            {/* Show in Map */}
            {person.location?.lat && person.location?.lon && onShowInMap && (
                <>
                    <div className="panel-divider" />
                    <button
                        className="show-in-map-btn"
                        onClick={() => onShowInMap(person.location.lat, person.location.lon)}
                    >
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" /></svg>
                        Show in Map
                    </button>
                </>
            )}

            {/* Feedback Form below all content */}
            <div style={{ marginTop: '30px', marginBottom: '10px', display: 'flex', justifyContent: 'flex-start' }}>
                <FeedbackForm
                    entityType="Person"
                    entityName={person.name}
                    entityId={person.md_filename}
                />
            </div>
        </div>
    );
}

export default PersonPanel;
