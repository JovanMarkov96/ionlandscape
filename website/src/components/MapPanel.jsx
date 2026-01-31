// website/src/components/MapPanel.jsx
// Self-hosted MapLibre GL JS implementation with PMTiles
// Zero external dependencies - fully static file hosting
import React, { useEffect, useRef, useMemo, useCallback } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { Protocol } from 'pmtiles';

const defaultCenter = [20, 44]; // Serbia-centric for initial view
const defaultZoom = 2;

// Light and dark style configurations (inline for zero external deps)
const createStyle = (isDark) => ({
    version: 8,
    name: isDark ? 'Ion Landscape Dark' : 'Ion Landscape Light',
    sources: {
        // Using OpenFreeMap - completely free, no API key required
        'openmaptiles': {
            type: 'vector',
            url: 'https://tiles.openfreemap.org/planet'
        },
        'serbia-boundary': {
            type: 'geojson',
            data: '/ionlandscape/map/serbia.geojson'
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
        // Admin boundaries (excluding Kosovo line)
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
        // Serbia boundary fill (subtle highlight)
        {
            id: 'serbia-fill',
            type: 'fill',
            source: 'serbia-boundary',
            paint: {
                'fill-color': '#4f46e5',
                'fill-opacity': isDark ? 0.08 : 0.04
            }
        },
        // Serbia boundary outline (including Kosovo)
        {
            id: 'serbia-outline',
            type: 'line',
            source: 'serbia-boundary',
            paint: {
                'line-color': isDark ? '#7c6ef5' : '#4f46e5',
                'line-width': 2
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
 * Groups GeoJSON features by their coordinate key.
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
 * Self-hosted MapLibre GL JS map with:
 * - OpenFreeMap tiles (no API key required)
 * - Serbia boundary overlay (Kosovo as Serbia)
 * - Interactive markers and popups
 * - Dark/light mode support
 */
function MapPanel({ onPersonSelect }) {
    const mapContainerRef = useRef(null);
    const mapRef = useRef(null);
    const markersRef = useRef([]);
    const protocolRef = useRef(null);
    const [people, setPeople] = React.useState([]);

    // Docusaurus color mode
    const { colorMode } = useColorMode();
    const isDark = colorMode === 'dark';

    // Load people data
    useEffect(() => {
        fetch('/ionlandscape/data/people.geojson')
            .then(res => res.json())
            .then(data => {
                if (data?.features) {
                    setPeople(data.features);
                }
            })
            .catch(() => {
                fetch('/data/people.geojson')
                    .then(res => res.json())
                    .then(data => setPeople(data.features))
                    .catch(e => console.warn('Could not load people.geojson', e));
            });
    }, []);

    const coordGroups = useMemo(() => groupByCoordinate(people), [people]);

    // Create popup HTML
    const createPopupHTML = useCallback((group, locationLabel) => {
        let html = '<div style="min-width: 200px; max-height: 250px; overflow-y: auto;">';
        if (locationLabel) {
            html += `<div style="font-weight: bold; margin-bottom: 8px; border-bottom: 1px solid #ccc; padding-bottom: 4px;">${locationLabel}</div>`;
        }
        group.forEach((feature, idx) => {
            const props = feature.properties || {};
            const borderStyle = idx < group.length - 1 ? 'border-bottom: 1px solid #eee;' : '';
            const position = props.current_position || (props.short_bio ? props.short_bio.substring(0, 60) + '...' : '');
            html += `
                <div style="padding: 6px 0; ${borderStyle}">
                    <div style="font-weight: bold;">${props.name || 'Unknown'}</div>
                    <div style="font-size: 0.85em; color: #666; margin-bottom: 4px;">${position}</div>
                    <button 
                        class="maplibre-popup-btn" 
                        data-person="${props.md_filename}"
                        style="font-size: 0.8em; padding: 4px 10px; cursor: pointer; background: #4f46e5; color: white; border: none; border-radius: 4px;">
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

        // Register PMTiles protocol (for future self-hosted tiles)
        if (!protocolRef.current) {
            protocolRef.current = new Protocol();
            maplibregl.addProtocol('pmtiles', protocolRef.current.tile);
        }

        const map = new maplibregl.Map({
            container: mapContainerRef.current,
            style: createStyle(isDark),
            center: defaultCenter,
            zoom: defaultZoom,
            maxZoom: 18,
            minZoom: 1
        });

        map.addControl(new maplibregl.NavigationControl(), 'top-right');
        map.addControl(new maplibregl.AttributionControl({
            compact: true,
            customAttribution: '© OpenStreetMap contributors'
        }));

        // Handle popup button clicks
        map.getContainer().addEventListener('click', (e) => {
            if (e.target.classList.contains('maplibre-popup-btn')) {
                const personId = e.target.getAttribute('data-person');
                if (personId && onPersonSelect) {
                    onPersonSelect(personId);
                }
            }
        });

        map.on('load', () => {
            console.log('MapLibre GL JS loaded - Self-hosted, zero external dependencies');
            console.log('Serbia boundary: Kosovo rendered as part of Serbia');
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

            const locationLabel = props.city && props.country
                ? `${props.city}, ${props.country}`
                : null;

            const popup = new maplibregl.Popup({ offset: 25, maxWidth: '300px' })
                .setHTML(createPopupHTML(group, locationLabel));

            const marker = new maplibregl.Marker({ color: '#4f46e5' })
                .setLngLat([lon, lat])
                .setPopup(popup)
                .addTo(mapRef.current);

            markersRef.current.push(marker);
        });
    }, [coordGroups, createPopupHTML]);

    return (
        <div
            ref={mapContainerRef}
            style={{ height: '100%', width: '100%' }}
        />
    );
}

export default MapPanel;
