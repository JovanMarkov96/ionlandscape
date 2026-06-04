// website/src/components/MapPanel.jsx
// Self-hosted MapLibre GL JS implementation with a raster basemap
// Zero external dependencies - fully static file hosting
import React, { useEffect, useRef, useMemo, useCallback, useImperativeHandle, forwardRef } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import PlatformFlyout, { PLATFORM_GROUPS } from './PlatformFlyout';

const defaultCenter = [10, 50]; // Centered on Europe
const defaultZoom = 2;

/**
 * Generates the MapLibre style object containing map layers and sources.
 * We use an inline style configuration with public raster tiles so the map
 * can render without an API key or cross-origin failures.
 * 
 * @param {boolean} isDark - Whether the UI is in dark mode
 * @returns {Object} A standalone MapLibre GL style object
 */
const createStyle = (isDark) => ({
    version: 8,
    name: isDark ? 'Quantum Landscape Dark' : 'Quantum Landscape Light',
    sources: {
        basemap: {
            type: 'raster',
            tiles: [
                isDark
                    ? 'https://basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}{r}.png'
                    : 'https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png'
            ],
            tileSize: 256,
            attribution: '© OpenStreetMap contributors © CARTO'
        }
    },
    layers: [
        {
            id: 'basemap',
            type: 'raster',
            source: 'basemap',
            paint: {
                'raster-opacity': 1,
                'raster-fade-duration': 0
            }
        }
    ]
});

/**
 * Groups raw GeoJSON feature entries by their exact lat/long coordinate.
 * This is used so multiple groups at the exact same location show up in the same popup.
 *
 * @param {Array<Object>} features - List of GeoJSON features
 * @returns {Map<string, Array<Object>>} A map of coordinate keys to feature arrays
 */
function groupByCoordinate(features) {
    const groups = new Map();
    for (const f of features) {
        const geom = f.geometry;
        if (!geom || !geom.coordinates) continue;
        const [lon, lat] = geom.coordinates;
        const key = `${lat.toFixed(5)},${lon.toFixed(5)}`;
        if (!groups.has(key)) {
            groups.set(key, []);
        }
        groups.get(key).push(f);
    }
    // Order within a shared location: institutions first, then companies, then
    // people — so the place is named before the researchers sitting there.
    const rank = (f) => {
        const t = f.properties?.entity_type;
        if (t === 'institution') return 0;
        if (t === 'company') return 1;
        return 2;
    };
    for (const [, arr] of groups) {
        arr.sort((a, b) => {
            const r = rank(a) - rank(b);
            if (r !== 0) return r;
            return (a.properties?.id || '').localeCompare(b.properties?.id || '');
        });
    }
    return groups;
}

/**
 * MapPanel Component
 * 
 * Self-hosted MapLibre GL JS interactive map using OpenFreeMap vector tiles.
 * Handles fetching markers, rendering popups, mapping coordinates, and 
 * responding to user marker clicks.
 * 
 * @param {Object} props
 * @param {Function} props.onPersonSelect - Callback executed when a person's profile is clicked in a popup
 * @param {Function} props.onCompanySelect - Callback executed when a company's profile is clicked in a popup 
 * @param {Function} props.onInstitutionSelect - Callback executed when an institution's profile is clicked in a popup 
 * @param {Function} [props.onLocationSelect] - Optional callback for purely location-based clicks
 * @returns {JSX.Element} Interactive map rendering
 */
const MapPanel = forwardRef(function MapPanel({ onPersonSelect, onCompanySelect, onInstitutionSelect, onLocationSelect }, ref) {
    const mapContainerRef = useRef(null);
    const mapRef = useRef(null);
    const markersRef = useRef([]);
    const [people, setPeople] = React.useState([]);
    const [companies, setCompanies] = React.useState([]);
    const [institutions, setInstitutions] = React.useState([]);
    const [filters, setFilters] = React.useState({ people: true, companies: true, institutions: true, platforms: [] });
    const [platformsOpen, setPlatformsOpen] = React.useState(false);

    const togglePlatform = useCallback((groupKey) => {
        setFilters(prev => {
            const set = new Set(prev.platforms);
            set.has(groupKey) ? set.delete(groupKey) : set.add(groupKey);
            return { ...prev, platforms: Array.from(set) };
        });
    }, []);

    // Docusaurus color mode
    const { colorMode } = useColorMode();
    const isDark = colorMode === 'dark';

    // Load data
    useEffect(() => {
        // Load people
        fetch('/quantum-landscape/data/people.geojson')
            .then(res => res.json())
            .then(data => { if (data?.features) setPeople(data.features); })
            .catch(() => {
                fetch('/data/people.geojson')
                    .then(res => res.json())
                    .then(data => setPeople(data.features || []))
                    .catch(e => console.warn('Could not load people.geojson', e));
            });

        // Load companies
        fetch('/quantum-landscape/data/companies.geojson')
            .then(res => res.json())
            .then(data => { if (data?.features) setCompanies(data.features); })
            .catch(() => {
                fetch('/data/companies.geojson')
                    .then(res => res.json())
                    .then(data => setCompanies(data.features || []))
                    .catch(e => console.warn('Could not load companies.json', e));
            });

        // Load institutions
        fetch('/quantum-landscape/data/institutions.geojson')
            .then(res => res.json())
            .then(data => { if (data?.features) setInstitutions(data.features); })
            .catch(() => {
                fetch('/data/institutions.geojson')
                    .then(res => res.json())
                    .then(data => setInstitutions(data.features || []))
                    .catch(e => console.warn('Could not load institutions.geojson', e));
            });
    }, []);

    // Filter and group features
    const displayFeatures = useMemo(() => {
        let features = [];
        if (filters.people) features = features.concat(people);
        if (filters.companies) features = features.concat(companies);
        if (filters.institutions) features = features.concat(institutions);

        if (filters.platforms.length > 0) {
            // Union of the raw platform values for every active group
            const activeValues = new Set(
                PLATFORM_GROUPS
                    .filter(g => filters.platforms.includes(g.key))
                    .flatMap(g => g.values)
            );
            features = features.filter(f =>
                (f.properties?.platforms || []).some(p => activeValues.has(p))
            );
        }
        return features;
    }, [people, companies, institutions, filters]);

    // Per-platform marker counts (across all loaded features, for tile badges)
    const platformCounts = useMemo(() => {
        const counts = {};
        [...people, ...companies, ...institutions].forEach(f => {
            (f.properties?.platforms || []).forEach(p => { counts[p] = (counts[p] || 0) + 1; });
        });
        return counts;
    }, [people, companies, institutions]);

    const coordGroups = useMemo(() => groupByCoordinate(displayFeatures), [displayFeatures]);

    /**
     * Builds HTML content for a single map marker popup based on the 
     * array of features matching that location.
     * 
     * @param {Array<Object>} group - GeoJSON features at this marker
     * @param {string} locationLabel - The calculated City/Country label for this area
     * @returns {string} Raw HTML string required by MapLibre Popup
     */
    const createPopupHTML = useCallback((group, locationLabel) => {
        let html = '<div class="popup-scroll-container">';
        if (locationLabel) {
            html += `<div class="popup-location-header">${locationLabel}</div>`;
        }
        group.forEach((feature, idx) => {
            const props = feature.properties || {};
            const borderClass = idx < group.length - 1 ? 'popup-feature-border' : '';
            // Show institutions instead of description
            const affiliations = props.affiliations || [];
            const cpObj = props.current_position || {};
            const cpInstitution = typeof cpObj === 'string' ? cpObj : (cpObj.institution || '');
            const institutionHtml = affiliations.length > 0
                ? affiliations.map(inst => `<div class="popup-institution">${inst}</div>`).join('')
                : (cpInstitution ? `<div class="popup-institution">${cpInstitution}</div>` : '');

            const isCompany = props.entity_type === 'company';
            const isInstitution = props.entity_type === 'institution';

            let detailText = institutionHtml;
            if (isCompany || isInstitution) {
                // Truncate the preview to a universal length so the logo + a short
                // intro fit in one popup frame; full text is on the profile.
                let summary = props.short_summary || props.short_description || '';
                const LIMIT = 120;
                if (summary.length > LIMIT) {
                    summary = summary.slice(0, LIMIT).replace(/\s+\S*$/, '').trim() + '…';
                }
                detailText = summary;
            }

            let btnTypeClass = 'person'; // Person
            if (isCompany) btnTypeClass = 'company'; // Company
            if (isInstitution) btnTypeClass = 'institution'; // Institution

            // Logo HTML
            let logoHtml = '';
            if (isCompany || isInstitution) {
                if (props.logo_path) {
                    const src = `/quantum-landscape${props.logo_path}`;
                    const safeSrc = src.startsWith('http') || src.startsWith('/quantum-landscape')
                        ? src
                        : `/quantum-landscape${src}`;

                    logoHtml = `
                    <div class="popup-logo-container">
                        <img src="${safeSrc}" onerror="this.onerror=null; this.src='${src}';" />
                    </div>`;
                } else if (isCompany) {
                    const nameParts = (props.name || '').split(' ').filter(p => p.trim() !== '');
                    let initials = 'CO';
                    if (nameParts.length > 1) initials = (nameParts[0][0] + nameParts[1][0]).toUpperCase();
                    else if (nameParts.length === 1) initials = nameParts[0].substring(0, 2).toUpperCase();

                    logoHtml = `
                    <div class="popup-logo-placeholder">
                        ${initials}
                    </div>`;
                }
            }

            const dataType = isCompany ? 'company' : (isInstitution ? 'institution' : 'person');
            const typeLabel = isCompany ? '<span class="popup-badge company">Co</span>' : (isInstitution ? '<span class="popup-badge institution">Inst</span>' : '');

            html += `
                <div class="popup-feature-wrapper ${borderClass}">
                    <div class="popup-feature-header">
                        <span class="popup-feature-title">
                            ${logoHtml}
                            <span>${props.name || 'Unknown'}</span>
                        </span>
                        ${typeLabel}
                    </div>
                    <div style="font-size: 0.85em; margin-bottom: 4px;" class="popup-detail-text">${detailText}</div>
                    <button 
                        class="maplibre-popup-btn popup-button ${btnTypeClass}" 
                        data-id="${props.id}"
                        data-type="${dataType}">
                        Open profile
                    </button>
                </div>
            `;
        });
        html += '</div>';
        return html;
    }, []);

    // Initialize map
    useEffect(() => {
        if (!mapContainerRef.current || mapRef.current) return;

        const map = new maplibregl.Map({
            container: mapContainerRef.current,
            style: createStyle(isDark),
            center: defaultCenter,
            zoom: defaultZoom,
            maxZoom: 18,
            minZoom: 1
        });

        map.addControl(new maplibregl.NavigationControl(), 'bottom-right');
        map.addControl(new maplibregl.AttributionControl({
            compact: true,
            customAttribution: '© OpenStreetMap contributors'
        }));

        // Handle popup button clicks
        map.getContainer().addEventListener('click', (e) => {
            if (e.target.classList.contains('maplibre-popup-btn')) {
                const id = e.target.getAttribute('data-id');
                const type = e.target.getAttribute('data-type');

                if (type === 'company' && onCompanySelect) {
                    onCompanySelect(id);
                } else if (type === 'institution' && onInstitutionSelect) {
                    onInstitutionSelect(id);
                } else if (onPersonSelect) {
                    onPersonSelect(id);
                }
            }
        });

        map.on('load', () => {
            console.log('MapLibre GL JS loaded successfully - Self-hosted, zero external dependencies');
            const toggleZoomClass = () => {
                if (mapContainerRef.current) {
                    if (map.getZoom() >= 10) {
                        mapContainerRef.current.classList.add('map-zoomed-in');
                    } else {
                        mapContainerRef.current.classList.remove('map-zoomed-in');
                    }
                }
            };
            map.on('zoom', toggleZoomClass);
            toggleZoomClass(); // Initial check
        });

        mapRef.current = map;

        return () => {
            markersRef.current.forEach(m => m.remove());
            markersRef.current = [];
            map.remove();
            mapRef.current = null;
        };
    }, []);

    // Update style when color mode changes
    useEffect(() => {
        if (mapRef.current) {
            mapRef.current.setStyle(createStyle(isDark));
        }
    }, [isDark]);

    /**
     * Expose a `flyTo` method so the parent component can programmatically
     * zoom the map to a given coordinate (used by "Show in Map" buttons).
     */
    useImperativeHandle(ref, () => ({
        flyTo(lat, lon, zoom = 10) {
            if (mapRef.current) {
                mapRef.current.flyTo({ center: [lon, lat], zoom, duration: 1500 });
            }
        }
    }), []);

    // Add markers when data changes
    useEffect(() => {
        if (!mapRef.current) return;

        // Clear existing markers
        markersRef.current.forEach(m => m.remove());
        markersRef.current = [];

        // Add new markers
        Array.from(coordGroups.entries()).forEach(([, group]) => {
            const firstFeature = group[0];
            const [lon, lat] = firstFeature.geometry.coordinates;
            const props = firstFeature.properties || {};

            const isCompanyGroup = group.some(f => f.properties?.entity_type === 'company');
            const isInstitutionGroup = group.some(f => f.properties?.entity_type === 'institution');

            let markerColor = '#4f46e5'; // Person default
            if (isCompanyGroup) markerColor = '#e65100'; // Company
            if (isInstitutionGroup) markerColor = '#14B8A6'; // Institution

            const locationLabel = props.city && props.country
                ? `${props.city}, ${props.country}`
                : null;

            // Create custom marker element
            const el = document.createElement('div');
            el.classList.add('ion-marker-enter'); // entrance animation

            let anchorType = 'bottom';
            let popupOffset = [0, -40]; // Popup floats above the pin tip

            const safeId = (props.id || 'new').replace(/[^a-zA-Z0-9_-]/g, '-');
            const svgPinContent = `
                <svg viewBox="0 0 24 24" width="36" height="36" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.35)); transition: filter 0.3s ease;">
                    <defs>
                        <linearGradient id="glassGrad-${safeId}" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="${markerColor}" stop-opacity="0.6" />
                            <stop offset="100%" stop-color="${markerColor}" stop-opacity="0.95" />
                        </linearGradient>
                        <radialGradient id="glassReflect-${safeId}" cx="30%" cy="30%" r="50%">
                            <stop offset="0%" stop-color="white" stop-opacity="0.6"/>
                            <stop offset="100%" stop-color="white" stop-opacity="0"/>
                        </radialGradient>
                    </defs>
                    <!-- Stroke/Outline -->
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" 
                          fill="url(#glassGrad-${safeId})" 
                          stroke="rgba(255,255,255,0.9)" 
                          stroke-width="1.2" />
                    <!-- Specular Highlight Overlay -->
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" 
                          fill="url(#glassReflect-${safeId})" 
                          pointer-events="none" />
                </svg>
            `;

            // Force institutions to use standard pins, only companies get logos
            const companyFeature = group.find(f => f.properties?.entity_type === 'company');
            if (companyFeature) {
                el.className = 'ion-marker-company';
                let logoHtml = '';

                if (companyFeature.properties?.logo_path) {
                    // Logo Marker
                    const src = `/quantum-landscape${companyFeature.properties.logo_path}`;
                    logoHtml = `<div class="ion-marker-logo" style="background-image: url('${src}')"></div>`;
                } else {
                    // Placeholder Logo Marker
                    const nameParts = (companyFeature.properties.name || '').split(' ').filter(p => p.trim() !== '');
                    let initials = 'CO';
                    if (nameParts.length > 1) initials = (nameParts[0][0] + nameParts[1][0]).toUpperCase();
                    else if (nameParts.length === 1) initials = nameParts[0].substring(0, 2).toUpperCase();
                    logoHtml = `<div class="ion-marker-placeholder"><span>${initials}</span></div>`;
                }

                // Append both representations inside the container
                el.innerHTML = `
                    <div class="ion-marker-pin">${svgPinContent}</div>
                    ${logoHtml}
                `;
                anchorType = 'bottom';
                popupOffset = [0, -40];
            } else {
                // Liquid Glass SVG Pin Marker (Matches Legend Icon)
                el.className = 'ion-marker-pin';
                el.innerHTML = svgPinContent;
                anchorType = 'bottom';
                popupOffset = [0, -40];
            }

            const popup = new maplibregl.Popup({ offset: popupOffset, maxWidth: '300px' })
                .setHTML(createPopupHTML(group, locationLabel));

            const marker = new maplibregl.Marker({ element: el, anchor: anchorType })
                .setLngLat([lon, lat])
                .setPopup(popup)
                .addTo(mapRef.current);

            markersRef.current.push(marker);
        });
    }, [coordGroups, createPopupHTML]);

    return (
        <div className="map-layout-wrapper">
            <div
                ref={mapContainerRef}
                className="map-viewport"
            />
            {/* Filter Controls - Liquid Glass Vertical */}
            <div className="map-filters-container">
                <div
                    className="map-filter-btn filter-btn-people"
                    onClick={() => setFilters(prev => ({ ...prev, people: !prev.people }))}
                    data-active={filters.people}
                    title="Toggle People"
                >
                    <svg viewBox="0 0 24 24" width="22" height="22">
                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" />
                    </svg>
                    <span>People</span>
                </div>

                <div
                    className="map-filter-btn filter-btn-companies"
                    onClick={() => setFilters(prev => ({ ...prev, companies: !prev.companies }))}
                    data-active={filters.companies}
                    title="Toggle Companies"
                >
                    <svg viewBox="0 0 24 24" width="22" height="22">
                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" />
                    </svg>
                    <span>Companies</span>
                </div>

                <div
                    className="map-filter-btn filter-btn-institutions"
                    onClick={() => setFilters(prev => ({ ...prev, institutions: !prev.institutions }))}
                    data-active={filters.institutions}
                    title="Toggle Institutions"
                >
                    <svg viewBox="0 0 24 24" width="22" height="22">
                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" />
                    </svg>
                    <span>Institutions</span>
                </div>

                {/* Platform Filter — collapsible tech-tile flyout */}
                <div className="map-platforms-divider" />
                <div
                    className="map-filter-btn filter-btn-platforms"
                    onClick={() => setPlatformsOpen(o => !o)}
                    data-active={platformsOpen || filters.platforms.length > 0}
                    title="Filter by platform"
                    role="button"
                    aria-expanded={platformsOpen}
                >
                    <svg viewBox="0 0 24 24" width="22" height="22">
                        <path d="M3 5h7v7H3V5zm11 0h7v7h-7V5zM3 16h7v3H3v-3zm11 0h7v3h-7v-3z" />
                    </svg>
                    <span>Platforms</span>
                    <span
                        className="platforms-active-dot"
                        data-on={filters.platforms.length > 0}
                        aria-label={filters.platforms.length > 0 ? `${filters.platforms.length} platforms selected` : undefined}
                    />
                    <svg className="platforms-chevron" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
                        <path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" strokeWidth="2.4"
                            strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                </div>

                <PlatformFlyout
                    open={platformsOpen}
                    active={filters.platforms}
                    onToggle={togglePlatform}
                    counts={platformCounts}
                />
            </div>
        </div>
    );
});
export default MapPanel;

