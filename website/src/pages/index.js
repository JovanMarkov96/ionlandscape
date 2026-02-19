import React, { useState, useEffect } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';


function HomeContent() {
    const [selectedPersonId, setSelectedPersonId] = useState(null);
    const [selectedCompanyId, setSelectedCompanyId] = useState(null);
    const [selectedLocation, setSelectedLocation] = useState(null);
    const [isPanelOpen, setIsPanelOpen] = useState(false);

    // These components require browser APIs
    const MapPanel = require('../components/MapPanel').default;
    const PersonPanel = require('../components/PersonPanel').default;
    const CompanyPanel = require('../components/CompanyPanel').default;

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
        setSelectedCompanyId(null);
        setIsPanelOpen(true); // Open panel when person selected
    };

    const handleCompanySelect = (id) => {
        setSelectedCompanyId(id);
        setSelectedPersonId(null);
        setIsPanelOpen(true);
    };

    const handleClosePanel = () => {
        setIsPanelOpen(false);
    };

    const handleClearProfile = () => {
        setSelectedPersonId(null);
        setSelectedCompanyId(null);
        setSelectedLocation(null);
    };

    return (
        <Layout
            title="Map"
            description="Interactive map of ion trap and neutral atom quantum computing groups"
            noFooter={false}
        >
            <div className="ion-landscape-container">
                <div className="ion-landscape-map">
                    <MapPanel
                        onPersonSelect={handlePersonSelect}
                        onCompanySelect={handleCompanySelect}
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
                    {selectedCompanyId ? (
                        <CompanyPanel
                            companyId={selectedCompanyId}
                            location={selectedLocation}
                            onCompanySelect={handleCompanySelect}
                            onPersonSelect={handlePersonSelect}
                            onClose={handleClearProfile}
                        />
                    ) : (
                        <PersonPanel
                            personId={selectedPersonId}
                            location={selectedLocation}
                            onPersonSelect={handlePersonSelect}
                            onCompanySelect={handleCompanySelect}
                            onClose={handleClearProfile}
                        />
                    )}
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
        </Layout>
    );
}

export default function Home() {
    return (
        <BrowserOnly fallback={<div style={{ padding: 20 }}>Loading map...</div>}>
            {() => <HomeContent />}
        </BrowserOnly>
    );
}
