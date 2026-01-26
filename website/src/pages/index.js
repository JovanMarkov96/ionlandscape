// website/src/pages/index.js
import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

export default function Home() {
    return (
        <BrowserOnly fallback={<div>Loading...</div>}>
            {() => {
                const MapPanel = require('../components/MapPanel').default;
                const PersonPanel = require('../components/PersonPanel').default;
                
                function HomeContent() {
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
                
                return <HomeContent />;
            }}
        </BrowserOnly>
    );
}
