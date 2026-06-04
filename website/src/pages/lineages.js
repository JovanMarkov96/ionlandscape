import React, { useEffect, useState, useMemo, useRef } from 'react';
import Layout from '@theme/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';
import GuidedTour from '../components/GuidedTour';

const GRAPH_TOUR_KEY = 'ql_tour_graph_v1';
const GRAPH_TOUR = [
    {
        selector: null,
        brand: true,
        title: 'The connection graph',
        body: 'Every dot is a person, company or institution; links show advising relationships and affiliations. Here’s a quick tour of how to explore it.',
        placement: 'center',
        cta: 'Start',
    },
    {
        selector: '.graph-search',
        anchor: '.graph-panel',
        title: 'Search',
        body: 'Find any person, company or institution by name and jump straight to it on the graph.',
        placement: 'right',
    },
    {
        selector: '.graph-legend-filters',
        anchor: '.graph-panel',
        title: 'Filters',
        body: 'Show or hide lineage (advisor) vs. affiliation/founding links, and hide unconnected nodes to declutter the view.',
        placement: 'right',
    },
    {
        selector: null,
        title: 'Click to explore',
        body: 'Click any node to open its profile card — it lights up everything connected to it and lists each relationship. Click a connection to keep walking the graph, or use “Open in map” to see it geographically.',
        placement: 'center',
        cta: 'Done',
    },
];

const TYPE_COLORS = { person: '#3578e5', company: '#00a65a', institution: '#f39c12' };
const KIND_LABEL = { person: 'Person', company: 'Company', institution: 'Institution' };
const LINEAGE_TYPES = new Set(['advisor', 'postdoc_advisor']);
const AFFILIATION_TYPES = new Set(['affiliated_with', 'founder', 'leadership', 'spun_out_from']);

// How an edge reads relative to the node currently selected in the card.
function relationLabel(type, selectedIsSource) {
    switch (type) {
        case 'advisor': return selectedIsSource ? 'Doctoral advisee' : 'Doctoral advisor';
        case 'postdoc_advisor': return selectedIsSource ? 'Postdoc (mentored)' : 'Postdoc advisor';
        case 'affiliated_with': return selectedIsSource ? 'Affiliated with' : 'Affiliated researcher';
        case 'founder': return selectedIsSource ? 'Founder of' : 'Founded by';
        case 'leadership': return selectedIsSource ? 'Leadership at' : 'Leadership';
        case 'spun_out_from': return selectedIsSource ? 'Spun out from' : 'Spinout';
        default: return type.replace(/_/g, ' ');
    }
}

const idOf = (x) => (typeof x === 'object' && x !== null ? x.id : x);

// One-line summary shown under the name in the card.
function summaryLine(node) {
    const d = node.data || {};
    if (node.kind === 'person') {
        const pos = d.current_position || {};
        const bits = [pos.title, pos.institution].filter(Boolean);
        return bits.join(' · ');
    }
    if (node.kind === 'company') {
        const loc = d.location || {};
        const place = [loc.city, loc.country].filter(Boolean).join(', ');
        return [d.entity_type === 'company' ? 'Company' : d.entity_type, place].filter(Boolean).join(' · ');
    }
    if (node.kind === 'institution') {
        const loc = d.location || {};
        const place = [loc.city, loc.country].filter(Boolean).join(', ');
        return [d.institution_type, place].filter(Boolean).join(' · ');
    }
    return '';
}

function platformsOf(node) {
    const d = node.data || {};
    return d.platforms || d.platforms_represented || [];
}

function LineageGraph() {
    const [raw, setRaw] = useState({ nodes: [], links: [] });
    const [loading, setLoading] = useState(true);
    const [showLineage, setShowLineage] = useState(true);
    const [showAffiliation, setShowAffiliation] = useState(true);
    const [hideIsolated, setHideIsolated] = useState(true);
    const [dark, setDark] = useState(false);
    const [selectedId, setSelectedId] = useState(null);
    const [query, setQuery] = useState('');
    const [showTour, setShowTour] = useState(false);
    const fgRef = useRef(null);

    // First-visit guided tour for the graph view
    useEffect(() => {
        try { if (!localStorage.getItem(GRAPH_TOUR_KEY)) setShowTour(true); } catch (e) { }
    }, []);
    const closeTour = () => {
        setShowTour(false);
        try { localStorage.setItem(GRAPH_TOUR_KEY, '1'); } catch (e) { }
    };

    // Track Docusaurus light/dark theme so the canvas + labels adapt
    useEffect(() => {
        const read = () => setDark(document.documentElement.getAttribute('data-theme') === 'dark');
        read();
        const obs = new MutationObserver(read);
        obs.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
        return () => obs.disconnect();
    }, []);

    useEffect(() => {
        const loadData = async () => {
            try {
                const [pRes, cRes, iRes, eRes] = await Promise.all([
                    fetch('/quantum-landscape/data/people.json').then(r => r.ok ? r.json() : fetch('/data/people.json').then(r => r.json())),
                    fetch('/quantum-landscape/data/companies.json').then(r => r.ok ? r.json() : fetch('/data/companies.json').then(r => r.json())),
                    fetch('/quantum-landscape/data/institutions.json').then(r => r.ok ? r.json() : fetch('/data/institutions.json').then(r => r.json())),
                    fetch('/quantum-landscape/data/edges.json').then(r => r.ok ? r.json() : fetch('/data/edges.json').then(r => r.json()))
                ]);

                const nodes = [];
                const validIds = new Set();
                pRes.forEach(p => { nodes.push({ id: p.id, name: p.name, kind: 'person', val: 1.5, color: TYPE_COLORS.person, data: p }); validIds.add(p.id); });
                cRes.forEach(c => { nodes.push({ id: c.id, name: c.name, kind: 'company', val: 5, color: TYPE_COLORS.company, data: c }); validIds.add(c.id); });
                iRes.forEach(i => { nodes.push({ id: i.id, name: i.name, kind: 'institution', val: 6, color: TYPE_COLORS.institution, data: i }); validIds.add(i.id); });

                const links = [];
                eRes.forEach(e => {
                    if (validIds.has(e.source) && validIds.has(e.target)) {
                        links.push({ source: e.source, target: e.target, type: e.type, name: e.type.replace(/_/g, ' ') });
                    }
                });

                setRaw({ nodes, links });
                setLoading(false);
            } catch (err) {
                console.error("Error loading graph data:", err);
                setLoading(false);
            }
        };
        loadData();
    }, []);

    // Fast lookups: id -> node, and full adjacency (independent of visual filters)
    const nodeById = useMemo(() => {
        const m = new Map();
        raw.nodes.forEach(n => m.set(n.id, n));
        return m;
    }, [raw.nodes]);

    const adjacency = useMemo(() => {
        const m = new Map();
        raw.links.forEach(l => {
            const sid = idOf(l.source), tid = idOf(l.target);
            if (!m.has(sid)) m.set(sid, []);
            if (!m.has(tid)) m.set(tid, []);
            m.get(sid).push({ otherId: tid, type: l.type, selectedIsSource: true });
            m.get(tid).push({ otherId: sid, type: l.type, selectedIsSource: false });
        });
        return m;
    }, [raw.links]);

    // Apply edge-type filters and isolated-node hiding
    const graphData = useMemo(() => {
        const links = raw.links.filter(l => {
            if (LINEAGE_TYPES.has(l.type) && !showLineage) return false;
            if (AFFILIATION_TYPES.has(l.type) && !showAffiliation) return false;
            return true;
        });
        let nodes = raw.nodes;
        if (hideIsolated) {
            const connected = new Set();
            links.forEach(l => { connected.add(idOf(l.source)); connected.add(idOf(l.target)); });
            nodes = raw.nodes.filter(n => connected.has(n.id));
        }
        return { nodes, links };
    }, [raw, showLineage, showAffiliation, hideIsolated]);

    // Neighbours of the selected node (for highlighting + the card's connection list)
    const selected = selectedId ? nodeById.get(selectedId) : null;
    const connections = useMemo(() => {
        if (!selectedId) return null;
        const seen = new Map(); // otherId|type -> entry (dedupe advisor+postdoc kept separate by type)
        (adjacency.get(selectedId) || []).forEach(({ otherId, type, selectedIsSource }) => {
            const other = nodeById.get(otherId);
            if (!other) return;
            const key = `${otherId}|${type}|${selectedIsSource}`;
            if (seen.has(key)) return;
            seen.set(key, { other, label: relationLabel(type, selectedIsSource) });
        });
        const groups = { person: [], company: [], institution: [] };
        seen.forEach(({ other, label }) => { groups[other.kind].push({ other, label }); });
        Object.values(groups).forEach(arr => arr.sort((a, b) => a.other.name.localeCompare(b.other.name)));
        return groups;
    }, [selectedId, adjacency, nodeById]);

    const neighborIds = useMemo(() => {
        const s = new Set();
        if (selectedId) (adjacency.get(selectedId) || []).forEach(({ otherId }) => s.add(otherId));
        return s;
    }, [selectedId, adjacency]);

    const selectNode = (node, recenter = false) => {
        if (!node) return;
        setSelectedId(node.id);
        if (recenter && fgRef.current && typeof node.x === 'number') {
            fgRef.current.centerAt(node.x, node.y, 600);
            fgRef.current.zoom(2.6, 600);
        }
    };

    const openInMap = (node) => {
        const base = '/quantum-landscape/';
        if (node.kind === 'person') window.location.href = `${base}?person=${node.id}`;
        else if (node.kind === 'company') window.location.href = `${base}?company=${node.id}`;
        else if (node.kind === 'institution') window.location.href = `${base}?institution=${node.id}`;
    };

    // Search matches (by name), capped
    const matches = useMemo(() => {
        const q = query.trim().toLowerCase();
        if (q.length < 2) return [];
        return raw.nodes.filter(n => n.name.toLowerCase().includes(q)).slice(0, 8);
    }, [query, raw.nodes]);

    if (loading) return <div style={{ padding: '50px', textAlign: 'center' }}>Loading Graph Data...</div>;

    const labelColor = dark ? 'rgba(255,255,255,0.95)' : 'rgba(60,60,70,0.95)';
    const labelHalo = dark ? 'rgba(10,12,20,0.85)' : 'rgba(255,255,255,0.85)';
    const ringColor = dark ? '#ffffff' : '#1c1e26';

    return (
        <BrowserOnly fallback={<div>Loading Graph...</div>}>
            {() => {
                const ForceGraph2D = require('react-force-graph-2d').default;
                return (
                    <div style={{ width: '100vw', height: 'calc(100vh - 60px)', position: 'relative' }}>
                        <GuidedTour open={showTour} steps={GRAPH_TOUR} onClose={closeTour} />
                        {!showTour && (
                            <button className="tour-help-btn" onClick={() => setShowTour(true)} title="Take the tour" aria-label="Take the guided tour">?</button>
                        )}
                        {/* ---- Left control panel ---- */}
                        <div className="graph-panel">
                            <div className="graph-panel-head">
                                <h2>Lineage &amp; Affiliation Graph</h2>
                                <p>Explore who trained whom, and how people connect to companies and institutions.</p>
                            </div>

                            <div className="graph-panel-section">
                                <label className="graph-field-label" htmlFor="graph-search">Search</label>
                                <div className="graph-search">
                                    <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" /></svg>
                                    <input
                                        id="graph-search"
                                        type="text"
                                        placeholder="Find a person, company, institution…"
                                        value={query}
                                        onChange={e => setQuery(e.target.value)}
                                        autoComplete="off"
                                    />
                                    {query && <button className="graph-search-clear" aria-label="Clear search" onClick={() => setQuery('')}>×</button>}
                                </div>
                                {matches.length > 0 && (
                                    <ul className="graph-search-results">
                                        {matches.map(n => (
                                            <li key={n.id}>
                                                <button onClick={() => { selectNode(n, true); setQuery(''); }}>
                                                    <span className="graph-dot" style={{ background: n.color }} />
                                                    <span className="graph-search-name">{n.name}</span>
                                                    <span className="graph-search-kind">{KIND_LABEL[n.kind]}</span>
                                                </button>
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </div>

                            <div className="graph-panel-section">
                                <span className="graph-field-label">Legend</span>
                                <div className="graph-legend-dots">
                                    {Object.entries({ People: TYPE_COLORS.person, Companies: TYPE_COLORS.company, Institutions: TYPE_COLORS.institution }).map(([label, color]) => (
                                        <span key={label}><span className="graph-dot" style={{ background: color }} /> {label}</span>
                                    ))}
                                </div>
                            </div>

                            <div className="graph-panel-section">
                                <span className="graph-field-label">Filters</span>
                                <div className="graph-legend-filters">
                                    <label><input type="checkbox" checked={showLineage} onChange={e => setShowLineage(e.target.checked)} /> Lineage (advisor)</label>
                                    <label><input type="checkbox" checked={showAffiliation} onChange={e => setShowAffiliation(e.target.checked)} /> Affiliation / founding</label>
                                    <label><input type="checkbox" checked={hideIsolated} onChange={e => setHideIsolated(e.target.checked)} /> Hide unconnected</label>
                                </div>
                            </div>

                            <small className="graph-panel-stats">{graphData.nodes.length} nodes · {graphData.links.length} connections · click a node to explore</small>
                        </div>

                        {/* ---- Floating profile / connections card ---- */}
                        {selected && connections && (
                            <div className="graph-card">
                                <button className="graph-card-close" aria-label="Close" onClick={() => setSelectedId(null)}>×</button>
                                <div className="graph-card-head">
                                    <span className="graph-card-kind" style={{ background: selected.color }}>{KIND_LABEL[selected.kind]}</span>
                                    <h3>{selected.name}</h3>
                                    {summaryLine(selected) && <p className="graph-card-sub">{summaryLine(selected)}</p>}
                                    {platformsOf(selected).length > 0 && (
                                        <div className="graph-card-tags">
                                            {platformsOf(selected).map(p => <span key={p} className="graph-card-tag">{p.replace(/_/g, ' ')}</span>)}
                                        </div>
                                    )}
                                </div>

                                <div className="graph-card-body">
                                    {[['person', 'People'], ['company', 'Companies'], ['institution', 'Institutions']].map(([kind, heading]) => (
                                        connections[kind].length > 0 && (
                                            <div className="graph-card-group" key={kind}>
                                                <div className="graph-card-group-title">
                                                    <span className="graph-dot" style={{ background: TYPE_COLORS[kind] }} />
                                                    {heading} <span className="graph-card-count">{connections[kind].length}</span>
                                                </div>
                                                <ul className="graph-card-conns">
                                                    {connections[kind].map(({ other, label }, i) => (
                                                        <li key={other.id + label + i}>
                                                            <button className="graph-conn-btn" onClick={() => selectNode(other, true)}>
                                                                <span className="graph-conn-name">{other.name}</span>
                                                                <span className="graph-conn-rel">{label}</span>
                                                            </button>
                                                        </li>
                                                    ))}
                                                </ul>
                                            </div>
                                        )
                                    ))}
                                    {connections.person.length === 0 && connections.company.length === 0 && connections.institution.length === 0 && (
                                        <p className="graph-card-empty">No recorded connections yet.</p>
                                    )}
                                </div>

                                <button className="graph-card-map-btn" onClick={() => openInMap(selected)}>
                                    <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6" /><line x1="8" y1="2" x2="8" y2="18" /><line x1="16" y1="6" x2="16" y2="22" /></svg>
                                    Open in map
                                </button>
                            </div>
                        )}

                        <ForceGraph2D
                            ref={fgRef}
                            graphData={graphData}
                            backgroundColor={dark ? '#0d1018' : '#ffffff'}
                            nodeLabel="name"
                            nodeVal="val"
                            nodeColor={n => n.color}
                            onNodeClick={node => selectNode(node)}
                            onBackgroundClick={() => setSelectedId(null)}
                            linkDirectionalArrowLength={3.5}
                            linkDirectionalArrowRelPos={1}
                            linkCurvature={0.15}
                            linkWidth={l => {
                                if (!selectedId) return 1;
                                return (idOf(l.source) === selectedId || idOf(l.target) === selectedId) ? 2.5 : 1;
                            }}
                            linkColor={l => {
                                if (!selectedId) return dark ? 'rgba(150,160,190,0.35)' : 'rgba(120,120,140,0.4)';
                                const on = idOf(l.source) === selectedId || idOf(l.target) === selectedId;
                                if (on) return dark ? 'rgba(120,170,255,0.9)' : 'rgba(53,120,229,0.85)';
                                return dark ? 'rgba(150,160,190,0.06)' : 'rgba(120,120,140,0.07)';
                            }}
                            linkLabel="name"
                            nodeCanvasObject={(node, ctx, globalScale) => {
                                const r = Math.sqrt(node.val) * 1.8;
                                const isSel = node.id === selectedId;
                                const isNeighbor = neighborIds.has(node.id);
                                const dim = selectedId && !isSel && !isNeighbor;
                                ctx.save();
                                if (dim) ctx.globalAlpha = 0.13;
                                ctx.beginPath();
                                ctx.arc(node.x, node.y, r, 0, 2 * Math.PI);
                                ctx.fillStyle = node.color;
                                ctx.fill();
                                if (isSel) {
                                    ctx.lineWidth = 2.5 / globalScale;
                                    ctx.strokeStyle = ringColor;
                                    ctx.stroke();
                                }
                                if (isSel || isNeighbor || globalScale > 1.4 || node.kind !== 'person') {
                                    const label = node.name;
                                    const fontSize = Math.max(3, (isSel ? 13 : 11) / globalScale);
                                    ctx.font = `${isSel ? 'bold ' : ''}${fontSize}px Sans-Serif`;
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'top';
                                    ctx.lineWidth = 3 / globalScale;
                                    ctx.strokeStyle = labelHalo;
                                    ctx.strokeText(label, node.x, node.y + r + 1);
                                    ctx.fillStyle = labelColor;
                                    ctx.fillText(label, node.x, node.y + r + 1);
                                }
                                ctx.restore();
                            }}
                            nodePointerAreaPaint={(node, color, ctx) => {
                                const r = Math.sqrt(node.val) * 1.8 + 2;
                                ctx.beginPath();
                                ctx.arc(node.x, node.y, r, 0, 2 * Math.PI);
                                ctx.fillStyle = color;
                                ctx.fill();
                            }}
                        />
                    </div>
                );
            }}
        </BrowserOnly>
    );
}

export default function Lineages() {
    return (
        <Layout title="Lineages" description="Knowledge graph of the quantum ecosystem">
            <LineageGraph />
        </Layout>
    );
}
