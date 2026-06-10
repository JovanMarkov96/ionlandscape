import React, { useEffect, useState, useMemo } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useLocation, useHistory } from 'react-router-dom';

/**
 * Companies Page Component
 * 
 * Displays a searchable and filterable list of research companies/companies.
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
function Companies() {
    const location = useLocation();
    const history = useHistory();
    const [companies, setCompanies] = useState([]);

    // Parse query params
    const searchParams = new URLSearchParams(location.search);
    const searchQuery = searchParams.get('q') || '';
    const labelFilters = searchParams.getAll('label');
    const ionFilters = searchParams.getAll('ion');
    const platformFilters = searchParams.getAll('platform');
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

    // Sync category state when the URL changes (e.g. back button)
    useEffect(() => {
        const urlCategory = searchParams.get('category') || 'All';
        if (urlCategory !== category) setCategory(urlCategory);
    }, [location.search]);

    // Debounce URL update
    useEffect(() => {
        const timer = setTimeout(() => {
            if (localSearch !== searchQuery) {
                updateUrl({
                    q: localSearch,
                    label: labelFilters,
                    ion: ionFilters,
                    platform: platformFilters,
                    inst: instFilters,
                    country: countryFilters,
                    category: category
                }, true); // push
            }
        }, 300);
        return () => clearTimeout(timer);
    }, [localSearch, labelFilters, ionFilters, platformFilters, instFilters, countryFilters, category]);

    // --- Dependent Filter Logic ---

    // Helper: Get companies that match specific filters (ignoring others)
    const getCompaniesInContext = (filters) => {
        return companies.filter(p => {
            // 0. Category
            if (category !== 'All') {
                const platforms = p.platforms || [];
                const isNeutrals = platforms.some(pl => pl === 'neutral_atom' || pl === 'rydberg_array');
                const isIons = platforms.includes('trapped_ion');
                if (category === 'Neutral Atoms' && !isNeutrals) return false;
                if (category === 'Trapped Ions' && !isIons) return false;
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
        const filtered = getCompaniesInContext({ country: countryFilters });
        const insts = new Set();
        filtered.forEach(p => {
            if (p.current_position?.institution) insts.add(p.current_position.institution);
        });
        return Array.from(insts).sort().filter(i => !instFilters.includes(i));
    }, [companies, category, countryFilters, instFilters]);

    // Available Countries: Depends on Category + Institution
    const availableCountries = useMemo(() => {
        const filtered = getCompaniesInContext({ inst: instFilters });
        const countries = new Set();
        filtered.forEach(p => {
            if (p.location?.country) countries.add(p.location.country);
        });
        return Array.from(countries).sort().filter(c => !countryFilters.includes(c));
    }, [companies, category, instFilters, countryFilters]);

    // Available Labels, Ions & Platforms (Global context within category)
    const { availableLabels, availableIons, availablePlatforms } = useMemo(() => {
        const filtered = getCompaniesInContext({});
        const labels = new Set();
        const ions = new Set();
        const platforms = new Set();
        filtered.forEach(p => {
            (p.labels || []).forEach(l => labels.add(l));
            (p.ion_species || []).forEach(i => ions.add(i));
            (p.platforms || []).forEach(pl => platforms.add(pl));
        });
        return {
            availableLabels: Array.from(labels).sort().filter(l => !labelFilters.includes(l)),
            availableIons: Array.from(ions).sort().filter(i => !ionFilters.includes(i)),
            availablePlatforms: Array.from(platforms).sort().filter(pl => !platformFilters.includes(pl)),
        };
    }, [companies, category, labelFilters, ionFilters, platformFilters]);

    useEffect(() => {
        // Force body scrolling when on the companies page
        document.body.style.overflow = 'auto';
        return () => {
            document.body.style.overflow = '';
        };
    }, []);

    useEffect(() => {
        const loadCompanies = async () => {
            const paths = [
                '/quantum-landscape/data/companies.json',
                '/data/companies.json',
                'data/companies.json' // Relative
            ];

            for (const path of paths) {
                try {
                    console.log('[Companies] Trying to fetch:', path);
                    const res = await fetch(path);
                    if (res.ok) {
                        const data = await res.json();
                        setCompanies(data);
                        return; // Success
                    } else {
                        console.log('[Companies] Failed fetch (not ok):', path, res.status);
                    }
                } catch (err) {
                    console.log('[Companies] Error fetching:', path, err);
                }
            }
            console.error('[Companies] All fetch attempts failed.');
        };

        loadCompanies();
    }, []);

    // Filter companies based on active filters (AND logic)
    const filteredCompanies = useMemo(() => {
        if (!companies.length) return [];

        return companies.filter(p => {
            // 0. Category Filter
            if (category !== 'All') {
                const platforms = p.platforms || [];
                const isNeutrals = platforms.some(pl => pl === 'neutral_atom' || pl === 'rydberg_array');
                const isIons = platforms.includes('trapped_ion');

                if (category === 'Neutral Atoms') {
                    if (!isNeutrals) return false;
                } else if (category === 'Trapped Ions') {
                    if (!isIons) return false;
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

            // 3b. Platform Filters (ALL selected)
            if (platformFilters.length > 0) {
                const hasAllPlatforms = platformFilters.every(pl => p.platforms && p.platforms.includes(pl));
                if (!hasAllPlatforms) return false;
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
        }).sort((a, b) => (a.name || '').toLowerCase().localeCompare((b.name || '').toLowerCase()));
    }, [companies, searchQuery, labelFilters, ionFilters, platformFilters, instFilters, countryFilters, category]);

    // Update URL with new filters
    const updateUrl = (newParams) => {
        const params = new URLSearchParams();

        if (newParams.category && newParams.category !== 'All') params.set('category', newParams.category);
        if (newParams.q) params.set('q', newParams.q);

        (newParams.label || []).forEach(l => params.append('label', l));
        (newParams.ion || []).forEach(i => params.append('ion', i));
        (newParams.platform || []).forEach(pl => params.append('platform', pl));
        (newParams.inst || []).forEach(i => params.append('inst', i));
        (newParams.country || []).forEach(c => params.append('country', c));

        history.push({ search: params.toString() });
    };

    // Keep helpers for immediate updates (dropdowns)
    const addFilter = (type, value) => {
        const current = {
            q: localSearch,
            label: labelFilters,
            ion: ionFilters,
            platform: platformFilters,
            inst: instFilters,
            country: countryFilters,
            category: category
        };

        if (type === 'inst') {
            // Single-select Institution
            current.inst = [value];
            // Auto-select Country
            const personWithInst = companies.find(p => p.current_position?.institution === value);
            console.log('[Companies] Selected Inst:', value);
            console.log('[Companies] Found Person:', personWithInst ? personWithInst.name : 'None');

            if (personWithInst?.location?.country) {
                console.log('[Companies] Auto-setting Country:', personWithInst.location.country);
                current.country = [personWithInst.location.country];
            }
        } else if (type === 'country') {
            // Single-select Country
            current.country = [value];
            // Clear Institution if it doesn't match new country
            if (current.inst.length > 0) {
                const selectedInst = current.inst[0];
                const matches = companies.some(p => p.current_position?.institution === selectedInst && p.location?.country === value);
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
            platform: platformFilters,
            inst: instFilters,
            country: countryFilters,
            category: category
        };

        current[type] = current[type].filter(x => x !== value);
        updateUrl(current);
    };

    const clearAllFilters = () => {
        setLocalSearch(''); // Clear local too
        history.push({ search: '' });
    };

    const hasActiveFilters = searchQuery || labelFilters.length > 0 || ionFilters.length > 0 || platformFilters.length > 0 || instFilters.length > 0 || countryFilters.length > 0;

    // Available options logic already calculated above

    return (
        <Layout title="Quantum Companies" description="Search and filter quantum technology companies, startups, and hardware manufacturers.">
            <div className="groups-page container margin-vert--lg">
                {/* Category Toggle */}
                <div className="category-toggle-container">
                    <div className="button-group">
                        {['All', 'Trapped Ions', 'Neutral Atoms'].map(cat => (
                            <button
                                key={cat}
                                className={`button button--${category === cat ? 'primary' : 'secondary'} category-btn-wrapper`}
                                onClick={() => {
                                    setCategory(cat);
                                    updateUrl({
                                        q: localSearch, label: labelFilters, ion: ionFilters,
                                        platform: platformFilters, inst: instFilters,
                                        country: countryFilters, category: cat,
                                    });
                                }}
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
                        {/* Species Dropdown: Only show if specific category selected */}
                        {category !== 'All' && (
                            <select className="filter-select" value="" onChange={(e) => e.target.value && addFilter('ion', e.target.value)}>
                                <option value="">+ {category === 'Neutral Atoms' ? 'Atom Species' : 'Ion Species'}</option>
                                {availableIons.map(o => <option key={o} value={o}>{o}</option>)}
                            </select>
                        )}

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
                            {platformFilters.map(v => (
                                <span key={`platform-${v}`} className="filter-chip filter-chip--platform">
                                    {v.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())} <button className="filter-chip-remove" onClick={() => removeFilter('platform', v)}>×</button>
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
                    Found {filteredCompanies.length} companies
                </p>

                {/* Results Grid */}
                <div className="row">
                    {filteredCompanies.map(company => {
                        const logoSrc = company.media?.logo_path
                            ? (company.media.logo_path.startsWith('http')
                                ? company.media.logo_path
                                : `/quantum-landscape${company.media.logo_path}`)
                            : null;
                        const nameParts = (company.name || '').split(' ').filter(p => p.trim() !== '');
                        const initials = nameParts.length > 1
                            ? (nameParts[0][0] + nameParts[1][0]).toUpperCase()
                            : nameParts.length === 1 ? nameParts[0].substring(0, 2).toUpperCase() : 'CO';
                        const clean = v => (v && String(v).trim().toLowerCase() !== 'unknown') ? v : null;
                        const location = [clean(company.location?.city), clean(company.location?.country)].filter(Boolean).join(', ');
                        return (
                        <div key={company.id} className="col col--4 margin-bottom--lg">
                            <div className="card inst-card">
                                <div className="card__header company-card-header">
                                    {logoSrc ? (
                                        <div className="inst-logo-ring">
                                            <img className="inst-logo-img" src={logoSrc} alt="" />
                                        </div>
                                    ) : (
                                        <div className="inst-logo-ring inst-logo-placeholder">
                                            <span>{initials}</span>
                                        </div>
                                    )}
                                    <div className="inst-card-title-block">
                                        <h3>{company.name}</h3>
                                        {location && <p className="company-card-location">{location}</p>}
                                    </div>
                                </div>
                                <div className="card__body inst-card-body">
                                    <p className="inst-card-description">{company.short_summary}</p>
                                    <div className="inst-card-badges">
                                        {(company.platforms || []).map(pl => (
                                            <span
                                                key={pl}
                                                className="badge badge--success margin-right--xs clickable-badge"
                                                onClick={() => addFilter('platform', pl)}
                                            >
                                                {pl.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
                                            </span>
                                        ))}
                                        {company.categories?.map(cat => (
                                            <span key={cat} className="badge badge--info margin-right--xs">
                                                {cat}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                                <div className="card__footer">
                                    <Link to={`/?company=${company.id}`} className="button button--primary button--block">
                                        View on Map
                                    </Link>
                                </div>
                            </div>
                        </div>
                        );
                    })}
                    {filteredCompanies.length === 0 && (
                        <div className="col col--12">
                            <div className="alert alert--warning">
                                <p>No companies found matching criteria.</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </Layout>
    );
}

export default Companies;
