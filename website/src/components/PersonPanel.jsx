// website/src/components/PersonPanel.jsx
import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

function PersonPanel({ personId, location }) {
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

    if (location && !person) {
        // Render a location summary list if location selected (optional)
        return (
            <div style={{ padding: 16 }}>
                <h3>{location.city}, {location.country}</h3>
                <p>People at this location (click a marker):</p>
                {/* Implement listing if you want — left as exercise */}
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
            <ReactMarkdown>{mdBody}</ReactMarkdown>

            <hr />
            <p><strong>Links</strong></p>
            <ul>
                {person.links && person.links.google_scholar ? <li><a href={person.links.google_scholar}>Google Scholar</a></li> : null}
                {person.links && person.links.orcid ? <li><a href={person.links.orcid}>ORCID</a></li> : null}
                {person.links && person.links.homepage ? <li><a href={person.links.homepage}>Homepage</a></li> : null}
            </ul>
        </div>
    );
}

export default PersonPanel;
