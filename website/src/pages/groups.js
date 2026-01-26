import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useLocation } from 'react-router-dom';

function Groups() {
    const location = useLocation();
    const [people, setPeople] = useState([]);
    const [filteredPeople, setFilteredPeople] = useState([]);

    // Parse query params
    const searchParams = new URLSearchParams(location.search);
    const labelFilter = searchParams.get('label');
    const ionFilter = searchParams.get('ion');

    useEffect(() => {
        fetch('/ionlandscape/data/people.json')
            .then(res => res.json())
            .then(data => {
                setPeople(data);
            })
            .catch(() => {
                fetch('/data/people.json').then(res => res.json()).then(setPeople);
            });
    }, []);

    useEffect(() => {
        if (!people.length) return;

        let res = people;
        if (labelFilter) {
            res = res.filter(p => p.labels && p.labels.includes(labelFilter));
        }
        if (ionFilter) {
            res = res.filter(p => p.ion_species && p.ion_species.includes(ionFilter));
        }
        setFilteredPeople(res);
    }, [people, labelFilter, ionFilter]);

    return (
        <Layout title="Groups">
            <div className="container margin-vert--lg">
                <h1>Research Groups</h1>

                {labelFilter && (
                    <div className="alert alert--info margin-bottom--md">
                        Filtering by Label: <strong>{labelFilter}</strong> <Link to="/groups">(Clear)</Link>
                    </div>
                )}
                {ionFilter && (
                    <div className="alert alert--info margin-bottom--md">
                        Filtering by Ion: <strong>{ionFilter}</strong> <Link to="/groups">(Clear)</Link>
                    </div>
                )}

                <div className="row">
                    {filteredPeople.map(person => (
                        <div key={person.id} className="col col--4 margin-bottom--lg">
                            <div className="card">
                                <div className="card__header">
                                    <h3>{person.name}</h3>
                                </div>
                                <div className="card__body">
                                    <p>{person.current_position?.institution}</p>
                                    <div>
                                        {person.ion_species?.map(ion => (
                                            <span key={ion} className="badge badge--secondary margin-right--xs">{ion}</span>
                                        ))}
                                    </div>
                                </div>
                                <div className="card__footer">
                                    <Link to={`/?person=${person.id}`} className="button button--primary button--block">
                                        View on Map
                                    </Link>
                                </div>
                            </div>
                        </div>
                    ))}
                    {filteredPeople.length === 0 && (
                        <div className="col col--12">
                            <p>No groups found matching criteria.</p>
                        </div>
                    )}
                </div>
            </div>
        </Layout>
    );
}

export default Groups;
