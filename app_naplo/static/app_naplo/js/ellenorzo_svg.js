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
  if (!svg)
    throw `Unable to draw graph! No element with id "${id}"`;
  for (const disp in ponthatar) {
    const y = 110 - ponthatar[disp];
    svg.innerHTML += `<line x1="9" y1="${y}" x2="111" y2="${y}" style="stroke:${disp.length > 1 ? "#777" : "#d7d8dc"};stroke-width:0.4;"/>`;
    svg.innerHTML += `<text x="22" y="${y + 4}" style="font:5px serif;" text-anchor="middle" fill="#d7d8dc">${disp}</text>`;
    svg.innerHTML += `<text x="98" y="${y + 4}" style="font:5px serif;" text-anchor="middle" fill="#d7d8dc">${ponthatar[disp]}%</text>`;
  }
  const joints = [];
  const dist = 50 / (IQR.length - 1);
  for (let i = 0; i < IQR.length; i++) {
    const p = { x: 25 + i * dist, y: 100 * IQR[i] };
    joints.push(p);
  }
  const cFirst = lerpPoint(joints[0], joints[1], 0.3);
  const cLast = lerpPoint(joints[joints.length - 1], joints[joints.length - 2], 0.3);
  const controlPoints = [cFirst];
  for (let i = 1; i < joints.length - 1; i++) {
    const [c0, c1] = controlPointsFromVector(joints[i - 1], joints[i + 1], joints[i]);
    controlPoints.push(c0, c1);
  }
  controlPoints.push(cLast);
  let keypoints = "";
  for (let i = 0; i < joints.length - 1; i++)
    keypoints += cubicB\u00E9zier(joints[i], controlPoints[i * 2], controlPoints[i * 2 + 1], joints[i + 1]) + " ";
  svg.innerHTML += `<polyline points="${keypoints}" style="fill:none;stroke:#826bfa;" />`;
  svg.innerHTML += `<rect x="9" y="9" width="26" height="102" style="fill:none;stroke:#d7d8dc;" />`;
  svg.innerHTML += `<rect x="85" y="9" width="26" height="102" style="fill:none;stroke:#d7d8dc;" />`;
  svg.innerHTML += `<rect x="9" y="9" width="102" height="102" style="fill:none;stroke:#d7d8dc;" />`;
}