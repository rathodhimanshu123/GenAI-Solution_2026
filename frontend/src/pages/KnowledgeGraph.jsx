import { useEffect, useRef, useState, useCallback } from 'react';
import { getGraph } from '../api';
import * as d3 from 'd3';
import { Loader2, Info, Network } from 'lucide-react';
import './KnowledgeGraph.css';

const CATEGORY_COLORS = {
  root: '#f5a623',
  domain: '#a78bfa',
  ayurveda: '#4ade80',
  yoga: '#06b6d4',
  philosophy: '#f472b6',
  arts: '#fb923c',
  math_astro: '#60a5fa',
  text: '#fbbf24',
  sanskrit: '#34d399',
};

export default function KnowledgeGraph() {
  const svgRef = useRef(null);
  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tooltip, setTooltip] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);

  useEffect(() => {
    getGraph()
      .then(data => { setGraphData(data); setLoading(false); })
      .catch(() => { setError('Could not load knowledge graph. Is the backend running?'); setLoading(false); });
  }, []);

  const renderGraph = useCallback(() => {
    if (!graphData || !svgRef.current) return;

    const width = svgRef.current.clientWidth || 900;
    const height = svgRef.current.clientHeight || 600;

    // Clear
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width).attr('height', height);

    // Background pattern
    const defs = svg.append('defs');
    const pattern = defs.append('pattern')
      .attr('id', 'grid').attr('width', 30).attr('height', 30)
      .attr('patternUnits', 'userSpaceOnUse');
    pattern.append('circle').attr('cx', 1).attr('cy', 1).attr('r', 0.8)
      .attr('fill', 'rgba(245,166,35,0.12)');

    svg.append('rect').attr('width', width).attr('height', height)
      .attr('fill', 'url(#grid)');

    const g = svg.append('g');

    // Zoom
    const zoom = d3.zoom()
      .scaleExtent([0.3, 3])
      .on('zoom', (e) => g.attr('transform', e.transform));
    svg.call(zoom);
    svg.call(zoom.transform, d3.zoomIdentity.translate(width / 2, height / 2).scale(0.75));

    // Simulation
    const nodes = graphData.nodes.map(n => ({ ...n }));
    const links = graphData.edges.map(e => ({
      ...e,
      source: e.source,
      target: e.target,
    }));

    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(d => 80 + 120 * (1 - d.strength)).strength(0.7))
      .force('charge', d3.forceManyBody().strength(-400))
      .force('center', d3.forceCenter(0, 0))
      .force('collision', d3.forceCollide().radius(d => d.size + 15));

    // Arrow markers
    defs.selectAll('marker')
      .data(['arrow'])
      .enter().append('marker')
      .attr('id', 'arrow')
      .attr('viewBox', '0 -5 10 10').attr('refX', 22).attr('refY', 0)
      .attr('markerWidth', 6).attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path').attr('d', 'M0,-5L10,0L0,5').attr('fill', 'rgba(245,166,35,0.3)');

    // Links
    const link = g.append('g').selectAll('line')
      .data(links).enter().append('line')
      .attr('stroke', 'rgba(245,166,35,0.2)')
      .attr('stroke-width', d => d.strength * 1.5)
      .attr('marker-end', 'url(#arrow)');

    // Link labels
    const linkLabel = g.append('g').selectAll('text')
      .data(links).enter().append('text')
      .attr('font-size', 8)
      .attr('fill', 'rgba(255,255,255,0.25)')
      .attr('text-anchor', 'middle')
      .text(d => d.label);

    // Node groups
    const node = g.append('g').selectAll('g')
      .data(nodes).enter().append('g')
      .attr('class', 'node-group')
      .style('cursor', 'pointer')
      .call(d3.drag()
        .on('start', (e, d) => { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
        .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y; })
        .on('end', (e, d) => { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }));

    node.on('click', (e, d) => setSelectedNode(d))
        .on('mouseenter', (e, d) => setTooltip({ x: e.clientX, y: e.clientY, node: d }))
        .on('mouseleave', () => setTooltip(null));

    // Glow
    const glowFilter = defs.append('filter').attr('id', 'glow');
    glowFilter.append('feGaussianBlur').attr('stdDeviation', 4).attr('result', 'blur');
    const merge = glowFilter.append('feMerge');
    merge.append('feMergeNode').attr('in', 'blur');
    merge.append('feMergeNode').attr('in', 'SourceGraphic');

    // Circles
    node.append('circle')
      .attr('r', d => d.size)
      .attr('fill', d => CATEGORY_COLORS[d.category] || '#888')
      .attr('fill-opacity', 0.18)
      .attr('stroke', d => CATEGORY_COLORS[d.category] || '#888')
      .attr('stroke-width', 1.5)
      .attr('filter', 'url(#glow)');

    // Emoji/text in center
    node.append('text')
      .attr('text-anchor', 'middle').attr('dominant-baseline', 'central')
      .attr('font-size', d => Math.min(d.size * 0.55, 11))
      .attr('fill', d => CATEGORY_COLORS[d.category] || '#fff')
      .attr('font-weight', '600')
      .text(d => d.label.replace('\n', ' ').substring(0, 10));

    // Label below
    node.append('text')
      .attr('y', d => d.size + 12)
      .attr('text-anchor', 'middle')
      .attr('font-size', d => d.category === 'root' ? 11 : 9)
      .attr('fill', 'rgba(255,255,255,0.65)')
      .attr('font-family', 'Inter, sans-serif')
      .each(function (d) {
        const parts = d.label.split('\n');
        const el = d3.select(this);
        parts.forEach((p, i) => {
          el.append('tspan').attr('x', 0).attr('dy', i === 0 ? 0 : 12).text(p);
        });
      });

    simulation.on('tick', () => {
      link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
      linkLabel
        .attr('x', d => (d.source.x + d.target.x) / 2)
        .attr('y', d => (d.source.y + d.target.y) / 2);
      node.attr('transform', d => `translate(${d.x},${d.y})`);
    });
  }, [graphData]);

  useEffect(() => { renderGraph(); }, [renderGraph]);
  useEffect(() => {
    const handle = () => renderGraph();
    window.addEventListener('resize', handle);
    return () => window.removeEventListener('resize', handle);
  }, [renderGraph]);

  const categories = Object.entries(CATEGORY_COLORS).filter(([k]) => k !== 'root');

  return (
    <div className="graph-page">
      <div className="graph-header container">
        <div>
          <h2><Network size={22} /> Knowledge Graph</h2>
          <p>Explore connections between Indian knowledge concepts. Drag nodes, scroll to zoom.</p>
        </div>
        <div className="legend">
          {categories.map(([cat, color]) => (
            <span key={cat} className="legend-item">
              <span className="legend-dot" style={{ background: color }} />
              {cat}
            </span>
          ))}
        </div>
      </div>

      <div className="graph-container">
        {loading && <div className="graph-loading"><Loader2 size={32} className="spin" /><span>Loading graph...</span></div>}
        {error && <div className="graph-error"><Info size={16} />{error}</div>}
        {!loading && !error && <svg ref={svgRef} className="graph-svg" />}
      </div>

      {tooltip && (
        <div className="node-tooltip" style={{ left: tooltip.x + 12, top: tooltip.y - 40 }}>
          <strong>{tooltip.node.label.replace('\n', ' ')}</strong>
          <span>{tooltip.node.description}</span>
        </div>
      )}

      {selectedNode && (
        <div className="node-detail card">
          <button className="detail-close" onClick={() => setSelectedNode(null)}>✕</button>
          <div className="badge badge-gold">{selectedNode.category}</div>
          <h3>{selectedNode.label.replace('\n', ' ')}</h3>
          <p>{selectedNode.description}</p>
        </div>
      )}
    </div>
  );
}
