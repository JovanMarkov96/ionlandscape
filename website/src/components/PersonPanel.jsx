// website/src/components/PersonPanel.jsx
import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

function PersonPanel({ personId, location, onPersonSelect }) {
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

        // Try to find the advisor in the people list
        // Normalize comparison (optional, but good for safety)
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

    if (location && !person) {
        return (
            <div style={{ padding: 16 }}>
                <h3>{location.city}, {location.country}</h3>
                <p>People at this location (click a marker):</p>
                {/* List people at this location if desired, similar to MapPanel popup logic */}
            </div>
        );
    }

    if (!person) {
        return (
            <div style={{ padding: 16 }}>
                <h3>Ion Landscape</h3>
                <p>Click a marker on the map to view a person profile.</p>
            </div>
        );
    }

    return (
        <div style={{ padding: 16 }}>
            <h2>{person.name}</h2>
            <p><em>{person.current_position && person.current_position.title} — {person.current_position && person.current_position.institution}</em></p>
            <p><strong>Platforms:</strong> {(person.platforms || []).join(', ')}</p>
            <p><strong>Keywords:</strong> {(person.keywords || []).join(', ')}</p>

            <hr />
            <div className="person-bio">
                <ReactMarkdown>{mdBody}</ReactMarkdown>
            </div>

            {/* Academic Trajectory / Education & Postdocs */}
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
