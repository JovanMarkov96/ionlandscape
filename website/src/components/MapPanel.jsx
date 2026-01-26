// website/src/components/MapPanel.jsx
import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const defaultCenter = [20, 0];
const defaultZoom = 2;

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

    return (
        <MapContainer center={defaultCenter} zoom={defaultZoom} style={{ height: '100%', width: '100%' }}>
            <TileLayer
                attribution='&copy; OpenStreetMap contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {people.map((f, i) => {
                const geom = f.geometry;
                const props = f.properties || {};
                if (!geom || !geom.coordinates) return null;
                const [lon, lat] = geom.coordinates;
                return (
                    <Marker key={i} position={[lat, lon]}>
                        <Popup>
                            <div>
                                <strong>{props.name}</strong>
                                <p>{props.short_bio}</p>
                                <button onClick={() => onPersonSelect(props.md_filename)}>Open profile</button>
                            </div>
                        </Popup>
                    </Marker>
                );
            })}
        </MapContainer>
    );
}

export default MapPanel;
