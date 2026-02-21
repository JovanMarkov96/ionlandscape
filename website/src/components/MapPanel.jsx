// website/src/components/MapPanel.jsx
// Self-hosted MapLibre GL JS implementation with PMTiles
// Zero external dependencies - fully static file hosting
import React, { useEffect, useRef, useMemo, useCallback } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
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
 * @param {Function} [props.onLocationSelect] - Optional callback for purely location-based clicks
 * @returns {JSX.Element} Interactive map rendering
 */
function MapPanel({ onPersonSelect, onCompanySelect, onLocationSelect }) {
    const mapContainerRef = useRef(null);
    const mapRef = useRef(null);
    const markersRef = useRef([]);
    const [people, setPeople] = React.useState([]);
    const [companies, setCompanies] = React.useState([]);
    const [filters, setFilters] = React.useState({ people: true, companies: true });
    // Collapsible Filters State
    const [showFilters, setShowFilters] = React.useState(false);

    useEffect(() => {
        // Expand by default on desktop
        if (typeof window !== 'undefined' && window.innerWidth > 768) {
            setShowFilters(true);
        }
    }, []);

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
    }, []);

    // Filter and group features
    const displayFeatures = useMemo(() => {
        let features = [];
        if (filters.people) features = features.concat(people);
        if (filters.companies) features = features.concat(companies);
        return features;
    }, [people, companies, filters]);

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
        let html = '<div style="min-width: 200px; max-height: 250px; overflow-y: auto;">';
        if (locationLabel) {
            html += `<div style="font-weight: bold; margin-bottom: 8px; border-bottom: 1px solid #ccc; padding-bottom: 4px;">${locationLabel}</div>`;
        }
        group.forEach((feature, idx) => {
            const props = feature.properties || {};
            const borderStyle = idx < group.length - 1 ? 'border-bottom: 1px solid #eee;' : '';
            // Show institutions instead of description
            const affiliations = props.affiliations || [];
            const cpObj = props.current_position || {};
            const cpInstitution = typeof cpObj === 'string' ? cpObj : (cpObj.institution || '');
            const institutionHtml = affiliations.length > 0
                ? affiliations.map(inst => `<div class="popup-institution">${inst}</div>`).join('')
                : (cpInstitution ? `<div class="popup-institution">${cpInstitution}</div>` : '');
            const isCompany = props.entity_type === 'company';
            const detailText = isCompany ? (props.short_summary || '') : institutionHtml;
            const btnColor = isCompany ? '#e65100' : '#4f46e5';

            // Logo HTML
            let logoHtml = '';
            if (isCompany && props.logo_path) {
                // Ensure /ionlandscape prefix if needed, or handle it via onerror in img tag (harder in string, so simple first)
                const src = `/ionlandscape${props.logo_path}`;
                const fallback = props.logo_path;

                // Ensure path has prefix for GitHub Pages
                const safeSrc = src.startsWith('http') || src.startsWith('/ionlandscape')
                    ? src
                    : `/ionlandscape${src}`;

                logoHtml = `
                <div class="popup-logo-container">
                    <img src="${safeSrc}" onerror="this.onerror=null; this.src='${src}';" />
                </div>`;
            }

            html += `
                <div style="padding: 6px 0; ${borderStyle}">
                    <div style="font-weight: bold; display: flex; align-items: center; justify-content: space-between;">
                        <span style="display: flex; align-items: center;">
                            ${logoHtml}
                            <span>${props.name || 'Unknown'}</span>
                        </span>
                        ${isCompany ? '<span style="font-size: 0.7em; background: #e65100; color: white; padding: 1px 4px; border-radius: 3px;">Co</span>' : ''}
                    </div>
                    <div style="font-size: 0.85em; margin-bottom: 4px;" class="popup-detail-text">${detailText}</div>
                    <button 
                        class="maplibre-popup-btn" 
                        data-id="${props.id}"
                        data-type="${isCompany ? 'company' : 'person'}"
                        style="font-size: 0.8em; padding: 4px 10px; cursor: pointer; background: ${btnColor}; color: white; border: none; border-radius: 4px;">
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
                } else if (onPersonSelect) {
                    onPersonSelect(id);
                }
            }
        });

        map.on('load', () => {
            console.log('MapLibre GL JS loaded - Self-hosted, zero external dependencies');
        });

        map.on('load', () => {
            console.log('MapLibre GL JS loaded successfully');
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
            const markerColor = isCompanyGroup ? '#e65100' : '#4f46e5';

            const locationLabel = props.city && props.country
                ? `${props.city}, ${props.country}`
                : null;

            const popup = new maplibregl.Popup({ offset: 35, maxWidth: '300px' })
                .setHTML(createPopupHTML(group, locationLabel));

            // Create custom marker element
            const el = document.createElement('div');

            // Check for logo (Quantum Art or other companies)
            const logoFeature = group.find(f => f.properties?.logo_path);

            if (logoFeature && logoFeature.properties.logo_path) {
                // Logo Marker
                el.className = 'ion-marker-logo';
                // Ensure correct path (prepend /ionlandscape if needed, or if path is absolute/relative correctly)
                // Assuming logo_path starts with /, e.g. /img/logos/quantum-art.png
                // Locally or on prod, might need prefix. logic in popup used /ionlandscape prefix.
                // Let's use CSS background-image.
                const src = `/ionlandscape${logoFeature.properties.logo_path}`;
                el.style.backgroundImage = `url('${src}')`;
                // Add fallback error handling? Hard with bg image.
            } else {
                // Teardrop Pin Marker
                el.className = 'ion-marker-pin';
                el.style.backgroundColor = markerColor;
            }

            const marker = new maplibregl.Marker({ element: el })
                .setLngLat([lon, lat])
                .setPopup(popup)
                .addTo(mapRef.current);

            markersRef.current.push(marker);
        });
    }, [coordGroups, createPopupHTML]);

    return (
        <div style={{ position: 'relative', height: '100%', width: '100%' }}>
            <div
                ref={mapContainerRef}
                style={{ height: '100%', width: '100%' }}
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
            </div>
        </div>
    );
}

export default MapPanel;
