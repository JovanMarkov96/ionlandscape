import React, { useState, useEffect, useRef } from 'react';
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
    const [selectedInstitutionId, setSelectedInstitutionId] = useState(null);
    const [selectedLocation, setSelectedLocation] = useState(null);
    const [isPanelOpen, setIsPanelOpen] = useState(false);
    const [showWelcome, setShowWelcome] = useState(false);

    // These components require browser APIs
    const MapPanel = require('../components/MapPanel').default;
    const PersonPanel = require('../components/PersonPanel').default;
    const CompanyPanel = require('../components/CompanyPanel').default;
    const InstitutionPanel = require('../components/InstitutionPanel').default;

    // Check for profile query params in URL
    useEffect(() => {
        const searchParams = new URLSearchParams(window.location.search);
        const personId = searchParams.get('person');
        const companyId = searchParams.get('company');
        const institutionId = searchParams.get('institution');
        if (personId) {
            setSelectedPersonId(personId);
            setIsPanelOpen(true);

            // Clean URL without reloading
            const newUrl = window.location.pathname;
            window.history.replaceState({}, '', newUrl);
        } else if (companyId) {
            setSelectedCompanyId(companyId);
            setIsPanelOpen(true);

            const newUrl = window.location.pathname;
            window.history.replaceState({}, '', newUrl);
        } else if (institutionId) {
            setSelectedInstitutionId(institutionId);
            setIsPanelOpen(true);

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
        setSelectedInstitutionId(null);
        setIsPanelOpen(true); // Open panel when person selected
        setShowWelcome(false);
    };

    const handleCompanySelect = (id) => {
        setSelectedCompanyId(id);
        setSelectedPersonId(null);
        setSelectedInstitutionId(null);
        setIsPanelOpen(true);
        setShowWelcome(false);
    };

    const handleInstitutionSelect = (id) => {
        setSelectedInstitutionId(id);
        setSelectedPersonId(null);
        setSelectedCompanyId(null);
        setIsPanelOpen(true);
        setShowWelcome(false);
    };

    const handleLocationSelect = (loc) => {
        setSelectedLocation(loc);
        setSelectedPersonId(null);
        setSelectedCompanyId(null);
        setSelectedInstitutionId(null);
        setIsPanelOpen(true);
        setShowWelcome(false);
    };

    const handleClosePanel = () => {
        setIsPanelOpen(false);
    };

    const handleClearProfile = () => {
        setSelectedPersonId(null);
        setSelectedCompanyId(null);
        setSelectedInstitutionId(null);
        setSelectedLocation(null);
        setIsPanelOpen(false);
    };

    const mapPanelRef = useRef(null);

    /**
     * Flies the map to the given coordinates and optionally closes the panel.
     * Used by the "Show in Map" button in profile panels.
     * @param {number} lat
     * @param {number} lon
     */
    const handleShowInMap = (lat, lon) => {
        if (mapPanelRef.current) {
            mapPanelRef.current.flyTo(lat, lon, 10);
        }
        setIsPanelOpen(false);
    };

    const handleDismissWelcome = () => {
        setShowWelcome(false);
        localStorage.setItem('hasSeenIonWelcome', 'true');
    };

    return (
        <div className="quantum-landscape-container">
            <div className="quantum-landscape-map">
                <MapPanel
                    ref={mapPanelRef}
                    onPersonSelect={handlePersonSelect}
                    onCompanySelect={handleCompanySelect}
                    onInstitutionSelect={handleInstitutionSelect}
                    onLocationSelect={handleLocationSelect}
                />
            </div>

            {showWelcome && !isPanelOpen && (
                <div className="welcome-popup">
                    <button className="close-panel-btn" onClick={handleDismissWelcome} aria-label="Dismiss welcome popup" style={{ top: '16px', right: '16px' }}>✕</button>
                    <div className="welcome-brand">
                        <img className="ql-stacked ql-stacked-dark" src="/quantum-landscape/img/brand/wordmark-stacked-on-dark.png" alt="Quantum Landscape" />
                        <img className="ql-stacked ql-stacked-light" src="/quantum-landscape/img/brand/wordmark-stacked-on-light.png" alt="Quantum Landscape" />
                    </div>
                    <p>An interactive map and academic family tree of the quantum technology landscape. Click a marker to explore a researcher, company, or institution.</p>
                    <button className="btn-primary" onClick={handleDismissWelcome}>Get Started</button>
                </div>
            )}

            <div className={`quantum-landscape-panel ${isPanelOpen ? 'panel-open' : ''}`}>
                <button
                    className="back-to-map-btn"
                    onClick={handleClosePanel}
                >
                    ← Back to Map
                </button>
                {selectedInstitutionId ? (
                    <InstitutionPanel
                        institutionId={selectedInstitutionId}
                        onPersonSelect={handlePersonSelect}
                        onClose={handleClearProfile}
                        onShowInMap={handleShowInMap}
                    />
                ) : selectedCompanyId ? (
                    <CompanyPanel
                        companyId={selectedCompanyId}
                        location={selectedLocation}
                        onCompanySelect={handleCompanySelect}
                        onInstitutionSelect={handleInstitutionSelect}
                        onPersonSelect={handlePersonSelect}
                        onClose={handleClearProfile}
                        onShowInMap={handleShowInMap}
                    />
                ) : (
                    <PersonPanel
                        personId={selectedPersonId}
                        location={selectedLocation}
                        onPersonSelect={handlePersonSelect}
                        onCompanySelect={handleCompanySelect}
                        onInstitutionSelect={handleInstitutionSelect}
                        onClose={handleClearProfile}
                        onShowInMap={handleShowInMap}
                    />
                )}
            </div>
        </div>
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
        <Layout
            title="Map"
            description="Interactive map of quantum computing groups"
            noFooter={false}
        >
            <BrowserOnly fallback={<div style={{ padding: 20 }}>Loading map...</div>}>
                {() => <HomeContent />}
            </BrowserOnly>
        </Layout>
    );
}
