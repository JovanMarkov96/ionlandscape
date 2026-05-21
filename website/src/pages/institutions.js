import React, { useEffect, useState, useMemo } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useLocation, useHistory } from 'react-router-dom';

/**
 * Institutions Page Component
 * 
 * Displays a searchable and filterable list of research institutions/institutions.
 * Supports filtering by:
 * - Category (Trapped Ions / Neutral Atoms)
 * - Search query (Name)
 * - Label (e.g., "Trapped Ions")
 * - Ion Species
 * - Institution
 * - Country
 * 
 * URL Synchronization: All filters are synced with URL query parameters for shareability.
 */
function Institutions() {
    const location = useLocation();
    const history = useHistory();
    const [institutions, setInstitutions] = useState([]);

    // Parse query params
    const searchParams = new URLSearchParams(location.search);
    const searchQuery = searchParams.get('q') || '';
    const labelFilters = searchParams.getAll('label');
    const ionFilters = searchParams.getAll('ion');
    const instFilters = searchParams.getAll('inst');
    const countryFilters = searchParams.getAll('country');

    // Local state for search to avoid URL round-trip lag while typing
    const [localSearch, setLocalSearch] = useState(searchQuery);

    // Category state (Trapped Ions vs Neutral Atoms)
    const [category, setCategory] = useState(searchParams.get('category') || 'All');

    // Sync local state when external URL changes (e.g. back button)
    // Avoid overwriting if user is actively typing (input focused)
    useEffect(() => {
        const searchInput = document.getElementById('search-input');
        const isFocused = document.activeElement === searchInput;

        if (!isFocused && searchQuery !== localSearch) {
            setLocalSearch(searchQuery);
        }
    }, [searchQuery]);

    // Debounce URL update
    useEffect(() => {
        const timer = setTimeout(() => {
            if (localSearch !== searchQuery) {
                updateUrl({
                    q: localSearch,
                    label: labelFilters,
                    ion: ionFilters,
                    inst: instFilters,
                    country: countryFilters,
                    category: category // Add category
                }, true); // push
            }
        }, 300);
        return () => clearTimeout(timer);
    }, [localSearch, labelFilters, ionFilters, instFilters, countryFilters, category]);

    // --- Dependent Filter Logic ---

    // Helper: Get institutions that match specific filters (ignoring others)
    const getInstitutionsInContext = (filters) => {
        return institutions.filter(p => {
            // 0. Category
            if (category !== 'All') {
                const platforms = p.platforms || [];
                const isNeutrals = platforms.some(pl => pl.toLowerCase().includes('neutral'));
                if (category === 'Neutral Atoms' && !isNeutrals) return false;
                if (category === 'Trapped Ions' && isNeutrals) return false;
            }

            // 1. Institution (if provided)
            if (filters.inst && filters.inst.length > 0) {
                if (!filters.inst.includes(p.current_position?.institution)) return false;
            }

            // 2. Country (if provided)
            if (filters.country && filters.country.length > 0) {
                if (!filters.country.includes(p.location?.country)) return false;
            }

            return true;
        });
    };

    // Available Institutions: Depends on Category + Country
    const availableInsts = useMemo(() => {
        const filtered = getInstitutionsInContext({ country: countryFilters });
        const insts = new Set();
        filtered.forEach(p => {
            if (p.current_position?.institution) insts.add(p.current_position.institution);
        });
        return Array.from(insts).sort().filter(i => !instFilters.includes(i));
    }, [institutions, category, countryFilters, instFilters]);

    // Available Countries: Depends on Category + Institution
    const availableCountries = useMemo(() => {
        const filtered = getInstitutionsInContext({ inst: instFilters });
        const countries = new Set();
        filtered.forEach(p => {
            if (p.location?.country) countries.add(p.location.country);
        });
        return Array.from(countries).sort().filter(c => !countryFilters.includes(c));
    }, [institutions, category, instFilters, countryFilters]);

    // Available Labels & Ions (Global context within category)
    const { availableLabels, availableIons } = useMemo(() => {
        const filtered = getInstitutionsInContext({}); // Valid in category
        const labels = new Set();
        const ions = new Set();
        filtered.forEach(p => {
            (p.labels || []).forEach(l => labels.add(l));
            (p.ion_species || []).forEach(i => ions.add(i));
        });
        return {
            availableLabels: Array.from(labels).sort().filter(l => !labelFilters.includes(l)),
            availableIons: Array.from(ions).sort().filter(i => !ionFilters.includes(i))
        };
    }, [institutions, category, labelFilters, ionFilters]);

    useEffect(() => {
        // Force body scrolling when on the institutions page
        document.body.style.overflow = 'auto';
        return () => {
            document.body.style.overflow = '';
        };
    }, []);

    useEffect(() => {
        const loadInstitutions = async () => {
            const paths = [
                '/ionlandscape/data/institutions.json',
                '/data/institutions.json',
                'data/institutions.json' // Relative
            ];

            for (const path of paths) {
                try {
                    console.log('[Institutions] Trying to fetch:', path);
                    const res = await fetch(path);
                    if (res.ok) {
                        const data = await res.json();
                        setInstitutions(data);
                        return; // Success
                    } else {
                        console.log('[Institutions] Failed fetch (not ok):', path, res.status);
                    }
                } catch (err) {
                    console.log('[Institutions] Error fetching:', path, err);
                }
            }
            console.error('[Institutions] All fetch attempts failed.');
        };

        loadInstitutions();
    }, []);

    // Filter institutions based on active filters (AND logic)
    const filteredInstitutions = useMemo(() => {
        if (!institutions.length) return [];

        return institutions.filter(p => {
            // 0. Category Filter
            if (category !== 'All') {
                const platforms = p.platforms || [];
                const isNeutrals = platforms.some(pl => pl.toLowerCase().includes('neutral'));

                if (category === 'Neutral Atoms') {
                    if (!isNeutrals) return false;
                } else if (category === 'Trapped Ions') {
                    // If specifically Neutral Atoms, exclude from Trapped Ions view (unless they are both, but assume disjoint for now based on user request)
                    if (isNeutrals) return false;
                }
            }

            // 1. Search Query (Name)
            if (searchQuery) {
                const q = searchQuery.toLowerCase();
                const nameMatch = p.name?.toLowerCase().includes(q) || p.sort_name?.toLowerCase().includes(q);
                if (!nameMatch) return false;
            }

            // 2. Label Filters (ALL selected)
            if (labelFilters.length > 0) {
                const hasAllLabels = labelFilters.every(label => p.labels && p.labels.includes(label));
                if (!hasAllLabels) return false;
            }

            // 3. Ion Filters (ALL selected)
            if (ionFilters.length > 0) {
                const hasAllIons = ionFilters.every(ion => p.ion_species && p.ion_species.includes(ion));
                if (!hasAllIons) return false;
            }

            // 4. Institution Filters (ALL selected)
            if (instFilters.length > 0) {
                const hasAllInst = instFilters.every(inst => p.current_position?.institution === inst);
                if (!hasAllInst) return false;
            }

            // 5. Country Filters (ALL selected)
            if (countryFilters.length > 0) {
                const hasAllCountry = countryFilters.every(c => p.location?.country === c);
                if (!hasAllCountry) return false;
            }

            return true;
        });
    }, [institutions, searchQuery, labelFilters, ionFilters, instFilters, countryFilters, category]);

    // Update URL with new filters
    const updateUrl = (newParams) => {
        const params = new URLSearchParams();

        if (newParams.category && newParams.category !== 'All') params.set('category', newParams.category);
        if (newParams.q) params.set('q', newParams.q);

        (newParams.label || []).forEach(l => params.append('label', l));
        (newParams.ion || []).forEach(i => params.append('ion', i));
        (newParams.inst || []).forEach(i => params.append('inst', i));
        (newParams.country || []).forEach(c => params.append('country', c));

        history.push({ search: params.toString() });
    };

    // Keep helpers for immediate updates (dropdowns)
    const addFilter = (type, value) => {
        const current = {
            q: localSearch, // use local search value
            label: labelFilters,
            ion: ionFilters,
            inst: instFilters,
            country: countryFilters
        };

        if (type === 'inst') {
            // Single-select Institution
            current.inst = [value];
            // Auto-select Country
            const personWithInst = institutions.find(p => p.current_position?.institution === value);
            console.log('[Institutions] Selected Inst:', value);
            console.log('[Institutions] Found Person:', personWithInst ? personWithInst.name : 'None');

            if (personWithInst?.location?.country) {
                console.log('[Institutions] Auto-setting Country:', personWithInst.location.country);
                current.country = [personWithInst.location.country];
            }
        } else if (type === 'country') {
            // Single-select Country
            current.country = [value];
            // Clear Institution if it doesn't match new country
            if (current.inst.length > 0) {
                const selectedInst = current.inst[0];
                const matches = institutions.some(p => p.current_position?.institution === selectedInst && p.location?.country === value);
                if (!matches) {
                    current.inst = []; // Clear invalid institution
                }
            }
        } else {
            // Multi-select for others
            if (current[type].includes(value)) return;
            current[type] = [...current[type], value];
        }

        updateUrl(current);
    };

    const removeFilter = (type, value) => {
        const current = {
            q: localSearch,
            label: labelFilters,
            ion: ionFilters,
            inst: instFilters,
            country: countryFilters
        };

        current[type] = current[type].filter(x => x !== value);
        updateUrl(current);
    };

    const clearAllFilters = () => {
        setLocalSearch(''); // Clear local too
        history.push({ search: '' });
    };

    const hasActiveFilters = searchQuery || labelFilters.length > 0 || ionFilters.length > 0 || instFilters.length > 0 || countryFilters.length > 0;

    // Available options logic already calculated above

    return (
        <Layout title="Quantum Research Institutions" description="Search and filter research universities, national labs, and institutes working in quantum computing.">
            <div className="groups-page container margin-vert--lg">
                <div className="institutions-header">
                    <h1>Search Institutions</h1>
                </div>

                {/* Category Toggle */}
                <div className="category-toggle-container">
                    <div className="button-group">
                        {['All', 'Trapped Ions', 'Neutral Atoms'].map(cat => (
                            <button
                                key={cat}
                                className={`button button--${category === cat ? 'primary' : 'secondary'} category-btn-wrapper`}
                                onClick={() => setCategory(cat)}
                            >
                                {cat}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Filter Bar */}
                <div className="filter-bar">
                    {/* Search Input */}
                    <div className="search-container">
                        <input
                            id="search-input"
                            type="text"
                            className="filter-select search-input"
                            placeholder="Search by name..."
                            value={localSearch}
                            onChange={(e) => setLocalSearch(e.target.value)}
                        />
                    </div>

                    <div className="filter-bar-row">
                        {/* Dropdowns */}
                        <select className="filter-select" value="" onChange={(e) => e.target.value && addFilter('label', e.target.value)}>
                            <option value="">+ Label</option>
                            {availableLabels.map(o => <option key={o} value={o}>{o}</option>)}
                        </select>

                        {/* Species Dropdown: Only show if specific category selected */}
                        {category !== 'All' && (
                            <select className="filter-select" value="" onChange={(e) => e.target.value && addFilter('ion', e.target.value)}>
                                <option value="">+ {category === 'Neutral Atoms' ? 'Atom Species' : 'Ion Species'}</option>
                                {availableIons.map(o => <option key={o} value={o}>{o}</option>)}
                            </select>
                        )}

                        <select className="filter-select" value="" onChange={(e) => e.target.value && addFilter('inst', e.target.value)}>
                            <option value="">+ Institution</option>
                            {availableInsts.map(o => <option key={o} value={o}>{o}</option>)}
                        </select>

                        <select className="filter-select" value="" onChange={(e) => e.target.value && addFilter('country', e.target.value)}>
                            <option value="">+ Country</option>
                            {availableCountries.map(o => <option key={o} value={o}>{o}</option>)}
                        </select>

                        {/* Clear All */}
                        {hasActiveFilters && (
                            <button className="clear-all-btn" onClick={clearAllFilters}>
                                Clear All
                            </button>
                        )}
                    </div>

                    {/* Active Chips */}
                    {hasActiveFilters && (
                        <div className="filter-chips">
                            {labelFilters.map(v => (
                                <span key={`label-${v}`} className="filter-chip filter-chip--label">
                                    {v} <button className="filter-chip-remove" onClick={() => removeFilter('label', v)}>×</button>
                                </span>
                            ))}
                            {ionFilters.map(v => (
                                <span key={`ion-${v}`} className="filter-chip filter-chip--ion">
                                    {v} <button className="filter-chip-remove" onClick={() => removeFilter('ion', v)}>×</button>
                                </span>
                            ))}
                            {instFilters.map(v => (
                                <span key={`inst-${v}`} className="filter-chip" style={{ background: '#e9ecef', color: '#333', border: '1px solid #ddd' }}>
                                    🏛️ {v} <button className="filter-chip-remove" onClick={() => removeFilter('inst', v)}>×</button>
                                </span>
                            ))}
                            {countryFilters.map(v => (
                                <span key={`country-${v}`} className="filter-chip" style={{ background: '#e9ecef', color: '#333', border: '1px solid #ddd' }}>
                                    🌍 {v} <button className="filter-chip-remove" onClick={() => removeFilter('country', v)}>×</button>
                                </span>
                            ))}
                        </div>
                    )}
                </div>

                <p className="results-count">
                    Found {filteredInstitutions.length} institutions
                </p>

                {/* Results Grid */}
                <div className="row">
                    {filteredInstitutions.map(person => (
                        <div key={person.id} className="col col--4 margin-bottom--lg">
                            <div className="card">
                                <div className="card__header">
                                    <h3>{person.name}</h3>
                                </div>
                                <div className="card__body">
                                    <p>{person.current_position?.institution}</p>
                                    <div className="card-badges-container">
                                        {person.labels?.map(label => (
                                            <span
                                                key={label}
                                                className="badge badge--primary margin-right--xs clickable-badge"
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
                                                className="badge badge--secondary margin-right--xs clickable-badge"
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
                    {filteredInstitutions.length === 0 && (
                        <div className="col col--12">
                            <div className="alert alert--warning">
                                <p>No institutions found matching criteria.</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </Layout>
    );
}

export default Institutions;
