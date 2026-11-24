function uj_feladatstatisztikák_svgbe(svg, szelesseg, leptek, feladatok_json, jelmagyarazat = true) {
  if (!svg) return;
  while (svg.firstChild) svg.removeChild(svg.firstChild);

  const lista = Array.isArray(feladatok_json)
    ? feladatok_json
    : Object.keys(feladatok_json || {}).map((nev, id) => ({ id, nev, ...feladatok_json[nev] }));

  if (!lista.length) {
    const szoveg = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    szoveg.setAttribute('x', '10');
    szoveg.setAttribute('y', '30');
    szoveg.setAttribute('fill', '#d7d8dc');
    szoveg.textContent = 'Nincs feladatonkénti adat.';
    svg.appendChild(szoveg);
    return;
  }

  const measuredWidth = Math.max(280, Math.min(900, Math.round(svg.getBoundingClientRect().width || szelesseg || 700)));
  const rowHeight = 92;
  const top = 62;
  const left = 48;
  const right = 20;
  const plotWidth = Math.max(120, measuredWidth - left - right);
  const height = top + lista.length * rowHeight + (jelmagyarazat ? 38 : 10);

  svg.setAttribute('viewBox', `0 0 ${measuredWidth} ${height}`);
  svg.setAttribute('width', '100%');
  svg.setAttribute('height', String(height));
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', 'Feladatonkénti boxplotok 0 és 100 százalék között');

  const ns = 'http://www.w3.org/2000/svg';
  const add = (tag, attrs, text) => {
    const elem = document.createElementNS(ns, tag);
    for (const [key, value] of Object.entries(attrs || {})) elem.setAttribute(key, String(value));
    if (text !== undefined) elem.textContent = text;
    svg.appendChild(elem);
    return elem;
  };

  for (let t = 0; t <= 10; t++) {
    const x = left + (plotWidth * t / 10);
    add('line', { x1: x, y1: top - 20, x2: x, y2: top + lista.length * rowHeight - 20, stroke: '#777', 'stroke-opacity': t === 0 || t === 10 ? 1 : 0.35 });
    add('text', { x, y: top - 29, fill: '#d7d8dc', 'font-size': 11, 'text-anchor': 'middle' }, `${t * 10}%`);
  }

  lista.forEach((feladat, i) => {
    const y = top + i * rowHeight;

    const q = Array.isArray(feladat.szazalek_kvartilis) ? feladat.szazalek_kvartilis : (feladat.kvartilis || []).map((x) => feladat.maxpont > 0 ? x / feladat.maxpont : null);
    const validQ = q.filter((x) => typeof x === 'number' && Number.isFinite(x)).map((x) => Math.max(0, Math.min(1, x)));

    if (validQ.length === 5) {
      const [min, q1, median, q3, max] = validQ;
      const x = (p) => left + plotWidth * p;
      add('line', { x1: x(min), y1: y + 28, x2: x(max), y2: y + 28, stroke: '#d7d8dc', 'stroke-width': 2 });
      add('line', { x1: x(min), y1: y + 18, x2: x(min), y2: y + 38, stroke: '#d7d8dc', 'stroke-width': 2 });
      add('line', { x1: x(max), y1: y + 18, x2: x(max), y2: y + 38, stroke: '#d7d8dc', 'stroke-width': 2 });
      add('rect', { x: x(q1), y: y + 16, width: Math.max(1, x(q3) - x(q1)), height: 24, fill: '#21262d', stroke: '#d7d8dc', 'stroke-width': 2 });
      add('line', { x1: x(median), y1: y + 16, x2: x(median), y2: y + 40, stroke: '#ffe533', 'stroke-width': 4 });

      if (typeof feladat.pont === 'number' && typeof feladat.maxpont === 'number' && feladat.maxpont > 0) {
        const sajat = Math.max(0, Math.min(1, feladat.pont / feladat.maxpont));
        add('circle', { cx: x(sajat), cy: y + 28, r: 7, fill: '#3699ff', stroke: '#ffffff', 'stroke-width': 2 });
      }
    } else if (feladat.allapot === 'hianyzo') {
      add('text', { x: left, y: y + 31, fill: '#d7d8dc', 'font-size': 12 }, 'Hiányzó eredmény');
    } else if (feladat.allapot === 'reszleges') {
      add('text', { x: left, y: y + 31, fill: '#d7d8dc', 'font-size': 12 }, 'Részben javítás alatt');
    }

    let eredmeny = 'Hiányzó';
    if (feladat.allapot === 'reszleges') eredmeny = 'Részleges javítás';
    else if (typeof feladat.pont === 'number') eredmeny = `${Number(feladat.pont.toFixed(2))}/${Number(feladat.maxpont.toFixed(2))}${typeof feladat.szazalek === 'number' ? ` · ${Number((feladat.szazalek * 100).toFixed(1))}%` : ''}`;
    add('text', { x: measuredWidth - 8, y: y + 14, fill: '#ffe533', 'font-size': 12, 'text-anchor': 'end' }, eredmeny);
  });

  if (!jelmagyarazat) return;

  const leg = height - 20;
  add('line', { x1: left, y1: leg, x2: left + 24, y2: leg, stroke: '#d7d8dc', 'stroke-width': 2 });
  add('text', { x: left + 30, y: leg + 4, fill: '#d7d8dc', 'font-size': 10 }, 'Tukey-bajusz');
  add('rect', { x: left + 120, y: leg - 8, width: 22, height: 16, fill: '#21262d', stroke: '#d7d8dc' });
  add('text', { x: left + 148, y: leg + 4, fill: '#d7d8dc', 'font-size': 10 }, 'kvartilisdoboz');
  add('line', { x1: left + 232, y1: leg - 8, x2: left + 232, y2: leg + 8, stroke: '#ffe533', 'stroke-width': 4 });
  add('text', { x: left + 238, y: leg + 4, fill: '#d7d8dc', 'font-size': 10 }, 'medián');
  add('circle', { cx: left + 292, cy: leg, r: 7, fill: '#3699ff', stroke: '#fff' });
  add('text', { x: left + 300, y: leg + 4, fill: '#d7d8dc', 'font-size': 10 }, 'saját eredmény');
}

