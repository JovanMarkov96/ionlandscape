import React, { useEffect, useState, useMemo } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useLocation, useHistory } from 'react-router-dom';

function Groups() {
    const location = useLocation();
    const history = useHistory();
    const [people, setPeople] = useState([]);

    // Parse query params - support multiple values
    const searchParams = new URLSearchParams(location.search);
    const labelFilters = searchParams.getAll('label');
    const ionFilters = searchParams.getAll('ion');

    // Get unique labels and ions for dropdown options
    const { allLabels, allIons } = useMemo(() => {
        const labels = new Set();
        const ions = new Set();
        people.forEach(p => {
            (p.labels || []).forEach(l => labels.add(l));
            (p.ion_species || []).forEach(i => ions.add(i));
        });
        return {
            allLabels: Array.from(labels).sort(),
            allIons: Array.from(ions).sort()
        };
    }, [people]);

    useEffect(() => {
        // Force body scrolling when on the groups page
        // This is a robust fix for the "no scrolling" issue regardless of CSS support
        document.body.style.overflow = 'auto';

        return () => {
            document.body.style.overflow = '';
        };
    }, []);

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

    // Filter people based on active filters (AND logic)
    const filteredPeople = useMemo(() => {
        if (!people.length) return [];

        let res = people;

        // Apply label filters (must have ALL selected labels)
        if (labelFilters.length > 0) {
            res = res.filter(p =>
                labelFilters.every(label => p.labels && p.labels.includes(label))
            );
        }

        // Apply ion filters (must have ALL selected ions)
        if (ionFilters.length > 0) {
            res = res.filter(p =>
                ionFilters.every(ion => p.ion_species && p.ion_species.includes(ion))
            );
        }

        return res;
    }, [people, labelFilters, ionFilters]);

    // Update URL with new filters
    const updateFilters = (newLabels, newIons) => {
        const params = new URLSearchParams();
        newLabels.forEach(l => params.append('label', l));
        newIons.forEach(i => params.append('ion', i));
        history.push({ search: params.toString() });
    };

    // Add a filter
    const addFilter = (type, value) => {
        if (type === 'label' && !labelFilters.includes(value)) {
            updateFilters([...labelFilters, value], ionFilters);
        } else if (type === 'ion' && !ionFilters.includes(value)) {
            updateFilters(labelFilters, [...ionFilters, value]);
        }
    };

    // Remove a specific filter
    const removeFilter = (type, value) => {
        if (type === 'label') {
            updateFilters(labelFilters.filter(l => l !== value), ionFilters);
        } else if (type === 'ion') {
            updateFilters(labelFilters, ionFilters.filter(i => i !== value));
        }
    };

    // Clear all filters
    const clearAllFilters = () => {
        history.push({ search: '' });
    };

    const hasActiveFilters = labelFilters.length > 0 || ionFilters.length > 0;

    // Get available options (exclude already selected)
    const availableLabels = allLabels.filter(l => !labelFilters.includes(l));
    const availableIons = allIons.filter(i => !ionFilters.includes(i));

    return (
        <Layout title="Groups">
            <div className="groups-page container margin-vert--lg">
                <h1>Research Groups</h1>
                <p className="margin-bottom--md" style={{ color: '#666' }}>
                    Showing {filteredPeople.length} of {people.length} researchers
                </p>

                {/* Filter Bar */}
                <div className="filter-bar">
                    <div className="filter-bar-row">
                        {/* Label Filter Dropdown */}
                        <select
                            className="filter-select"
                            value=""
                            onChange={(e) => {
                                if (e.target.value) {
                                    addFilter('label', e.target.value);
                                }
                            }}
                        >
                            <option value="">+ Add Label Filter</option>
                            {availableLabels.map(label => (
                                <option key={label} value={label}>{label}</option>
                            ))}
                        </select>

                        {/* Ion Species Filter Dropdown */}
                        <select
                            className="filter-select"
                            value=""
                            onChange={(e) => {
                                if (e.target.value) {
                                    addFilter('ion', e.target.value);
                                }
                            }}
                        >
                            <option value="">+ Add Ion Filter</option>
                            {availableIons.map(ion => (
                                <option key={ion} value={ion}>{ion}</option>
                            ))}
                        </select>

                        {/* Clear All Button */}
                        {hasActiveFilters && (
                            <button
                                className="clear-all-btn"
                                onClick={clearAllFilters}
                            >
                                Clear All
                            </button>
                        )}
                    </div>

                    {/* Active Filter Chips */}
                    {hasActiveFilters && (
                        <div className="filter-chips">
                            {labelFilters.map(label => (
                                <span key={`label-${label}`} className="filter-chip filter-chip--label">
                                    {label}
                                    <button
                                        className="filter-chip-remove"
                                        onClick={() => removeFilter('label', label)}
                                        aria-label={`Remove ${label} filter`}
                                    >
                                        ×
                                    </button>
                                </span>
                            ))}
                            {ionFilters.map(ion => (
                                <span key={`ion-${ion}`} className="filter-chip filter-chip--ion">
                                    {ion}
                                    <button
                                        className="filter-chip-remove"
                                        onClick={() => removeFilter('ion', ion)}
                                        aria-label={`Remove ${ion} filter`}
                                    >
                                        ×
                                    </button>
                                </span>
                            ))}
                        </div>
                    )}
                </div>

                {/* Results Grid */}
                <div className="row">
                    {filteredPeople.map(person => (
                        <div key={person.id} className="col col--4 margin-bottom--lg">
                            <div className="card">
                                <div className="card__header">
                                    <h3>{person.name}</h3>
                                </div>
                                <div className="card__body">
                                    <p>{person.current_position?.institution}</p>
                                    <div style={{ marginBottom: 8 }}>
                                        {person.labels?.map(label => (
                                            <span
                                                key={label}
                                                className="badge badge--primary margin-right--xs"
                                                style={{ cursor: 'pointer' }}
                                                onClick={() => addFilter('label', label)}
                                            >
                                                {label}
                                            </span>
                                        ))}
                                    </div>
                                    <div>
                                        {person.ion_species?.map(ion => (
                                            <span
                                                key={ion}
                                                className="badge badge--secondary margin-right--xs"
                                                style={{ cursor: 'pointer' }}
                                                onClick={() => addFilter('ion', ion)}
                                            >
                                                {ion}
                                            </span>
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
                            <div className="alert alert--warning">
                                <p>No groups found matching all selected filters.</p>
                                <p>Try removing some filters to see more results.</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </Layout>
    );
}

export default Groups;
