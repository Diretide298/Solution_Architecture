/* One plan per venue, in plan units (0–100 on both axes).
   Both the 3D stage and the 2D plan read this file, so the two maps are the same map.
   1 plan unit = 4 metres. */
(function () {
  const PLAN = {
    park: {
      ground: '#1b2a1e', paper: '#20301f', ink: '#8fa885',
      home: 'g1',
      shapes: [
        { id: 'plaza', kind: 'plaza', cx: 50, cy: 50, r: 22, fill: '#3c443c' },
        { id: 'pond', kind: 'water', cx: 50, cy: 50, r: 9, fill: '#1b7fa8' },
        { id: 'gate', kind: 'building', x: 40, y: 4, w: 20, h: 9, ht: 11, wall: '#57606e', glass: '#ffe6ae', label: 'Main gate' },
        { id: 'gateW', kind: 'block', x: 34, y: 6, w: 5, h: 5, ht: 6, fill: '#4a5261' },
        { id: 'gateE', kind: 'block', x: 61, y: 6, w: 5, h: 5, ht: 6, fill: '#4a5261' },
        { id: 'station', kind: 'block', x: 20, y: 28, w: 9, h: 7, ht: 5, fill: '#4a5261', label: 'Coaster station' },
        { id: 'towerBase', kind: 'block', x: 64, y: 28, w: 7, h: 7, ht: 3, fill: '#4a5261', label: 'Freefall Tower' },
        { id: 'carousel', kind: 'ride', cx: 34, cy: 64, r: 8, fill: '#3d4a5c', label: 'Junior Circuit' },
        { id: 'hall', kind: 'building', x: 58, y: 56, w: 18, h: 12, ht: 9, wall: '#6a5442', glass: '#ffd79a', canopy: '#e2603a', label: 'The Crater Grill' },
        { id: 'arcade', kind: 'building', x: 16, y: 56, w: 13, h: 10, ht: 8, wall: '#4f5867', glass: '#bfe4ff', canopy: '#4c9be8', label: 'Dune Coffee' },
        { id: 'shop1', kind: 'block', x: 30, y: 74, w: 6, h: 7, ht: 5.5, fill: '#5a6374', label: 'Summit Store' },
        { id: 'shop2', kind: 'block', x: 37, y: 74, w: 6, h: 7, ht: 5.5, fill: '#4f5867' },
        { id: 'shop3', kind: 'block', x: 44, y: 74, w: 6, h: 7, ht: 5.5, fill: '#5a6374' },
        { id: 'shop4', kind: 'block', x: 51, y: 74, w: 6, h: 7, ht: 5.5, fill: '#4f5867' },
        { id: 'park1', kind: 'parking', x: 78, y: 62, cols: 6, rows: 4, rot: 1, fill: '#2b3138', label: 'East car park' }
      ],
      routes: [
        { name: 'Ring Road', pts: [[16, 20], [50, 10], [84, 22], [90, 56], [66, 88], [28, 84], [10, 52], [16, 20]] },
        { name: 'Central Spine', pts: [[50, 10], [50, 26], [50, 38], [50, 62], [50, 78]] },
        { name: 'Coaster Walk', pts: [[50, 26], [34, 26], [24, 30]] },
        { name: 'Tower Walk', pts: [[50, 26], [66, 28], [70, 32]] },
        { name: 'Wadi Path', pts: [[50, 62], [62, 62], [66, 70], [58, 78]] },
        { name: 'Dunes Path', pts: [[50, 62], [36, 64], [24, 62], [20, 66]] },
        { name: 'Retail Parade', pts: [[50, 78], [40, 78], [33, 78]] },
        { name: 'Car Park Link', pts: [[90, 56], [86, 58], [80, 62]] },
        { name: 'Service Link', pts: [[50, 78], [46, 80], [44, 78]] }
      ]
    },

    water: {
      ground: '#123043', paper: '#12303f', ink: '#7fb6cf',
      home: 'f1',
      shapes: [
        { id: 'pool', kind: 'water', cx: 40, cy: 54, r: 16, fill: '#1b7fa8', label: 'Wave Pool' },
        { id: 'river', kind: 'ring', cx: 50, cy: 50, r: 28, band: 2.6, fill: '#2494bd', label: 'Lazy River' },
        { id: 'tower1', kind: 'building', x: 70, y: 24, w: 6, h: 6, ht: 36, wall: '#54606f', glass: '#bfe4ff', label: 'The Drop' },
        { id: 'tower2', kind: 'building', x: 80, y: 44, w: 6, h: 6, ht: 27, wall: '#54606f', glass: '#bfe4ff', label: 'Vortex' },
        { id: 'entrance', kind: 'building', x: 16, y: 12, w: 18, h: 9, ht: 10, wall: '#4f5867', glass: '#ffe6ae', label: 'Entrance' },
        { id: 'change', kind: 'building', x: 46, y: 12, w: 14, h: 8, ht: 7, wall: '#5a6374', glass: '#bfe4ff', canopy: '#4c9be8', label: 'Changing rooms' },
        { id: 'canteen', kind: 'building', x: 62, y: 66, w: 14, h: 10, ht: 8, wall: '#6a5442', glass: '#ffd79a', canopy: '#e2603a', label: 'Poolside Bar' },
        { id: 'cabanas', kind: 'block', x: 13, y: 74, w: 43, h: 4, ht: 3.2, fill: '#6b5a49', label: 'Cabana Row' },
        { id: 'park1', kind: 'parking', x: 82, y: 58, cols: 5, rows: 4, rot: 1, fill: '#2b3138', label: 'Beach car park' }
      ],
      routes: [
        { name: 'Perimeter Walk', pts: [[14, 16], [86, 16], [88, 60], [88, 84], [12, 86], [14, 16]] },
        { name: 'Entrance Walk', pts: [[14, 16], [22, 20], [30, 30], [34, 42]] },
        { name: 'Pool Deck', pts: [[34, 42], [26, 54], [34, 66], [48, 70], [58, 62], [58, 48], [48, 40], [34, 42]] },
        { name: 'Tower Walk', pts: [[58, 48], [68, 40], [72, 30], [73, 26], [86, 16]] },
        { name: 'Vortex Link', pts: [[68, 40], [78, 44], [83, 46]] },
        { name: 'Cabana Path', pts: [[34, 66], [24, 72], [16, 76], [12, 86]] },
        { name: 'Bar Path', pts: [[58, 62], [64, 68], [68, 70]] },
        { name: 'Car Park Link', pts: [[88, 60], [84, 60], [80, 58]] }
      ]
    },

    stadium: {
      ground: '#141c29', paper: '#18202e', ink: '#8ba0bd',
      home: 'g1',
      shapes: [
        { id: 'pitch', kind: 'pitch', x: 29, y: 35, w: 42, h: 30, fill: '#2f6b3a', label: 'Pitch' },
        { id: 'bowl', kind: 'ring', cx: 50, cy: 50, r: 29, band: 6, fill: '#58657a', label: 'Lower tier' },
        { id: 'upper', kind: 'ring', cx: 50, cy: 50, r: 34, band: 4, fill: '#445061', label: 'Upper tier' },
        { id: 'concourse', kind: 'ring', cx: 50, cy: 50, r: 40, band: 3, fill: '#333b46', label: 'Concourse' },
        { id: 'east', kind: 'building', x: 84, y: 42, w: 12, h: 14, ht: 12, wall: '#4f5867', glass: '#bfe4ff', label: 'Gate C' },
        { id: 'west', kind: 'building', x: 16, y: 58, w: 12, h: 10, ht: 9, wall: '#5a6374', glass: '#ffd79a', canopy: '#e2603a', label: 'Club Store' },
        { id: 'park1', kind: 'parking', x: 88, y: 62, cols: 5, rows: 5, rot: 1, fill: '#2b3138', label: 'East car park' }
      ],
      routes: [
        { name: 'Concourse Ring', pts: [[50, 10], [76, 22], [88, 50], [76, 78], [50, 90], [24, 78], [12, 50], [24, 22], [50, 10]] },
        { name: 'Gate C Approach', pts: [[88, 50], [84, 50], [78, 50]] },
        { name: 'Lower Tier Vomitory', pts: [[76, 22], [66, 28], [62, 30]] },
        { name: 'Block 112 Link', pts: [[24, 22], [34, 26], [38, 26]] },
        { name: 'Club Link', pts: [[50, 90], [50, 84], [50, 80]] },
        { name: 'West Link', pts: [[24, 78], [24, 70], [26, 66]] },
        { name: 'Car Park Link', pts: [[88, 50], [90, 46], [90, 44]] },
        { name: 'Accessible Route', pts: [[12, 50], [22, 46], [30, 42]] },
        { name: 'First Aid Link', pts: [[76, 78], [72, 74], [70, 72]] }
      ]
    },

    theatre: {
      ground: '#1d1826', paper: '#221c2d', ink: '#a496bd',
      home: 'v1',
      shapes: [
        { id: 'house', kind: 'building', x: 32, y: 28, w: 34, h: 26, ht: 18, wall: '#3f3850', glass: '#ffd79a', label: 'Auditorium' },
        { id: 'fly', kind: 'building', x: 44, y: 24, w: 12, h: 10, ht: 34, wall: '#332d42', glass: '#5c5470', label: 'Fly tower' },
        { id: 'portico', kind: 'block', x: 30, y: 54, w: 40, h: 8, ht: 15, fill: '#4a4257', label: 'Portico' },
        { id: 'forecourt', kind: 'plaza', cx: 50, cy: 80, r: 30, fill: '#2a2535' },
        { id: 'cafe', kind: 'building', x: 66, y: 66, w: 12, h: 9, ht: 7, wall: '#4a4257', glass: '#ffd79a', canopy: '#e2603a', label: 'Terrace Café' },
        { id: 'box', kind: 'building', x: 24, y: 66, w: 10, h: 8, ht: 7, wall: '#453e55', glass: '#bfe4ff', label: 'Cloakroom' },
        { id: 'park1', kind: 'parking', x: 78, y: 40, cols: 4, rows: 4, rot: 1, fill: '#2b3138', label: 'Underground parking' }
      ],
      routes: [
        { name: 'Forecourt Walk', pts: [[18, 88], [50, 84], [82, 88]] },
        { name: 'Entrance Steps', pts: [[50, 84], [50, 72], [50, 64]] },
        { name: 'Foyer Walk', pts: [[50, 72], [38, 70], [34, 66]] },
        { name: 'Terrace Walk', pts: [[50, 72], [62, 70], [68, 66]] },
        { name: 'Auditorium Aisle', pts: [[50, 64], [50, 52], [50, 40], [56, 40]] },
        { name: 'Programme Desk Link', pts: [[50, 72], [50, 74]] },
        { name: 'Car Park Link', pts: [[82, 88], [86, 66], [84, 52]] }
      ]
    },

    dining: {
      ground: '#241d17', paper: '#2a211a', ink: '#c0a487',
      home: 'f1',
      shapes: [
        { id: 'room', kind: 'room', x: 28, y: 28, w: 44, h: 26, ht: 2.6, fill: '#4a3b2f', label: 'Dining room' },
        { id: 'kitchen', kind: 'building', x: 62, y: 22, w: 14, h: 10, ht: 7, wall: '#332920', glass: '#ffe6ae', label: 'Kitchen' },
        { id: 'pass', kind: 'block', x: 42, y: 30, w: 18, h: 4, ht: 3.4, fill: '#6b543f', label: 'Kitchen pass' },
        { id: 'terrace', kind: 'deck', x: 28, y: 64, w: 44, h: 16, ht: 0.6, fill: '#5a4838', label: 'Terrace' },
        { id: 'entry', kind: 'plaza', cx: 50, cy: 90, r: 18, fill: '#2a231c' },
        { id: 'park1', kind: 'parking', x: 12, y: 62, cols: 3, rows: 4, rot: 0, fill: '#2b3138', label: 'Valet bay' }
      ],
      routes: [
        { name: 'Arrival Walk', pts: [[18, 88], [50, 88], [82, 88]] },
        { name: 'Front Path', pts: [[50, 88], [50, 80], [50, 72]] },
        { name: 'Terrace Walk', pts: [[50, 72], [36, 70], [30, 70]] },
        { name: 'Dining Aisle', pts: [[50, 72], [50, 58], [50, 46], [50, 38]] },
        { name: 'Private Room Link', pts: [[50, 46], [62, 44], [70, 40]] },
        { name: 'Pantry Link', pts: [[50, 72], [64, 70], [74, 68]] },
        { name: 'Valet Link', pts: [[18, 88], [18, 78], [18, 72]] }
      ]
    }
  };

  // ---- graph: merge route vertices into nodes, edges follow each polyline ----
  const TOL = 2.2;
  function graphOf(v) {
    const p = PLAN[v];
    if (p._graph) return p._graph;
    const nodes = [], edges = [];
    const find = (x, y) => {
      for (let i = 0; i < nodes.length; i++) {
        if (Math.hypot(nodes[i].x - x, nodes[i].y - y) <= TOL) return i;
      }
      nodes.push({ x, y, names: [] });
      return nodes.length - 1;
    };
    p.routes.forEach(r => {
      let prev = null;
      r.pts.forEach(pt => {
        const i = find(pt[0], pt[1]);
        if (nodes[i].names.indexOf(r.name) < 0) nodes[i].names.push(r.name);
        if (prev !== null && prev !== i) {
          const d = Math.hypot(nodes[i].x - nodes[prev].x, nodes[i].y - nodes[prev].y);
          edges.push({ a: prev, b: i, d, name: r.name });
        }
        prev = i;
      });
    });
    const adj = nodes.map(() => []);
    edges.forEach((e, i) => { adj[e.a].push({ to: e.b, e: i }); adj[e.b].push({ to: e.a, e: i }); });
    p._graph = { nodes, edges, adj };
    return p._graph;
  }

  function nearestNode(v, x, y) {
    const g = graphOf(v);
    let best = 0, bd = Infinity;
    g.nodes.forEach((n, i) => { const d = Math.hypot(n.x - x, n.y - y); if (d < bd) { bd = d; best = i; } });
    return best;
  }

  // Dijkstra; returns { nodes:[idx], pts:[[x,y]], legs:[{name,dist}], dist }
  function route(v, from, to) {
    const g = graphOf(v);
    const a = nearestNode(v, from[0], from[1]), b = nearestNode(v, to[0], to[1]);
    if (a === b) return { nodes: [a], pts: [[g.nodes[a].x, g.nodes[a].y]], legs: [], dist: 0 };
    const dist = g.nodes.map(() => Infinity), prev = g.nodes.map(() => null), seen = g.nodes.map(() => false);
    dist[a] = 0;
    for (;;) {
      let u = -1, bd = Infinity;
      for (let i = 0; i < dist.length; i++) if (!seen[i] && dist[i] < bd) { bd = dist[i]; u = i; }
      if (u < 0 || u === b) break;
      seen[u] = true;
      g.adj[u].forEach(l => {
        const nd = dist[u] + g.edges[l.e].d;
        if (nd < dist[l.to]) { dist[l.to] = nd; prev[l.to] = { n: u, e: l.e }; }
      });
    }
    if (!isFinite(dist[b])) return null;
    const chain = [];
    let cur = b;
    while (prev[cur]) { chain.unshift({ from: prev[cur].n, to: cur, e: prev[cur].e }); cur = prev[cur].n; }
    const pts = [[g.nodes[a].x, g.nodes[a].y]].concat(chain.map(c => [g.nodes[c.to].x, g.nodes[c.to].y]));
    const legs = [];
    chain.forEach((c, i) => {
      const nm = g.edges[c.e].name, d = g.edges[c.e].d;
      const last = legs[legs.length - 1];
      if (last && last.name === nm) { last.dist += d; last.endIdx = i + 1; }
      else legs.push({ name: nm, dist: d, startIdx: i, endIdx: i + 1 });
    });
    return { nodes: [a].concat(chain.map(c => c.to)), pts, legs, dist: dist[b] };
  }

  window.TICVAI_PLAN = PLAN;
  window.TICVAI_ROUTE = { graphOf, nearestNode, route, UNIT_M: 4 };
})();
