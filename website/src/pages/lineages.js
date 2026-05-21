import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';

function LineageGraph() {
    const [graphData, setGraphData] = useState({ nodes: [], links: [] });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
            try {
                // Fetch nodes
                const [pRes, cRes, iRes, eRes] = await Promise.all([
                    fetch('/ionlandscape/data/people.json').then(r => r.ok ? r.json() : fetch('/data/people.json').then(r => r.json())),
                    fetch('/ionlandscape/data/companies.json').then(r => r.ok ? r.json() : fetch('/data/companies.json').then(r => r.json())),
                    fetch('/ionlandscape/data/institutions.json').then(r => r.ok ? r.json() : fetch('/data/institutions.json').then(r => r.json())),
                    fetch('/ionlandscape/data/edges.json').then(r => r.ok ? r.json() : fetch('/data/edges.json').then(r => r.json()))
                ]);

                const nodes = [];
                const validIds = new Set();
                
                // Colors based on entity type
                pRes.forEach(p => { nodes.push({ id: p.id, name: p.name, val: 1.5, color: '#3578e5' }); validIds.add(p.id); });
                cRes.forEach(c => { nodes.push({ id: c.id, name: c.name, val: 3, color: '#00a65a' }); validIds.add(c.id); });
                iRes.forEach(i => { nodes.push({ id: i.id, name: i.name, val: 4, color: '#f39c12' }); validIds.add(i.id); });

                // Links
                const links = [];
                eRes.forEach(e => {
                    if (validIds.has(e.source) && validIds.has(e.target)) {
                        links.push({ source: e.source, target: e.target, name: e.type, color: '#999' });
                    }
                });

                setGraphData({ nodes, links });
                setLoading(false);
            } catch (err) {
                console.error("Error loading graph data:", err);
                setLoading(false);
            }
        };
        loadData();
    }, []);

    if (loading) return <div style={{padding: '50px', textAlign: 'center'}}>Loading Graph Data...</div>;

    return (
        <BrowserOnly fallback={<div>Loading Graph...</div>}>
            {() => {
                const ForceGraph2D = require('react-force-graph-2d').default;
                return (
                    <div style={{ width: '100vw', height: 'calc(100vh - 60px)', display: 'flex', flexDirection: 'column' }}>
                        <div style={{ padding: '10px 20px', background: '#f8f9fa', borderBottom: '1px solid #ddd' }}>
                            <h2 style={{ margin: 0, fontSize: '1.2rem' }}>Lineage & Affiliation Graph</h2>
                            <small>Nodes: Blue (People), Green (Companies), Orange (Institutions). Edges: Founders, Advisors, Affiliations.</small>
                        </div>
                        <div style={{ flex: 1, position: 'relative' }}>
                            <ForceGraph2D
                                graphData={graphData}
                                nodeLabel="name"
                                nodeAutoColorBy="color"
                                linkDirectionalArrowLength={3.5}
                                linkDirectionalArrowRelPos={1}
                                linkCurvature={0.25}
                                linkLabel="name"
                                nodeCanvasObject={(node, ctx, globalScale) => {
                                    const label = node.name;
                                    const fontSize = 12/globalScale;
                                    ctx.font = `${fontSize}px Sans-Serif`;
                                    const textWidth = ctx.measureText(label).width;
                                    const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); 

                                    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
                                    ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);

                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'middle';
                                    ctx.fillStyle = node.color;
                                    ctx.fillText(label, node.x, node.y);

                                    node.__bckgDimensions = bckgDimensions; 
                                }}
                                nodePointerAreaPaint={(node, color, ctx) => {
                                    ctx.fillStyle = color;
                                    const bckgDimensions = node.__bckgDimensions;
                                    bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
                                }}
                            />
                        </div>
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
