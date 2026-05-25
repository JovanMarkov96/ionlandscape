import React, { useEffect, useState, useMemo } from 'react';
import Layout from '@theme/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';

const TYPE_COLORS = { person: '#3578e5', company: '#00a65a', institution: '#f39c12' };
const LINEAGE_TYPES = new Set(['advisor', 'postdoc_advisor']);
const AFFILIATION_TYPES = new Set(['affiliated_with', 'founder', 'leadership', 'spun_out_from']);

function LineageGraph() {
    const [raw, setRaw] = useState({ nodes: [], links: [] });
    const [loading, setLoading] = useState(true);
    const [showLineage, setShowLineage] = useState(true);
    const [showAffiliation, setShowAffiliation] = useState(true);
    const [hideIsolated, setHideIsolated] = useState(true);
    const [dark, setDark] = useState(false);

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
                    fetch('/ionlandscape/data/people.json').then(r => r.ok ? r.json() : fetch('/data/people.json').then(r => r.json())),
                    fetch('/ionlandscape/data/companies.json').then(r => r.ok ? r.json() : fetch('/data/companies.json').then(r => r.json())),
                    fetch('/ionlandscape/data/institutions.json').then(r => r.ok ? r.json() : fetch('/data/institutions.json').then(r => r.json())),
                    fetch('/ionlandscape/data/edges.json').then(r => r.ok ? r.json() : fetch('/data/edges.json').then(r => r.json()))
                ]);

                const nodes = [];
                const validIds = new Set();
                pRes.forEach(p => { nodes.push({ id: p.id, name: p.name, kind: 'person', val: 1.5, color: TYPE_COLORS.person }); validIds.add(p.id); });
                cRes.forEach(c => { nodes.push({ id: c.id, name: c.name, kind: 'company', val: 5, color: TYPE_COLORS.company }); validIds.add(c.id); });
                iRes.forEach(i => { nodes.push({ id: i.id, name: i.name, kind: 'institution', val: 6, color: TYPE_COLORS.institution }); validIds.add(i.id); });

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
            links.forEach(l => {
                connected.add(typeof l.source === 'object' ? l.source.id : l.source);
                connected.add(typeof l.target === 'object' ? l.target.id : l.target);
            });
            nodes = raw.nodes.filter(n => connected.has(n.id));
        }
        return { nodes, links };
    }, [raw, showLineage, showAffiliation, hideIsolated]);

    const handleNodeClick = (node) => {
        const base = '/ionlandscape/';
        if (node.kind === 'person') window.location.href = `${base}?person=${node.id}`;
        else if (node.kind === 'company') window.location.href = `${base}?company=${node.id}`;
        else if (node.kind === 'institution') window.location.href = `${base}?institution=${node.id}`;
    };

    if (loading) return <div style={{ padding: '50px', textAlign: 'center' }}>Loading Graph Data...</div>;

    const labelColor = dark ? 'rgba(225,228,240,0.95)' : 'rgba(60,60,70,0.95)';
    const labelHalo = dark ? 'rgba(10,12,20,0.85)' : 'rgba(255,255,255,0.85)';

    const Panel = () => (
        <div className="graph-legend-panel">
            <h2>Lineage &amp; Affiliation Graph</h2>
            <div className="graph-legend-dots">
                {Object.entries({ People: TYPE_COLORS.person, Companies: TYPE_COLORS.company, Institutions: TYPE_COLORS.institution }).map(([label, color]) => (
                    <span key={label}>
                        <span className="graph-dot" style={{ background: color }} /> {label}
                    </span>
                ))}
            </div>
            <div className="graph-legend-filters">
                <label><input type="checkbox" checked={showLineage} onChange={e => setShowLineage(e.target.checked)} /> Lineage (advisor)</label>
                <label><input type="checkbox" checked={showAffiliation} onChange={e => setShowAffiliation(e.target.checked)} /> Affiliation / founding</label>
                <label><input type="checkbox" checked={hideIsolated} onChange={e => setHideIsolated(e.target.checked)} /> Hide unconnected</label>
            </div>
            <small>{graphData.nodes.length} nodes · {graphData.links.length} connections · click a node to open its profile</small>
        </div>
    );

    return (
        <BrowserOnly fallback={<div>Loading Graph...</div>}>
            {() => {
                const ForceGraph2D = require('react-force-graph-2d').default;
                return (
                    <div style={{ width: '100vw', height: 'calc(100vh - 60px)', position: 'relative' }}>
                        <Panel />
                        <ForceGraph2D
                            graphData={graphData}
                            backgroundColor={dark ? '#0d1018' : '#ffffff'}
                            nodeLabel="name"
                            nodeVal="val"
                            nodeColor={n => n.color}
                            onNodeClick={handleNodeClick}
                            linkDirectionalArrowLength={3.5}
                            linkDirectionalArrowRelPos={1}
                            linkCurvature={0.15}
                            linkColor={() => dark ? 'rgba(150,160,190,0.35)' : 'rgba(120,120,140,0.4)'}
                            linkLabel="name"
                            nodeCanvasObject={(node, ctx, globalScale) => {
                                const r = Math.sqrt(node.val) * 1.8;
                                ctx.beginPath();
                                ctx.arc(node.x, node.y, r, 0, 2 * Math.PI);
                                ctx.fillStyle = node.color;
                                ctx.fill();
                                if (globalScale > 1.4 || node.kind !== 'person') {
                                    const label = node.name;
                                    const fontSize = Math.max(3, 11 / globalScale);
                                    ctx.font = `${fontSize}px Sans-Serif`;
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'top';
                                    ctx.lineWidth = 3 / globalScale;
                                    ctx.strokeStyle = labelHalo;
                                    ctx.strokeText(label, node.x, node.y + r + 1);
                                    ctx.fillStyle = labelColor;
                                    ctx.fillText(label, node.x, node.y + r + 1);
                                }
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
