// website/src/pages/index.js
import React, { useState } from 'react';
import MapPanel from '../components/MapPanel';
import PersonPanel from '../components/PersonPanel';

export default function Home() {
    const [selectedPersonId, setSelectedPersonId] = useState(null);
    const [selectedLocation, setSelectedLocation] = useState(null);

    return (
        <div style={{ display: 'flex', height: '100vh' }}>
            <div style={{ flex: 1 }}>
                <MapPanel
                    onPersonSelect={(id) => setSelectedPersonId(id)}
                    onLocationSelect={(loc) => setSelectedLocation(loc)}
                />
            </div>
            <div style={{ width: 420, borderLeft: '1px solid #ddd', overflow: 'auto' }}>
                <PersonPanel personId={selectedPersonId} location={selectedLocation} />
            </div>
        </div>
    );
}
