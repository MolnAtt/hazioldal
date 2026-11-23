const CARDINAL_TRESHOLD = 3;
const TENSION = 0.35;
function lerp(a, b, t) {
  return a + t * (b - a);
}
function pointToString(p) {
  return `${(10 + p.x).toFixed(2)},${(110 - p.y).toFixed(2)}`;
}
function lerpPoint(a, b, t) {
  return { x: lerp(a.x, b.x, t), y: lerp(a.y, b.y, t) };
}
function cubicB\u00E9zier(a, c1, c2, b) {
  let t = 0;
  const step = 0.01;
  const points = [];
  while (t <= 1) {
    points.push(calcB\u00E9zierPoint(a, c1, c2, b, t));
    t += step;
  }
  return points.map((x) => pointToString(x)).join(" ");
}
function calcB\u00E9zierPoint(a, c1, c2, b, t) {
  const x = Math.pow(1 - t, 3) * a.x + Math.pow(1 - t, 2) * 3 * t * c1.x + 3 * t * t * (1 - t) * c2.x + Math.pow(t, 3) * b.x;
  const y = Math.pow(1 - t, 3) * a.y + Math.pow(1 - t, 2) * 3 * t * c1.y + 3 * t * t * (1 - t) * c2.y + Math.pow(t, 3) * b.y;
  return { x, y };
}
function controlPointsFromVector(v0, v1, targ, tension = TENSION, treshold = CARDINAL_TRESHOLD) {
  const x = (v1.x - v0.x) * tension / 3 + targ.x;
  const y = (v1.y - v0.y) * tension / 3 + targ.y;
  let c0 = reflect({ x, y }, targ), c1 = { x, y };
  const v0Ratio = Math.abs(v0.y - targ.y) / Math.abs(v0.x - targ.x);
  if (v0Ratio > CARDINAL_TRESHOLD) {
    c0 = { x: v0.x, y: targ.y };
    c1 = reflect(c0, targ);
  }
  const v1Ratio = Math.abs(v1.y - targ.y) / Math.abs(v1.x - targ.x);
  if (v1Ratio > CARDINAL_TRESHOLD) {
    c1 = { x: v1.x, y: targ.y };
    c0 = reflect(c1, targ);
  }
  return [c0, c1];
}
function reflect(a, center) {
  return {
    x: 2 * center.x - a.x,
    y: 2 * center.y - a.y
  };
}
function drawGraph(ponthatar, IQR, id = "svg-graph") {
  const svg = document.getElementById(id);
  if (!svg) return;
  while (svg.firstChild && svg.firstChild.tagName !== 'title') svg.removeChild(svg.firstChild);
  while (svg.firstChild) svg.removeChild(svg.firstChild);

  const ns = 'http://www.w3.org/2000/svg';
  const add = (tag, attrs, text) => {
    const elem = document.createElementNS(ns, tag);
    for (const [key, value] of Object.entries(attrs || {})) elem.setAttribute(key, String(value));
    if (text !== undefined) elem.textContent = text;
    svg.appendChild(elem);
    return elem;
  };
  add('title', { id: 'csoport-grafikon-cim' }, 'Csoporteredmények eloszlása');

  const addTextView = document.getElementById('csoport-szoveges');
  if (addTextView) addTextView.textContent = '';

  const pontok = Array.isArray(IQR)
    ? IQR.filter((x) => typeof x === 'number' && Number.isFinite(x)).map((x) => Math.max(0, Math.min(1, x)))
    : [];

  if (!pontok.length) {
    add('text', { x: 60, y: 60, fill: '#d7d8dc', 'text-anchor': 'middle' }, 'Nincs csoporteredmény.');
    if (addTextView) addTextView.textContent = 'A csoportban nincs értékelhető eredmény.';
    return;
  }

  for (let i = 0; i <= 10; i++) {
    const y = 110 - i * 10;
    add('line', { x1: 9, y1: y, x2: 111, y2: y, stroke: '#777', 'stroke-width': 0.4 });
    add('text', { x: 104, y: y + 3, fill: '#d7d8dc', 'font-size': 5, 'text-anchor': 'end' }, `${i * 10}%`);
  }

  if (pontok.length === 1) {
    const y = 110 - pontok[0] * 100;
    add('circle', { cx: 60, cy: y, r: 3, fill: '#0097fb' });
    add('text', { x: 66, y: y + 2, fill: '#d7d8dc', 'font-size': 5 }, `${(pontok[0] * 100).toFixed(1)}%`);
  } else {
    const points = pontok.map((value, i) => `${25 + i * (50 / (pontok.length - 1))},${110 - value * 100}`).join(' ');
    add('polyline', { points, fill: 'none', stroke: '#0097fb', 'stroke-width': 1.5 });
  }

  add('rect', { x: 9, y: 9, width: 102, height: 102, fill: 'none', stroke: '#d7d8dc', 'stroke-width': 0.5 });

  if (ponthatar && typeof ponthatar === 'object') {
    for (const [jegy, value] of Object.entries(ponthatar)) {
      const numeric = Number(value);
      if (!Number.isFinite(numeric)) continue;
      const y = 110 - Math.max(0, Math.min(100, numeric));
      add('text', { x: 22, y: y + 3, fill: '#d7d8dc', 'font-size': 5, 'text-anchor': 'middle' }, String(jegy));
    }
  }

  if (addTextView) {
    addTextView.textContent = pontok.length === 1
      ? `Egy értékelhető csoporteredmény: ${(pontok[0] * 100).toFixed(1)}%.`
      : `Értékelhető csoporteredmények: ${pontok.map((x) => `${(x * 100).toFixed(1)}%`).join(', ')}.`;
  }
}