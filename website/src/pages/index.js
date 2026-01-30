// website/src/pages/index.js
import React, { useState, useEffect } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

function HomeContent() {
    const [selectedPersonId, setSelectedPersonId] = useState(null);
    const [selectedLocation, setSelectedLocation] = useState(null);
    const [isPanelOpen, setIsPanelOpen] = useState(false);

    // These components require browser APIs
    const MapPanel = require('../components/MapPanel').default;
    const PersonPanel = require('../components/PersonPanel').default;

    // Check for ?person=ID in URL
    useEffect(() => {
        const searchParams = new URLSearchParams(window.location.search);
        const personId = searchParams.get('person');
        if (personId) {
            setSelectedPersonId(personId);
            setIsPanelOpen(true);

            // Clean URL without reloading
            const newUrl = window.location.pathname;
            window.history.replaceState({}, '', newUrl);
        }
    }, []);

    // Auto-open panel when a person is selected (mobile)
    useEffect(() => {
        if (selectedPersonId) {
            setIsPanelOpen(true);
        }
    }, [selectedPersonId]);

    const handlePersonSelect = (id) => {
        setSelectedPersonId(id);
        setIsPanelOpen(true); // Open panel when person selected
    };

    const handleClosePanel = () => {
        setIsPanelOpen(false);
    };

    const handleClearProfile = () => {
        setSelectedPersonId(null);
        setSelectedLocation(null);
    };

    return (
        <div className="ion-landscape-container">
            <div className="ion-landscape-map">
                <MapPanel
                    onPersonSelect={handlePersonSelect}
                    onLocationSelect={(loc) => setSelectedLocation(loc)}
                />
            </div>
            <div className={`ion-landscape-panel ${isPanelOpen ? 'panel-open' : ''}`}>
                <button
                    className="back-to-map-btn"
                    onClick={handleClosePanel}
                >
                    ← Back to Map
                </button>
                <PersonPanel
                    personId={selectedPersonId}
                    location={selectedLocation}
                    onPersonSelect={handlePersonSelect}
                    onClose={handleClearProfile}
                />
            </div>

            {/* Mobile floating button to open panel when no person selected */}
            <button
                className="mobile-panel-toggle"
                onClick={() => setIsPanelOpen(!isPanelOpen)}
                aria-label={isPanelOpen ? "Close panel" : "Open panel"}
            >
                {isPanelOpen ? '✕' : '☰'}
            </button>
        </div>
    );
}

export default function Home() {
    return (
        <BrowserOnly fallback={<div style={{ padding: 20 }}>Loading map...</div>}>
            {() => <HomeContent />}
        </BrowserOnly>
    );
}
