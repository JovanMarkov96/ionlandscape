// website/src/pages/index.js
import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

function HomeContent() {
    const [selectedPersonId, setSelectedPersonId] = useState(null);
    const [selectedLocation, setSelectedLocation] = useState(null);

    // These components require browser APIs
    const MapPanel = require('../components/MapPanel').default;
    const PersonPanel = require('../components/PersonPanel').default;

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

export default function Home() {
    return (
        <BrowserOnly fallback={<div>Loading...</div>}>
            {() => <HomeContent />}
        </BrowserOnly>
    );
}
