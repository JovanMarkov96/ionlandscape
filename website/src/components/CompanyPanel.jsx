// website/src/components/CompanyPanel.jsx
import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import Link from '@docusaurus/Link';

/**
 * CompanyPanel Component
 * 
 * Displays detailed information about a selected company.
 * Fetched from `companies.json`.
 */
function CompanyPanel({ companyId, location, onCompanySelect, onPersonSelect, onClose }) {
    const [companies, setCompanies] = useState([]);
    const [company, setCompany] = useState(null);
    const [people, setPeople] = useState([]);

    useEffect(() => {
        // Fetch people for linking
        fetch('/ionlandscape/data/people.json')
            .then(res => res.json())
            .then(setPeople)
            .catch(() => {
                fetch('/data/people.json')
                    .then(res => res.json())
                    .then(setPeople)
                    .catch(e => console.warn("Could not load people.json", e));
            });

        // Fetch companies
        fetch('/ionlandscape/data/companies.json')
            .then(res => res.json())
            .then(setCompanies)
            .catch(err => {
                // fallback
                fetch('/data/companies.json')
                    .then(res => res.json())
                    .then(setCompanies)
                    .catch(e => console.warn("Could not load companies.json", e));
            });
    }, []);

    useEffect(() => {
        if (!companyId) {
            setCompany(null);
            return;
        }
        // companyId is stored as md_filename by MapPanel. Find the object.
        const c = companies.find(x => x.md_filename === companyId) || companies.find(x => x.id === companyId);
        if (c) {
            setCompany(c);
        } else {
            setCompany(null);
        }
    }, [companyId, companies]);

    const handleClose = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (onClose) onClose();
    };

    // Helper to receive person name/ID and return a link if found
    const renderPersonLink = (name) => {
        if (!name) return name;

        // precise or fuzzy match
        const person = people.find(p =>
            (p.name && p.name.toLowerCase() === name.toLowerCase()) ||
            (p.sort_name && p.sort_name.toLowerCase() === name.toLowerCase()) ||
            (p.id === name)
        );

        if (person && onCompanySelect) { // onCompanySelect is actually handleCompanySelect from index.js
            // We need to switch to Person view. 
            // index.js handleCompanySelect sets selectedCompanyId. 
            // We need a way to select a person.
            // CompanyPanel receives onCompanySelect. It does NOT receive onPersonSelect?
            // Checking index.js:
            // <CompanyPanel ... onCompanySelect={handleCompanySelect} ... />
            // It seems CompanyPanel only gets onCompanySelect.
            // I need to update index.js to pass onPersonSelect to CompanyPanel too!
            // For now I will assume onPersonSelect is passed or I add it.
            // Wait, I should verify index.js again.
            return (
                <span
                    className="advisor-link"
                    onClick={() => onPersonSelect && onPersonSelect(person.md_filename)}
                    title="Open Person Profile"
                >
                    {name}
                </span>
            );
        }
        return name;
    };

    if (!company) return null;

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
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                    {company.media?.logo_path && (
                        <div style={{
                            width: '80px', /* Increased from 60px */
                            height: '80px',
                            borderRadius: '50%',
                            backgroundColor: 'white',
                            border: '1px solid #ddd',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            overflow: 'hidden',
                            flexShrink: 0,
                            boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                        }}>
                            <img
                                src={company.media.logo_path.startsWith('http') ? company.media.logo_path : `/ionlandscape${company.media.logo_path}`}
                                alt={`${company.name} logo`}
                                style={{ width: '100%', height: '100%', objectFit: 'contain', padding: '8px' }}
                                onError={(e) => {
                                    // Try without prefix if failed
                                    if (e.target.src.includes('/ionlandscape')) {
                                        e.target.src = company.media.logo_path;
                                    }
                                }}
                            />
                        </div>
                    )}
                    <h2>{company.name}</h2>
                </div>
            </div>

            <p className="person-panel-position">
                <em>{company.location?.city}, {company.location?.country}</em>
            </p>

            <div className="person-panel-badges">
                {company.platforms && company.platforms.map((platform, i) => (
                    <span key={i} className="badge badge--primary margin-right--xs">
                        {platform}
                    </span>
                ))}
                {company.status?.operating_status === "active" && (
                    <span className="badge badge--success margin-right--xs">Active</span>
                )}
                {company.status?.operating_status === "acquired" && (
                    <span className="badge badge--warning margin-right--xs">Acquired</span>
                )}
            </div>

            <div className="panel-divider" />

            <div className="person-bio">
                <p><strong>{company.short_summary}</strong></p>
            </div>

            {/* Approach */}
            {(company.approach?.elevator_pitch || company.approach?.differentiators) && (
                <>
                    <h4 className="section-header">Approach</h4>
                    {company.approach.elevator_pitch && (
                        <p style={{ fontSize: '0.9em', fontStyle: 'italic' }}>
                            "{company.approach.elevator_pitch}"
                        </p>
                    )}
                    {company.approach.differentiators && (
                        <ul style={{ fontSize: '0.9em' }}>
                            {company.approach.differentiators.map((diff, i) => (
                                <li key={i}>{diff}</li>
                            ))}
                        </ul>
                    )}
                    {company.approach.architecture_tags && (
                        <div style={{ marginBottom: '10px' }}>
                            {company.approach.architecture_tags.map((tag, i) => (
                                <span key={i} className="badge badge--secondary margin-right--xs" style={{ fontSize: '0.8em' }}>
                                    {tag}
                                </span>
                            ))}
                        </div>
                    )}
                </>
            )}

            {/* Funding */}
            {company.funding && (company.funding.total_usd > 0 || company.funding.rounds?.length > 0) && (
                <>
                    <div className="panel-divider" />
                    <h4 className="section-header">Funding</h4>
                    {company.funding.total_usd > 0 && (
                        <p><strong>Total Raised:</strong> ${(company.funding.total_usd / 1000000).toFixed(1)}M</p>
                    )}
                    {company.funding.rounds && company.funding.rounds.map((round, i) => (
                        <div key={i} className="trajectory-item">
                            <div className="trajectory-title">{round.round} — {(round.amount_usd / 1000000).toFixed(1)}M</div>
                            <div className="trajectory-details">
                                {round.date} • Lead: {round.lead_investors?.join(", ")}
                                {round.other_investors?.length > 0 && (
                                    <div style={{ marginTop: '4px' }}>
                                        <details style={{ cursor: 'pointer', color: '#666', fontSize: '0.9em' }}>
                                            <summary style={{ outline: 'none' }}>
                                                + {round.other_investors.length} other investors
                                            </summary>
                                            <div style={{ paddingLeft: '10px', marginTop: '2px', lineHeight: '1.4' }}>
                                                {round.other_investors.join(", ")}
                                            </div>
                                        </details>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </>
            )}

            {/* People */}
            {company.people && (company.people.founders?.length > 0 || company.people.leadership?.length > 0) && (
                <>
                    <div className="panel-divider" />
                    <h4 className="section-header">Leadership</h4>
                    {company.people.founders && company.people.founders.map((p, i) => (
                        <div key={i} className="affiliation-item">
                            <strong>{renderPersonLink(p.name)}</strong> — {p.role}
                        </div>
                    ))}
                    {company.people.spun_out_of && company.people.spun_out_of.length > 0 && (
                        <div className="affiliation-item" style={{ marginTop: '5px' }}>
                            <em>Spun out of: {company.people.spun_out_of.join(", ")}</em>
                        </div>
                    )}
                </>
            )}

            {/* Links */}
            <div className="panel-divider" />
            <h4 className="section-header">Links</h4>
            <div className="links-list" style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                {company.links?.website && (
                    <a href={company.links.website} target="_blank" rel="noopener noreferrer" className="badge badge--secondary" style={{ display: 'flex', alignItems: 'center', gap: '5px', padding: '8px 12px', borderRadius: '20px', textDecoration: 'none' }}>
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z" /></svg>
                        Website
                    </a>
                )}
                {company.links?.news && (
                    <a href={company.links.news} target="_blank" rel="noopener noreferrer" className="badge badge--secondary" style={{ display: 'flex', alignItems: 'center', gap: '5px', padding: '8px 12px', borderRadius: '20px', textDecoration: 'none' }}>
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M22 3c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V3zm-2.5 12.5h-10v-1h10v1zm0-3.5h-10v-1h10v1zm0-3.5h-10v-1h10v1zM6 15.5h2v-7H6v7z" /></svg>
                        News
                    </a>
                )}
                {company.links?.careers && (
                    <a href={company.links.careers} target="_blank" rel="noopener noreferrer" className="badge badge--secondary" style={{ display: 'flex', alignItems: 'center', gap: '5px', padding: '8px 12px', borderRadius: '20px', textDecoration: 'none' }}>
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2z" /></svg>
                        Careers
                    </a>
                )}
            </div>

            {/* Sources */}
            {company.sources && company.sources.length > 0 && (
                <>
                    <div className="panel-divider" />
                    <h4 className="section-header" style={{ fontSize: '0.9em', color: '#666' }}>Evidence Map</h4>
                    <ul style={{ fontSize: '0.8em', color: '#666', paddingLeft: '20px' }}>
                        {company.sources.map((src, i) => (
                            <li key={i}>
                                <a href={src.url} target="_blank" rel="noopener noreferrer" style={{ color: '#666', textDecoration: 'underline' }}>
                                    {src.note}
                                </a>
                            </li>
                        ))}
                    </ul>
                </>
            )}
        </div>
    );
}

export default CompanyPanel;
