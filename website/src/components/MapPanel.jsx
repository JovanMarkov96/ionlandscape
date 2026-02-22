// website/src/components/MapPanel.jsx
// Self-hosted MapLibre GL JS implementation with PMTiles
// Zero external dependencies - fully static file hosting
import React, { useEffect, useRef, useMemo, useCallback, useImperativeHandle, forwardRef } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

const defaultCenter = [10, 50]; // Centered on Europe
const defaultZoom = 2;

/**
 * Generates the MapLibre style object containing map layers and sources.
 * We use an inline style configuration to utilize OpenFreeMap without an API key.
 * 
 * @param {boolean} isDark - Whether the UI is in dark mode
 * @returns {Object} A standalone MapLibre GL style object
 */
const createStyle = (isDark) => ({
    version: 8,
    name: isDark ? 'Ion Landscape Dark' : 'Ion Landscape Light',
    sources: {
        // Using OpenFreeMap - completely free, no API key required
        'openmaptiles': {
            type: 'vector',
            url: 'https://tiles.openfreemap.org/planet'
        }
    },
    glyphs: 'https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf',
    layers: [
        // Background
        {
            id: 'background',
            type: 'background',
            paint: {
                'background-color': isDark ? '#1a1a2e' : '#f8f4f0'
            }
        },
        // Water
        {
            id: 'water',
            type: 'fill',
            source: 'openmaptiles',
            'source-layer': 'water',
            paint: {
                'fill-color': isDark ? '#1e3a5f' : '#a0c8f0'
            }
        },
        // Landcover
        {
            id: 'landcover',
            type: 'fill',
            source: 'openmaptiles',
            'source-layer': 'landcover',
            paint: {
                'fill-color': isDark ? '#2d4a3e' : '#d8e8c8',
                'fill-opacity': 0.4
            }
        },
        // Parks
        {
            id: 'park',
            type: 'fill',
            source: 'openmaptiles',
            'source-layer': 'park',
            paint: {
                'fill-color': isDark ? '#2d4a3e' : '#c8e6c8',
                'fill-opacity': 0.5
            }
        },
        // Buildings
        {
            id: 'building',
            type: 'fill',
            source: 'openmaptiles',
            'source-layer': 'building',
            paint: {
                'fill-color': isDark ? '#2a2a3e' : '#ddd',
                'fill-opacity': 0.7
            },
            minzoom: 13
        },
        // Roads - minor
        {
            id: 'road-minor',
            type: 'line',
            source: 'openmaptiles',
            'source-layer': 'transportation',
            filter: ['in', 'class', 'minor', 'service', 'path'],
            paint: {
                'line-color': isDark ? '#3a3a4e' : '#fff',
                'line-width': 1
            },
            minzoom: 12
        },
        // Roads - secondary
        {
            id: 'road-secondary',
            type: 'line',
            source: 'openmaptiles',
            'source-layer': 'transportation',
            filter: ['in', 'class', 'secondary', 'tertiary'],
            paint: {
                'line-color': isDark ? '#4a4a5e' : '#fefeb3',
                'line-width': 2
            },
            minzoom: 8
        },
        // Roads - primary
        {
            id: 'road-primary',
            type: 'line',
            source: 'openmaptiles',
            'source-layer': 'transportation',
            filter: ['==', 'class', 'primary'],
            paint: {
                'line-color': isDark ? '#5a5a6e' : '#fcd6a4',
                'line-width': 3
            },
            minzoom: 6
        },
        // Roads - highway
        {
            id: 'road-motorway',
            type: 'line',
            source: 'openmaptiles',
            'source-layer': 'transportation',
            filter: ['==', 'class', 'motorway'],
            paint: {
                'line-color': isDark ? '#e9ac77' : '#e9ac77',
                'line-width': 4
            },
            minzoom: 4
        },
        // Admin boundaries
        {
            id: 'admin-boundary',
            type: 'line',
            source: 'openmaptiles',
            'source-layer': 'boundary',
            filter: ['all',
                ['==', 'admin_level', 2],
                ['!=', 'disputed', 1],
                ['!=', 'maritime', 1]
            ],
            paint: {
                'line-color': isDark ? '#6a6a7e' : '#9e9cab',
                'line-width': 1,
                'line-dasharray': [3, 2]
            }
        },

        // Place labels - cities
        {
            id: 'place-city',
            type: 'symbol',
            source: 'openmaptiles',
            'source-layer': 'place',
            filter: ['==', 'class', 'city'],
            layout: {
                'text-field': ['get', 'name'],
                'text-font': ['Noto Sans Regular'],
                'text-size': 14
            },
            paint: {
                'text-color': isDark ? '#e0e0e0' : '#333',
                'text-halo-color': isDark ? '#1a1a2e' : '#fff',
                'text-halo-width': 1.5
            },
            minzoom: 5
        },
        // Place labels - countries
        {
            id: 'place-country',
            type: 'symbol',
            source: 'openmaptiles',
            'source-layer': 'place',
            filter: ['==', 'class', 'country'],
            layout: {
                'text-field': ['get', 'name'],
                'text-font': ['Noto Sans Bold'],
                'text-size': 14,
                'text-transform': 'uppercase',
                'text-letter-spacing': 0.1
            },
            paint: {
                'text-color': isDark ? '#b0b0b0' : '#555',
                'text-halo-color': isDark ? '#1a1a2e' : '#fff',
                'text-halo-width': 2
            },
            minzoom: 2,
            maxzoom: 6
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
    for (const [, arr] of groups) {
        arr.sort((a, b) => {
            const idA = a.properties?.id || '';
            const idB = b.properties?.id || '';
            return idA.localeCompare(idB);
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
    const [filters, setFilters] = React.useState({ people: true, companies: true, institutions: true });

    // Docusaurus color mode
    const { colorMode } = useColorMode();
    const isDark = colorMode === 'dark';

    // Load data
    useEffect(() => {
        // Load people
        fetch('/ionlandscape/data/people.geojson')
            .then(res => res.json())
            .then(data => { if (data?.features) setPeople(data.features); })
            .catch(() => {
                fetch('/data/people.geojson')
                    .then(res => res.json())
                    .then(data => setPeople(data.features || []))
                    .catch(e => console.warn('Could not load people.geojson', e));
            });

        // Load companies
        fetch('/ionlandscape/data/companies.geojson')
            .then(res => res.json())
            .then(data => { if (data?.features) setCompanies(data.features); })
            .catch(() => {
                fetch('/data/companies.geojson')
                    .then(res => res.json())
                    .then(data => setCompanies(data.features || []))
                    .catch(e => console.warn('Could not load companies.json', e));
            });

        // Load institutions
        fetch('/ionlandscape/data/institutions.geojson')
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
        return features;
    }, [people, companies, institutions, filters]);

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
                detailText = props.short_summary || props.short_description || '';
            }

            let btnTypeClass = 'person'; // Person
            if (isCompany) btnTypeClass = 'company'; // Company
            if (isInstitution) btnTypeClass = 'institution'; // Institution

            // Logo HTML
            let logoHtml = '';
            if (isCompany || isInstitution) {
                if (props.logo_path) {
                    const src = `/ionlandscape${props.logo_path}`;
                    const safeSrc = src.startsWith('http') || src.startsWith('/ionlandscape')
                        ? src
                        : `/ionlandscape${src}`;

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

            // Force institutions to use standard pins, only companies get logos
            const companyFeature = group.find(f => f.properties?.entity_type === 'company');
            if (companyFeature) {
                if (companyFeature.properties?.logo_path) {
                    // Logo Marker
                    el.className = 'ion-marker-logo';
                    const src = `/ionlandscape${companyFeature.properties.logo_path}`;
                    el.style.backgroundImage = `url('${src}')`;
                } else {
                    // Placeholder Logo Marker
                    el.className = 'ion-marker-placeholder';
                    const nameParts = (companyFeature.properties.name || '').split(' ').filter(p => p.trim() !== '');
                    let initials = 'CO';
                    if (nameParts.length > 1) initials = (nameParts[0][0] + nameParts[1][0]).toUpperCase();
                    else if (nameParts.length === 1) initials = nameParts[0].substring(0, 2).toUpperCase();
                    el.innerHTML = `<span>${initials}</span>`;
                }
                anchorType = 'center'; // Circles anchor in their true center
                popupOffset = [0, -28];
            } else {
                // Liquid Glass SVG Pin Marker (Matches Legend Icon)
                el.className = 'ion-marker-pin';
                const safeId = (props.id || 'new').replace(/[^a-zA-Z0-9_-]/g, '-');

                // Construct inline SVG with dynamic color and glass overlay
                el.innerHTML = `
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
            </div>
        </div>
    );
});
export default MapPanel;

