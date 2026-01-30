// website/src/components/MapPanel.jsx
import React, { useEffect, useMemo } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const defaultCenter = [20, 0];
const defaultZoom = 2;

/**
 * Groups GeoJSON features by their coordinate key.
 * @param {Array} features - Array of GeoJSON features
 * @returns {Map} Map of coordKey -> array of features
 */
function groupByCoordinate(features) {
    const groups = new Map();
    for (const f of features) {
        const geom = f.geometry;
        if (!geom || !geom.coordinates) continue;
        const [lon, lat] = geom.coordinates;
        // Use fixed precision to group identical coords
        const key = `${lat.toFixed(5)},${lon.toFixed(5)}`;
        if (!groups.has(key)) {
            groups.set(key, []);
        }
        groups.get(key).push(f);
    }
    // Sort people within each group by id for deterministic order
    for (const [key, arr] of groups) {
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
 * Renders an interactive Leaflet map displaying researchers/groups as markers.
 * - Clusters people by location (city/coordinates).
 * - Clicking a marker opens a Popup with a list of people at that location.
 * - Clicking "Open profile" selects a person.
 * 
 * @param {Object} props
 * @param {Function} props.onPersonSelect - Callback when a person is selected (md_filename)
 * @param {Function} props.onLocationSelect - Callback when a location is selected (unused currently)
 */
function MapPanel({ onPersonSelect, onLocationSelect }) {
    const [people, setPeople] = React.useState([]);

    useEffect(() => {
        fetch('/ionlandscape/data/people.geojson')
            .then(res => res.json())
            .then(data => {
                if (data && data.features) {
                    setPeople(data.features);
                }
            }).catch(err => {
                // fallback: try from /data/people.geojson
                fetch('/data/people.geojson')
                    .then(res => res.json())
                    .then(data => setPeople(data.features))
                    .catch(e => console.warn("Could not load people.geojson", e));
            });
    }, []);

    // Fix default marker icons for Leaflet in many bundlers
    useEffect(() => {
        delete L.Icon.Default.prototype._getIconUrl;
        L.Icon.Default.mergeOptions({
            iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
            iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
            shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        });
    }, []);

    // Group features by coordinate
    const coordGroups = useMemo(() => groupByCoordinate(people), [people]);

    // Docusaurus color mode hook
    const { colorMode } = useColorMode();
    const isDark = colorMode === 'dark';

    // CartoDB Tile URLs
    const lightTile = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png";
    const darkTile = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png";

    return (
        <MapContainer center={defaultCenter} zoom={defaultZoom} style={{ height: '100%', width: '100%' }}>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                url={isDark ? darkTile : lightTile}
            />
            {Array.from(coordGroups.entries()).map(([coordKey, group]) => {
                const firstFeature = group[0];
                const [lon, lat] = firstFeature.geometry.coordinates;
                const firstProps = firstFeature.properties || {};
                // Try to get location info from first person
                const locationLabel = firstProps.city && firstProps.country
                    ? `${firstProps.city}, ${firstProps.country}`
                    : null;

                return (
                    <Marker key={coordKey} position={[lat, lon]}>
                        <Popup>
                            <div style={{ minWidth: '200px' }}>
                                {locationLabel && (
                                    <div style={{
                                        fontWeight: 'bold',
                                        marginBottom: '8px',
                                        borderBottom: '1px solid #ccc',
                                        paddingBottom: '4px'
                                    }}>
                                        {locationLabel}
                                    </div>
                                )}
                                <div style={{
                                    maxHeight: '200px',
                                    overflowY: 'auto'
                                }}>
                                    {group.map((feature, idx) => {
                                        const props = feature.properties || {};
                                        return (
                                            <div
                                                key={props.md_filename || idx}
                                                style={{
                                                    padding: '6px 0',
                                                    borderBottom: idx < group.length - 1 ? '1px solid #eee' : 'none'
                                                }}
                                            >
                                                <div style={{ fontWeight: 'bold' }}>
                                                    {props.name}
                                                </div>
                                                <div style={{
                                                    fontSize: '0.85em',
                                                    color: '#666',
                                                    marginBottom: '4px'
                                                }}>
                                                    {props.current_position || props.short_bio?.substring(0, 60) + '...' || ''}
                                                </div>
                                                <button
                                                    onClick={() => onPersonSelect(props.md_filename)}
                                                    style={{
                                                        fontSize: '0.8em',
                                                        padding: '2px 8px',
                                                        cursor: 'pointer'
                                                    }}
                                                >
                                                    Open profile
                                                </button>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        </Popup>
                    </Marker>
                );
            })}
        </MapContainer>
    );
}

export default MapPanel;
