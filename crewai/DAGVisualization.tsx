import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface Block {
  hash: string;
  parentHashes: string[];
  blueScore: number;
  isCanonical: boolean;
}

interface DAGVisualizationProps {
  blocks: Block[];
}

const DAGVisualization: React.FC<DAGVisualizationProps> = ({ blocks }) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = +svg.attr('width');
    const height = +svg.attr('height');

    const simulation = d3.forceSimulation(blocks)
      .force('link', d3.forceLink().id((d: any) => d.hash))
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(blocks.flatMap(b => b.parentHashes.map(p => ({ source: b.hash, target: p }))))
      .enter().append('line');

    const node = svg.append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(blocks)
      .enter().append('circle')
      .attr('r', 5)
      .attr('fill', d => d.isCanonical ? 'blue' : 'red')
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended)
      );

    const label = svg.append('g')
      .attr('class', 'labels')
      .selectAll('text')
      .data(blocks)
      .enter().append('text')
      .text(d => d.hash.slice(0, 6))
      .attr('x', 6)
      .attr('y', 3);

    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node
        .attr('cx', (d: any) => d.x)
        .attr('cy', (d: any) => d.y);
  
      label
        .attr('x', (d: any) => d.x)
        .attr('y', (d: any) => d.y);
    });

    function dragstarted(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }
    
    function dragged(event: any, d: any) {
      d.fx = event.x;
      d.fy = event.y;
    }
    
    function dragended(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

  }, [blocks]);

  return (
    <svg ref={svgRef} width="800" height="600">
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" />
        </marker>
      </defs>
    </svg>
  );
};

export default DAGVisualization;
