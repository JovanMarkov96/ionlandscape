// website/src/components/CompanyPanel.jsx
import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import Link from '@docusaurus/Link';
import FeedbackForm from './FeedbackForm';
import { formatSourceLabel } from './InstitutionPanel';

/**
 * CompanyPanel Component
 * 
 * Displays detailed information about a selected company or startup.
 * Fetches backing data from `companies.json` and supports cross-referencing
 * founders with `people.json`.
 * 
 * @param {Object} props
 * @param {string} props.companyId - ID or md_filename of the company to display
 * @param {Object} [props.location] - Parent location selected object
 * @param {Function} props.onCompanySelect - Callback to select another nested company
 * @param {Function} props.onPersonSelect - Callback to select a person (e.g., founder)
 * @param {Function} props.onClose - Callback to close the panel
 * @returns {JSX.Element|null} Company Profile visual component
 */
function CompanyPanel({ companyId, location, onCompanySelect, onPersonSelect, onInstitutionSelect, onClose, onShowInMap }) {
    const [companies, setCompanies] = useState([]);
    const [company, setCompany] = useState(null);
    const [people, setPeople] = useState([]);
    const [institutions, setInstitutions] = useState([]);

    useEffect(() => {
        // Fetch people for linking
        fetch('/quantum-landscape/data/people.json')
            .then(res => res.json())
            .then(setPeople)
            .catch(() => {
                fetch('/data/people.json')
                    .then(res => res.json())
                    .then(setPeople)
                    .catch(e => console.warn("Could not load people.json", e));
            });

        // Fetch companies
        fetch('/quantum-landscape/data/companies.json')
            .then(res => res.json())
            .then(setCompanies)
            .catch(err => {
                // fallback
                fetch('/data/companies.json')
                    .then(res => res.json())
                    .then(setCompanies)
                    .catch(e => console.warn("Could not load companies.json", e));
            });

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

    /**
     * Attempts to resolve a plain person name into an interactive profile link 
     * by querying the loaded `people.json` cache.
     * 
     * @param {string} name - Name, ID, or sort_name to lookup
     * @returns {JSX.Element|string} A clickable link or the original plain string
     */
    const renderPersonLink = (name) => {
        if (!name) return name;

        // precise or fuzzy match
        const person = people.find(p =>
            (p.name && p.name.toLowerCase() === name.toLowerCase()) ||
            (p.sort_name && p.sort_name.toLowerCase() === name.toLowerCase()) ||
            (p.id === name)
        );

        if (person && onPersonSelect) {
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

    /**
     * Resolves an institution name into an interactive profile link.
     */
    const renderInstitutionLink = (name) => {
        if (!name) return name;

        const inst = institutions.find(i =>
            (i.name && i.name.toLowerCase() === name.toLowerCase()) ||
            (i.id === name) ||
            (i.aliases && i.aliases.some(a => a.toLowerCase() === name.toLowerCase())) ||
            (i.name && i.name.toLowerCase().includes(name.toLowerCase()) && name.length > 3)
        );

        if (inst && onInstitutionSelect) {
            return (
                <span
                    className="advisor-link"
                    onClick={() => onInstitutionSelect(inst.md_filename)}
                    title="Open Institution Profile"
                >
                    {name}
                </span>
            );
        }
        return name;
    };

    if (!company) return null;

    // Humanize underscore_keys for display, with special-casing for acronyms.
    const ACRONYMS = { nv: 'NV', qed: 'QED', ac: 'AC', qpu: 'QPU', gpu: 'GPU', qkd: 'QKD', rf: 'RF' };
    const humanize = (s) => {
        if (!s) return s;
        return s
            .replace(/_/g, ' ')
            .replace(/\b\w+/g, (w) => ACRONYMS[w.toLowerCase()] || (w.charAt(0).toUpperCase() + w.slice(1)));
    };

    // Render a species token like "171Yb+" or "87Rb" with the leading mass number as superscript.
    const formatSpecies = (s) => {
        const m = /^(\d+)(.*)$/.exec(s);
        if (!m) return s;
        return (<><sup>{m[1]}</sup>{m[2]}</>);
    };

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
                <div className="panel-flex-header">
                    {company.media?.logo_path ? (
                        <div className="panel-logo-container">
                            <img
                                src={company.media.logo_path.startsWith('http') ? company.media.logo_path : `/quantum-landscape${company.media.logo_path}`}
                                alt={`${company.name} logo`}
                                onError={(e) => {
                                    if (e.target.src.includes('/quantum-landscape')) {
                                        e.target.src = company.media.logo_path;
                                    }
                                }}
                            />
                        </div>
                    ) : (
                        <div className="panel-logo-placeholder" title="No logo available">
                            {(() => {
                                const nameParts = (company.name || '').split(' ').filter(p => p.trim() !== '');
                                if (nameParts.length > 1) return (nameParts[0][0] + nameParts[1][0]).toUpperCase();
                                if (nameParts.length === 1) return nameParts[0].substring(0, 2).toUpperCase();
                                return 'CO';
                            })()}
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
                        {humanize(platform)}
                    </span>
                ))}
                {company.status?.operating_status === "public" && (
                    <span className="badge badge--success margin-right--xs">
                        Public{company.status?.ticker ? ` · ${company.status.ticker}` : ''}
                    </span>
                )}
                {company.status?.operating_status === "acquired" && (
                    <span className="badge badge--warning margin-right--xs">
                        Acquired{company.status?.acquired?.acquired_by ? ` by ${company.status.acquired.acquired_by}` : ''}
                    </span>
                )}
                {company.status?.operating_status === "defunct" && (
                    <span className="badge badge--danger margin-right--xs">Defunct</span>
                )}
                {company.status?.operating_status === "stealth" && (
                    <span className="badge badge--info margin-right--xs">Stealth</span>
                )}
                {company.status?.operating_status === "non_profit" && (
                    <span className="badge badge--info margin-right--xs">Non-profit</span>
                )}
            </div>

            {(company.qubit_type || (company.ion_species && company.ion_species.length > 0)) && (
                <div className="company-qubit-tech">
                    {company.qubit_type && (
                        <div className="qubit-tech-row">
                            <span className="qubit-tech-label">Qubit type</span>
                            <span className="qubit-tech-value">{company.qubit_type}</span>
                        </div>
                    )}
                    {company.ion_species && company.ion_species.length > 0 && (
                        <div className="qubit-tech-row">
                            <span className="qubit-tech-label">Species</span>
                            <span className="qubit-tech-chips">
                                {company.ion_species.map((s, i) => (
                                    <span key={i} className="species-chip">{formatSpecies(s)}</span>
                                ))}
                            </span>
                        </div>
                    )}
                </div>
            )}

            <div className="panel-divider" />

            <div className="person-bio">
                <p><strong>{company.short_summary}</strong></p>
            </div>

            {/* Approach */}
            {(company.approach?.elevator_pitch || company.approach?.differentiators) && (
                <>
                    <h4 className="section-header">Approach</h4>
                    {company.approach.elevator_pitch && (
                        <p className="company-approach-pitch">
                            "{company.approach.elevator_pitch}"
                        </p>
                    )}
                    {company.approach.differentiators && (
                        <ul className="company-approach-list">
                            {company.approach.differentiators.map((diff, i) => (
                                <li key={i}>{diff}</li>
                            ))}
                        </ul>
                    )}
                    {company.approach.architecture_tags && (
                        <div className="company-architecture-tags">
                            {company.approach.architecture_tags.map((tag, i) => (
                                <span key={i} className="badge badge--secondary margin-right--xs architecture-tag">
                                    {humanize(tag)}
                                </span>
                            ))}
                        </div>
                    )}
                </>
            )}

            {/* People */}
            {(() => {
                const founders = company.people?.founders || [];
                const leadership = company.people?.leadership || [];
                const former = company.people?.former_leadership || [];
                const advisors = company.people?.advisors || [];
                const spinouts = company.people?.spun_out_of || [];
                const dirMembers = company.directory?.current_members || [];

                // Names already listed as founders/leadership/former, so the generic
                // directory line doesn't repeat them.
                const known = new Set();
                [...founders, ...leadership, ...former, ...advisors].forEach((p) => {
                    if (p?.name) known.add(p.name.toLowerCase());
                });
                const otherMembers = dirMembers
                    .map((pID) => {
                        const mp = people.find((p) => p.md_filename === pID);
                        return mp ? mp.name : pID;
                    })
                    .filter((nm) => nm && !known.has(nm.toLowerCase()));

                if (!(founders.length || leadership.length || former.length || advisors.length || otherMembers.length || spinouts.length)) {
                    return null;
                }

                const roleList = (arr) => arr.map((p, i) => (
                    <div key={i} className="affiliation-item">
                        <strong>{renderPersonLink(p.name)}</strong>{p.role ? ` — ${p.role}` : ''}
                    </div>
                ));

                return (
                    <>
                        <div className="panel-divider" />
                        <h4 className="section-header">Team & Leadership</h4>

                        {founders.length > 0 && (<>
                            <div className="team-subhead">Founders</div>
                            {roleList(founders)}
                        </>)}

                        {leadership.length > 0 && (<>
                            <div className="team-subhead">Leadership</div>
                            {roleList(leadership)}
                        </>)}

                        {former.length > 0 && (<>
                            <div className="team-subhead">Former leadership</div>
                            {roleList(former)}
                        </>)}

                        {advisors.length > 0 && (<>
                            <div className="team-subhead">Advisors</div>
                            {roleList(advisors)}
                        </>)}

                        {otherMembers.length > 0 && (
                            <div className="affiliation-item" style={{ marginTop: '8px' }}>
                                <strong>Other team members: </strong>
                                {otherMembers.map((nm, idx) => (
                                    <React.Fragment key={idx}>
                                        {renderPersonLink(nm)}
                                        {idx < otherMembers.length - 1 ? ', ' : ''}
                                    </React.Fragment>
                                ))}
                            </div>
                        )}

                        {spinouts.length > 0 && (
                            <div className="affiliation-item" style={{ marginTop: '8px' }}>
                                <em>Spun out of: {spinouts.map((inst, idx) => (
                                    <React.Fragment key={idx}>
                                        {renderInstitutionLink(typeof inst === 'string' ? inst : inst.name)}
                                        {idx < spinouts.length - 1 ? ', ' : ''}
                                    </React.Fragment>
                                ))}</em>
                            </div>
                        )}
                    </>
                );
            })()}

            {/* Links */}
            <div className="panel-divider" />
            <h4 className="section-header">Links</h4>
            <div className="links-list" style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                {company.links?.website && (
                    <a href={company.links.website} target="_blank" rel="noopener noreferrer" className="badge badge--secondary link-badge">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z" /></svg>
                        Website
                    </a>
                )}
                {company.links?.news && (
                    <a href={company.links.news} target="_blank" rel="noopener noreferrer" className="badge badge--secondary link-badge">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M22 3c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V3zm-2.5 12.5h-10v-1h10v1zm0-3.5h-10v-1h10v1zm0-3.5h-10v-1h10v1zM6 15.5h2v-7H6v7z" /></svg>
                        News
                    </a>
                )}
                {company.links?.careers && (
                    <a href={company.links.careers} target="_blank" rel="noopener noreferrer" className="badge badge--secondary link-badge">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2z" /></svg>
                        Careers
                    </a>
                )}
                {company.links?.linkedin && (
                    <a href={company.links.linkedin} target="_blank" rel="noopener noreferrer" className="badge badge--secondary link-badge">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z" /></svg>
                        LinkedIn
                    </a>
                )}
                {company.links?.wikipedia && (
                    <a href={company.links.wikipedia} target="_blank" rel="noopener noreferrer" className="badge badge--secondary link-badge">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M14.97 18.95l-2.56-6.03c-1.02 1.99-2.14 4.08-3.1 6.03-.01.01-.47 0-.47 0L4.91 9.6c-.83-1.95-.87-1.99-1.91-2.04V7h5.25v.56c-.61.03-1.66.16-1.36.94l2.87 6.81 1.97-3.91-1.07-2.42c-.39-.83-.7-1.37-1.7-1.42V7h4.63v.52c-.8.02-1.21.32-.91 1l1.86 4.32 1.86-4.13c.33-.79-.13-1.13-1.21-1.18V7h4.27v.52c-.85.07-1.27.46-1.61 1.27l-2.55 5.86 2.39 5.58 3.04-7.04c.32-.79-.17-1.12-1.07-1.15V7h4.34v.56c-1 .07-1.32.34-1.78 1.37l-3.93 8.97c-.01.01-.43.05-.43.05z" /></svg>
                        Wikipedia
                    </a>
                )}
                {company.links?.investor_relations && (
                    <a href={company.links.investor_relations} target="_blank" rel="noopener noreferrer" className="badge badge--secondary link-badge">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M3.5 18.49l6-6.01 4 4L22 6.92l-1.41-1.41-7.09 7.97-4-4L2 16.99z" /></svg>
                        Investors
                    </a>
                )}
            </div>

            {/* Milestones */}
            {company.milestones && company.milestones.length > 0 && (
                <>
                    <div className="panel-divider" />
                    <h4 className="section-header">Milestones</h4>
                    <div className="milestones-timeline" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {/* Sort by date descending (assuming format YYYY-MM or similar is string sortable, or just preserve array order which is usually chronological) */}
                        {company.milestones.map((ms, i) => (
                            <div key={i} className="trajectory-item">
                                <div className="trajectory-title">{ms.date}</div>
                                <div className="trajectory-details">{ms.claim || ms.description}</div>
                                {(ms.source || ms.link) && (
                                    <div className="trajectory-details">
                                        <a href={ms.source || ms.link} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.9em' }}>Source</a>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </>
            )}

            {/* Funding */}
            {company.funding && ((company.funding.total_raised_usd || company.funding.total_usd) > 0 || company.funding.rounds?.length > 0) && (
                <>
                    <div className="panel-divider" />
                    <h4 className="section-header">Funding</h4>
                    {(company.funding.total_raised_usd || company.funding.total_usd) > 0 && (
                        <p><strong>Total Raised:</strong> ${((company.funding.total_raised_usd || company.funding.total_usd) / 1000000).toFixed(1)}M</p>
                    )}
                    {company.funding.rounds && company.funding.rounds.map((round, i) => {
                        const leads = (round.lead_investors && round.lead_investors.length > 0)
                            ? round.lead_investors.join(", ")
                            : round.lead_investor;
                        return (
                        <div key={i} className="trajectory-item">
                            <div className="trajectory-title">{round.round || round.stage}{round.amount_usd ? ` — $${(round.amount_usd / 1000000).toFixed(1)}M` : ''}</div>
                            <div className="trajectory-details">
                                {round.date}{leads ? <> • Lead: {leads}</> : null}
                                {round.other_investors?.length > 0 && (
                                    <div style={{ marginTop: '4px' }}>
                                        <details className="funding-round-details-toggle">
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
                        );
                    })}
                </>
            )}

            {/* Roadmap */}
            {company.roadmap && company.roadmap.length > 0 && (
                <>
                    <div className="panel-divider" />
                    <h4 className="section-header">Roadmap</h4>
                    <div className="milestones-timeline" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {company.roadmap.map((r, i) => (
                            <div key={i} className="trajectory-item">
                                {r.target_date && <div className="trajectory-title">{r.target_date}</div>}
                                <div className="trajectory-details">{r.target_claim}</div>
                                {r.source && (
                                    <div className="trajectory-details">
                                        <a href={r.source} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.9em' }}>Source</a>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </>
            )}

            {/* Partnerships */}
            {company.partnerships && company.partnerships.length > 0 && (
                <>
                    <div className="panel-divider" />
                    <h4 className="section-header">Partnerships</h4>
                    <div className="inst-card-badges">
                        {company.partnerships.map((pn, i) => (
                            <span key={i} className="badge badge--secondary margin-right--xs">
                                {pn.name}{pn.type ? ` · ${pn.type.replace(/_/g, ' ')}` : ''}
                            </span>
                        ))}
                    </div>
                </>
            )}

            {/* Sources */}
            {company.sources && company.sources.length > 0 && (
                <>
                    <div className="panel-divider" />
                    <h4 className="section-header" style={{ fontSize: '0.9em' }}>Sources</h4>
                    <ul className="panel-sources-list">
                        {company.sources.map((src, i) => (
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
            {company.location?.lat && company.location?.lon && onShowInMap && (
                <>
                    <div className="panel-divider" />
                    <button
                        className="show-in-map-btn"
                        onClick={() => onShowInMap(company.location.lat, company.location.lon)}
                    >
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" /></svg>
                        Show in Map
                    </button>
                </>
            )}

            {/* Feedback Form below all content */}
            <div style={{ marginTop: '30px', marginBottom: '10px', display: 'flex', justifyContent: 'flex-start' }}>
                <FeedbackForm
                    entityType="Company"
                    entityName={company.name}
                    entityId={company.md_filename}
                />
            </div>
        </div>
    );
}

export default CompanyPanel;
