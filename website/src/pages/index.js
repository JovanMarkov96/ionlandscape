import React, { useState, useEffect } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';

/**
 * Private inner component that handles map state and side panels 
 * when the map view is active. Must be rendered client-side 
 * because it interacts with `window` and `localStorage`.
 * 
 * Manages the layout state, welcome modal, and floating profile panels.
 * 
 * @returns {JSX.Element} The rendered map content layout
 */
function HomeContent() {
    const [selectedPersonId, setSelectedPersonId] = useState(null);
    const [selectedCompanyId, setSelectedCompanyId] = useState(null);
    const [selectedLocation, setSelectedLocation] = useState(null);
    const [isPanelOpen, setIsPanelOpen] = useState(false);
    const [showWelcome, setShowWelcome] = useState(false);

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
        } else {
            const hasSeenWelcome = localStorage.getItem('hasSeenIonWelcome');
            if (!hasSeenWelcome) {
                setShowWelcome(true);
            }
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
        setShowWelcome(false);
    };

    const handleCompanySelect = (id) => {
        setSelectedCompanyId(id);
        setSelectedPersonId(null);
        setIsPanelOpen(true);
        setShowWelcome(false);
    };

    const handleLocationSelect = (loc) => {
        setSelectedLocation(loc);
        setSelectedPersonId(null);
        setSelectedCompanyId(null);
        setIsPanelOpen(true);
        setShowWelcome(false);
    };

    const handleClosePanel = () => {
        setIsPanelOpen(false);
    };

    const handleClearProfile = () => {
        setSelectedPersonId(null);
        setSelectedCompanyId(null);
        setSelectedLocation(null);
        setIsPanelOpen(false);
    };

    const handleDismissWelcome = () => {
        setShowWelcome(false);
        localStorage.setItem('hasSeenIonWelcome', 'true');
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
                        onLocationSelect={handleLocationSelect}
                    />
                </div>

                {showWelcome && !isPanelOpen && (
                    <div className="welcome-popup">
                        <button className="close-panel-btn" onClick={handleDismissWelcome} aria-label="Dismiss welcome popup" style={{ top: '16px', right: '16px' }}>✕</button>
                        <h2>Ion Landscape</h2>
                        <p>Click a marker on the map to view a personal or company profile.</p>
                        <button className="btn-primary" onClick={handleDismissWelcome}>Get Started</button>
                    </div>
                )}

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
            </div>
        </Layout>
    );
}

/**
 * Main Entry Page (`/`)
 * 
 * Renders the map application inside a generic Docusaurus Layout.
 * We wrap `HomeContent` in `BrowserOnly` because the MapLibre engine 
 * cannot be initialized during static server-side rendering (SSR).
 * 
 * @returns {JSX.Element} The page layout
 */
export default function Home() {
    return (
        <BrowserOnly fallback={<div style={{ padding: 20 }}>Loading map...</div>}>
            {() => <HomeContent />}
        </BrowserOnly>
    );
}
