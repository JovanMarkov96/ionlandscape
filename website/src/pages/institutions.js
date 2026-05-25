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
    const focusAreaFilters = searchParams.getAll('focus_area');
    const platformFilters = searchParams.getAll('platform');
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
                    focus_area: focusAreaFilters,
                    platform: platformFilters,
                    country: countryFilters,
                    category: category
                }, true); // push
            }
        }, 300);
        return () => clearTimeout(timer);
    }, [localSearch, focusAreaFilters, platformFilters, countryFilters, category]);

    // --- Dependent Filter Logic ---

    // Helper: Get institutions that match specific filters (ignoring others)
    const getInstitutionsInContext = (filters) => {
        return institutions.filter(p => {
            // 0. Category
            if (category !== 'All') {
                const pls = p.platforms_represented || [];
                const isNeutrals = pls.some(pl => pl.toLowerCase().includes('neutral'));
                if (category === 'Neutral Atoms' && !isNeutrals) return false;
                if (category === 'Trapped Ions' && isNeutrals) return false;
            }
            // Country (if provided)
            if (filters.country && filters.country.length > 0) {
                if (!filters.country.includes(p.location?.country)) return false;
            }
            return true;
        });
    };

    // Available Countries
    const availableCountries = useMemo(() => {
        const filtered = getInstitutionsInContext({});
        const countries = new Set();
        filtered.forEach(p => {
            if (p.location?.country) countries.add(p.location.country);
        });
        return Array.from(countries).sort().filter(c => !countryFilters.includes(c));
    }, [institutions, category, countryFilters]);

    // Available Focus Areas & Platforms
    const { availableFocusAreas, availablePlatforms } = useMemo(() => {
        const filtered = getInstitutionsInContext({});
        const focusAreas = new Set();
        const platforms = new Set();
        filtered.forEach(p => {
            (p.focus_areas || []).forEach(a => focusAreas.add(a));
            (p.platforms_represented || []).forEach(pl => platforms.add(pl));
        });
        return {
            availableFocusAreas: Array.from(focusAreas).sort().filter(a => !focusAreaFilters.includes(a)),
            availablePlatforms: Array.from(platforms).sort().filter(pl => !platformFilters.includes(pl)),
        };
    }, [institutions, category, focusAreaFilters, platformFilters]);

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
                const pls = p.platforms_represented || [];
                const isNeutrals = pls.some(pl => pl.toLowerCase().includes('neutral'));
                if (category === 'Neutral Atoms' && !isNeutrals) return false;
                if (category === 'Trapped Ions' && isNeutrals) return false;
            }

            // 1. Search Query (Name)
            if (searchQuery) {
                const q = searchQuery.toLowerCase();
                const nameMatch = p.name?.toLowerCase().includes(q) || p.sort_name?.toLowerCase().includes(q);
                if (!nameMatch) return false;
            }

            // 2. Focus Area Filters (ALL selected)
            if (focusAreaFilters.length > 0) {
                const hasAll = focusAreaFilters.every(a => p.focus_areas && p.focus_areas.includes(a));
                if (!hasAll) return false;
            }

            // 4. Platform Filters (ALL selected)
            if (platformFilters.length > 0) {
                const hasAll = platformFilters.every(pl => p.platforms_represented && p.platforms_represented.includes(pl));
                if (!hasAll) return false;
            }

            // 5. Country Filters (ALL selected)
            if (countryFilters.length > 0) {
                const hasAllCountry = countryFilters.every(c => p.location?.country === c);
                if (!hasAllCountry) return false;
            }

            return true;
        }).sort((a, b) => (a.name || '').toLowerCase().localeCompare((b.name || '').toLowerCase()));
    }, [institutions, searchQuery, focusAreaFilters, platformFilters, countryFilters, category]);

    // Update URL with new filters
    const updateUrl = (newParams) => {
        const params = new URLSearchParams();

        if (newParams.category && newParams.category !== 'All') params.set('category', newParams.category);
        if (newParams.q) params.set('q', newParams.q);

        (newParams.focus_area || []).forEach(a => params.append('focus_area', a));
        (newParams.platform || []).forEach(pl => params.append('platform', pl));
        (newParams.country || []).forEach(c => params.append('country', c));

        history.push({ search: params.toString() });
    };

    // Keep helpers for immediate updates (dropdowns)
    const addFilter = (type, value) => {
        const current = {
            q: localSearch,
            focus_area: focusAreaFilters,
            platform: platformFilters,
            country: countryFilters
        };
        if (current[type] !== undefined) {
            if (Array.isArray(current[type]) && current[type].includes(value)) return;
            current[type] = Array.isArray(current[type]) ? [...current[type], value] : [value];
        }
        updateUrl(current);
    };

    const removeFilter = (type, value) => {
        const current = {
            q: localSearch,
            focus_area: focusAreaFilters,
            platform: platformFilters,
            country: countryFilters
        };
        if (Array.isArray(current[type])) {
            current[type] = current[type].filter(x => x !== value);
        }
        updateUrl(current);
    };

    const clearAllFilters = () => {
        setLocalSearch('');
        history.push({ search: '' });
    };

    const hasActiveFilters = searchQuery || focusAreaFilters.length > 0 || platformFilters.length > 0 || countryFilters.length > 0;

    // Available options logic already calculated above

    return (
        <Layout title="Quantum Research Institutions" description="Search and filter research universities, national labs, and institutes working in quantum computing.">
            <div className="groups-page container margin-vert--lg">
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
                        <select className="filter-select" value="" onChange={(e) => e.target.value && addFilter('focus_area', e.target.value)}>
                            <option value="">+ Focus Area</option>
                            {availableFocusAreas.map(o => <option key={o} value={o}>{o}</option>)}
                        </select>

                        <select className="filter-select" value="" onChange={(e) => e.target.value && addFilter('platform', e.target.value)}>
                            <option value="">+ Platform</option>
                            {availablePlatforms.map(o => (
                                <option key={o} value={o}>
                                    {o.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
                                </option>
                            ))}
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
                            {focusAreaFilters.map(v => (
                                <span key={`focus_area-${v}`} className="filter-chip filter-chip--label">
                                    {v} <button className="filter-chip-remove" onClick={() => removeFilter('focus_area', v)}>×</button>
                                </span>
                            ))}
                            {platformFilters.map(v => (
                                <span key={`platform-${v}`} className="filter-chip filter-chip--platform">
                                    {v.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())} <button className="filter-chip-remove" onClick={() => removeFilter('platform', v)}>×</button>
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
                    {filteredInstitutions.map(institution => {
                        const logoSrc = institution.media?.logo_path
                            ? (institution.media.logo_path.startsWith('http')
                                ? institution.media.logo_path
                                : `/ionlandscape${institution.media.logo_path}`)
                            : null;
                        const nameParts = (institution.name || '').split(' ').filter(p => p.trim() !== '');
                        const initials = nameParts.length > 1
                            ? (nameParts[0][0] + nameParts[1][0]).toUpperCase()
                            : nameParts.length === 1 ? nameParts[0].substring(0, 2).toUpperCase() : 'IN';
                        const clean = v => (v && String(v).trim().toLowerCase() !== 'unknown') ? v : null;
                        const location = [clean(institution.location?.city), clean(institution.location?.country)].filter(Boolean).join(', ');

                        return (
                        <div key={institution.id} className="col col--4 margin-bottom--lg">
                            <div className="card inst-card">
                                <div className="card__header company-card-header">
                                    {logoSrc ? (
                                        <div className="inst-logo-ring">
                                            <img
                                                className="inst-logo-img"
                                                src={logoSrc}
                                                alt=""
                                            />
                                        </div>
                                    ) : (
                                        <div className="inst-logo-ring inst-logo-placeholder">
                                            <span>{initials}</span>
                                        </div>
                                    )}
                                    <div className="inst-card-title-block">
                                        <h3>{institution.name}</h3>
                                        {location && <p className="company-card-location">{location}</p>}
                                    </div>
                                </div>
                                <div className="card__body inst-card-body">
                                    <p className="inst-card-description">
                                        {institution.short_description || 'No description available'}
                                    </p>
                                    <div className="inst-card-badges">
                                        {(institution.focus_areas || []).map(area => (
                                            <span
                                                key={area}
                                                className="badge badge--primary margin-right--xs margin-bottom--xs clickable-badge"
                                                onClick={() => addFilter('focus_area', area)}
                                            >
                                                {area}
                                            </span>
                                        ))}
                                        {(institution.platforms_represented || []).map(pl => (
                                            <span
                                                key={pl}
                                                className="badge badge--success margin-right--xs margin-bottom--xs clickable-badge"
                                                onClick={() => addFilter('platform', pl)}
                                            >
                                                {pl.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                                <div className="card__footer">
                                    <Link to={`/?institution=${institution.id}`} className="button button--primary button--block">
                                        View on Map
                                    </Link>
                                </div>
                            </div>
                        </div>
                        );
                    })}
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
