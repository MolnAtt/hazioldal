// // debug-hoz egyelőre itt hagyom

// const data = {
//   nev: "Igazságtáblázatok",
//   slug: "igazsagtablazatok",
//   csoport: "22f-szt-bertok",
//   tanar: "mattila",
//   datum: "2022-11-01T15:23:39Z",
//   suly: 1.0,
//   ertekeles: {
//     pont: 5.0,
//     szazalek: 0.8333333333333334,
//     jegy: "4/5",
//   },
//   ponthatar: {
//     "1/2": 28.0,
//     2: 33.0,
//     "2/3": 45.0,
//     3: 50.0,
//     "3/4": 61.0,
//     4: 66.0,
//     "4/5": 82.0,
//     5: 87.0,
//     "5*": 100.0,
//   },
//   feladatonkent: {
//     Formulafa: {
//       pont: 0.0,
//       maxpont: 1.0,
//       atlag: 1.0,
//       modusz: [1.0],
//       kvartilis: [1.0, 1.0, 1.0, 1.0, 1.0],
//       "boxplot-min": 1.0,
//       "boxplot-max": 1.0,
//       outliers: [],
//       extreme_outliers: [],
//     },
//     Kétváltozós: {
//       pont: 1.0,
//       maxpont: 1.0,
//       atlag: 1.0,
//       modusz: [1.0],
//       kvartilis: [1.0, 1.0, 1.0, 1.0, 1.0],
//       "boxplot-min": 1.0,
//       "boxplot-max": 1.0,
//       outliers: [],
//       extreme_outliers: [],
//     },
//     Háromváltozós: {
//       pont: 2.0,
//       maxpont: 2.0,
//       atlag: 1.89,
//       modusz: [2.0],
//       kvartilis: [1.0, 2.0, 2.0, 2.0, 2.0],
//       "boxplot-min": 2.0,
//       "boxplot-max": 2.0,
//       outliers: [1.0, 1.0],
//       extreme_outliers: [1.0, 1.0],
//     },
//     Következtetés: {
//       pont: 2.0,
//       maxpont: 2.0,
//       atlag: 1.56,
//       modusz: [2.0],
//       kvartilis: [1.0, 1.0, 2.0, 2.0, 2.0],
//       "boxplot-min": 1.0,
//       "boxplot-max": 2.0,
//       outliers: [],
//       extreme_outliers: [],
//     },
//   },
//   statisztika: {
//     atlag: {
//       pont: 4.28,
//       szazalek: 0.71,
//       jegy: 3.97,
//     },
//     kvartilis: {
//       pont: [2.0, 4.0, 4.0, 5.0, 6.0],
//       szazalek: [0.3333333333333333, 0.6666666666666666, 0.6666666666666666, 0.8333333333333334, 1.0],
//       jegy: [2, 4, 4.0, 4.5, 5],
//     },
//     modusz: {
//       pont: [4.0, 5.0],
//       szazalek: [0.6666666666666666, 0.8333333333333334],
//       jegy: [4, 4.5],
//     },
//     atlagos_abszolut_elteres: {
//       pont: 0.7533333333333331,
//       szazalek: 0.12518518518518526,
//       jegy: 0.5477777777777773,
//     },
//     szorasnegyzet: {
//       pont: 0.867288888888889,
//       szazalek: 0.024100000000000003,
//       jegy: 0.6242333333333331,
//     },
//     IQR_grafikon: [
//       0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666,
//       0.8333333333333334, 0.8333333333333334, 0.8333333333333334, 0.8333333333333334, 0.8333333333333334, 0.8333333333333334, 0.8333333333333334,
//     ],
//   },
// };




function szazalekracs(v, N, leptek) {
  for (let j = 0; j <= 10; j++) {
    v.szovegdoboz({
      P: new Pont(j + 0.25, 1.5),
      szoveg: `${j * 10}%`,
      font: "10px serif",
      align: "center",
      forgatas: -Math.PI / 2,
      szin:"white",
    });

    let F = new Pont(j, 0);
    let A = new Pont(j, -N * leptek);

    v.vonal(F, A, 0.3);
  }
}

function feladatstatisztikák(v, feladatok_json) {
  let leptek = 1;
  let feladatok = Object.keys(feladatok_json);
  let N = feladatok.length;
  v.resize(400, N * 40, new Pont(100, 50), new Pont(10, 10));
  // v.context.fillStyle = "#3d4046";
  // v.context.fillRect(0, 0, v.canvas.width, v.canvas.height);
  szazalekracs(v, N, leptek * 2);
  let i = 1;
  for (const feladat of feladatok) {
    v.szovegdoboz({
      P: new Pont(-1, -(i + 0.8)),
      szoveg: feladat,
      font: "10px serif",
      align: "right",
      forgatas: 0,
      szin: "white",
    });

    let feladat_pontja = feladatok_json[feladat].pont;
    let feladat_maxpontja = feladatok_json[feladat].maxpont;

    let w = 10;

    v.boxplot({
      O: new Pont(0, -(i + 1)),
      w: w,
      h: leptek,
      linewidth: 1.5,
      medianwidth: 4,
      kvartilis: feladatok_json[feladat].kvartilis.map((k) => k / feladat_maxpontja),
      outliers: feladatok_json[feladat].outliers.map((o) => o / feladat_maxpontja),
      extreme_outliers: feladatok_json[feladat].extreme_outliers.map((o) => o / feladat_maxpontja),
      kiemelt_pont: feladat_pontja / feladat_maxpontja,
      szin: "white",
    });

    v.szovegdoboz({
      P: new Pont(1 + w, -(i + 0.8)),
      szoveg: `${feladat_pontja}/${feladat_maxpontja}`,
      font: "10px serif",
      align: "left",
      forgatas: 0,
      szin:"white",
    });

    i += leptek * 2;
  }
}



function osztalygrafikon(v, w, h, ponthatar, IQR_grafikon) {
  // let w = 250;
  // let h = 250;
  v.resize(w, h, new Pont(0.05 * w, 0.95 * h), new Pont(0.009 * w, 0.009 * h));

  let BBA = new Pont(0, 0);
  let BBF = new Pont(0, 100);
  let BJF = new Pont(25, 100);
  let BJA = new Pont(25, 0);
  v.teglalap(BBA, BBF, BJF, BJA, 1, "black", "gray");

  let JBA = new Pont(75, 0);
  let JBF = new Pont(75, 100);
  let JJF = new Pont(100, 100);
  let JJA = new Pont(100, 0);

  v.teglalap(JBA, JBF, JJF, JJA, 1, "black", "gray");

  v.teglalap(BBA, BBF, JJF, JJA, 1, "black", "gray");

  let jegyek = Object.keys(ponthatar);
  for (const jegy of jegyek) {
    let magassag = ponthatar[jegy];
    v.szovegdoboz({
      P: new Pont(12.5, magassag),
      szoveg: jegy,
      font: "10px serif",
      align: "center",
      forgatas: 0,
    });

    v.szovegdoboz({
      P: new Pont(87.5, magassag),
      szoveg: `${ponthatar[jegy]}%`,
      font: "10px serif",
      align: "center",
      forgatas: 0,
    });

    if (1 < jegy.length) {
      // console.log(`${jegy}: ${jegy.length}`);
      v.vonal(new Pont(0, magassag), new Pont(100, magassag), 0.1);
    } else {
      v.vonal(new Pont(0, magassag), new Pont(100, magassag), 0.5);
    }

    let honnan = 25;
    let meddig = 75;
    let tav = meddig - honnan;
    let pontleptek = tav / (IQR_grafikon.length - 1);

    pontlista = [];
    for (let i = 0; i < IQR_grafikon.length; i++) {
      let P = new Pont(honnan + i * pontleptek, 100 * IQR_grafikon[i]);
      // v.kor(P, 2, 1, 'black', 'black');
      pontlista.push(P);
    }

    v.gorbe(pontlista, 0.2); //default tension=0.5
  }
}

// let canvaselem = document.querySelector('#canvaselem');
// let canvaselem2 = document.querySelector("#canvaselem2");

function setText(id, text) {
  const elem = document.getElementById(id);
  if (elem) elem.textContent = text == null ? '—' : String(text);
}

function finiteNumber(value) {
  if (value === null || value === undefined) return null;
  if (typeof value === 'string' && value.trim() === '') return null;
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function szepdatum(value) {
  if (value === null || value === undefined || value === '') return null;
  const datum = new Date(value);
  if (Number.isNaN(datum.getTime())) return null;
  const ketjegyu = (n) => String(n).padStart(2, '0');
  return `${datum.getFullYear()}.${ketjegyu(datum.getMonth() + 1)}.${ketjegyu(datum.getDate())}.`;
}

let feladatObserverek = [];

function observerek_leallitasa() {
  feladatObserverek.forEach((observer) => observer.disconnect());
  feladatObserverek = [];
}

function formatPont(value) {
  const number = finiteNumber(value);
  return number === null ? '—' : Number(number.toFixed(2)).toString();
}

function formatSzazalek(value) {
  const number = finiteNumber(value);
  if (number === null) return '—';
  return `${Number((number * 100).toFixed(1))}%`;
}

function explicitJegySzam(jegy) {
  const map = {'1': 1, '1/2': 1.5, '2': 2, '2/3': 2.5, '3': 3, '3/4': 3.5, '4': 4, '4/5': 4.5, '5': 5, '5*': 5};
  return map[String(jegy)] ?? null;
}

function oldal_kitoltese_json_alapjan(adatok) {
  if (!adatok || typeof adatok !== 'object') {
    setText('api-allapot', 'Nem érkezett feldolgozható adat.');
    return;
  }

  observerek_leallitasa();
  setText('api-allapot', 'Az adatok betöltve.');
  setText('h1', adatok.nev);
  try {
    const datum = szepdatum(adatok.datum);
    if (datum) setText('datum', datum);
  } catch (error) {
    console.error('A dátum megjelenítése sikertelen:', error);
  }

  const ertekeles = adatok.ertekeles || {};
  setText('ertekeles_pont', formatPont(ertekeles.pont));
  const feladatok = Array.isArray(adatok.feladatonkent) ? adatok.feladatonkent : [];
  const maxpont = feladatok.reduce((sum, feladat) => sum + (finiteNumber(feladat.maxpont) || 0), 0);
  setText('ertekeles_maxpont', formatPont(maxpont));
  if (ertekeles.allapot === 'hianyzo') setText('ertekeles_szazalek', 'Hiányzó');
  else if (ertekeles.allapot === 'reszleges') setText('ertekeles_szazalek', 'Részleges');
  else if (ertekeles.szazalek !== null && ertekeles.szazalek !== undefined) setText('ertekeles_szazalek', formatSzazalek(ertekeles.szazalek));
  else setText('ertekeles_szazalek', maxpont === 0 ? 'Maximum 0' : '—');
  setText('ertekeles_jegy', ertekeles.jegy == null ? (ertekeles.allapot === 'hianyzo' ? 'Hiányzó' : ertekeles.allapot === 'reszleges' ? 'Részleges' : '—') : ertekeles.jegy);
  setText('ertekeles_suly', formatPont(adatok.suly));

  if (adatok.ponthatar && typeof adatok.ponthatar === 'object') {
    const tbody = document.querySelector('#ponthatarok tbody');
    if (tbody) {
      while (tbody.firstChild) tbody.removeChild(tbody.firstChild);
      for (const [jegy, value] of Object.entries(adatok.ponthatar)) {
        const tr = document.createElement('tr');
        const th = document.createElement('th');
        th.scope = 'row';
        th.textContent = String(jegy);
        const td = document.createElement('td');
        td.textContent = `${formatPont(value)}%`;
        tr.append(th, td);
        tbody.appendChild(tr);
      }
    }
  }

  const lista = document.getElementById('feladatlista');
  if (lista) {
    while (lista.firstChild) lista.removeChild(lista.firstChild);
    const szoveges = document.getElementById('feladat-szoveges');
    if (szoveges) szoveges.textContent = '';

    if (!feladatok.length) {
      const ures = document.createElement('p');
      ures.textContent = 'Ehhez a dolgozathoz nincs feladatonkénti eredmény.';
      lista.appendChild(ures);
    }

    feladatok.forEach((feladat, index) => {
      const sor = document.createElement('article');
      sor.className = 'feladat-sor';

      const nevBlokk = document.createElement('div');
      const h3 = document.createElement('h3');
      h3.textContent = String(feladat.nev || `Feladat ${index + 1}`);
      const adat = document.createElement('p');
      adat.className = 'feladat-adatok';

      let eredmeny;
      if (feladat.allapot === 'hianyzo') eredmeny = 'Hiányzó eredmény';
      else if (feladat.allapot === 'reszleges') eredmeny = 'Részleges / javítás alatt';
      else if (typeof feladat.pont === 'number') eredmeny = `${formatPont(feladat.pont)}/${formatPont(feladat.maxpont)} pont${typeof feladat.szazalek === 'number' ? ` · ${formatSzazalek(feladat.szazalek)}` : ''}`;
      else eredmeny = feladat.maxpont === 0 ? '0 maximumpont' : 'Nincs értékelhető pont';
      adat.textContent = eredmeny;
      nevBlokk.append(h3, adat);

      const graf = document.createElement('div');
      graf.className = 'feladat-grafikon';
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.id = `feladat-boxplot-${index}`;
      svg.setAttribute('role', 'img');
      svg.setAttribute('aria-label', `${String(feladat.nev || `Feladat ${index + 1}`)} boxplotja. ${eredmeny}`);
      graf.appendChild(svg);

      sor.append(nevBlokk, graf);
      lista.appendChild(sor);
      uj_feladatstatisztikák_svgbe(svg, 700, 92, [feladat]);

      if (szoveges) {
        const p = document.createElement('p');
        p.textContent = `${String(feladat.nev || `Feladat ${index + 1}`)}: ${eredmeny}.`;
        szoveges.appendChild(p);
      }

      if ('ResizeObserver' in window) {
        const observer = new ResizeObserver(() => uj_feladatstatisztikák_svgbe(svg, 700, 92, [feladat]));
        observer.observe(graf);
        feladatObserverek.push(observer);
      }
    });
  }

  const stat = adatok.statisztika || {};
  const torzs = document.getElementById('statisztika-torzs');
  if (torzs) {
    while (torzs.firstChild) torzs.removeChild(torzs.firstChild);
    const avg = stat.atlag || {};
    const kvartilis = stat.kvartilis || {};
    const modusz = stat.modusz || {};
    const abs = stat.atlagos_abszolut_elteres || {};
    const variancia = stat.szorasnegyzet || {};
    const sajatPont = finiteNumber(ertekeles.pont);
    const sajatSzazalek = finiteNumber(ertekeles.szazalek);
    const sajatJegy = explicitJegySzam(ertekeles.jegy);

    const rows = [
      ['Átlag', formatSzazalek(avg.szazalek), `${formatPont(avg.pont)} pt`, formatPont(avg.jegy)],
      ['Medián', formatSzazalek(kvartilis.szazalek ? kvartilis.szazalek[2] : null), `${formatPont(kvartilis.pont ? kvartilis.pont[2] : null)} pt`, formatPont(kvartilis.jegy ? explicitJegySzam(kvartilis.jegy[2]) : null)],
      ['Módusz', modusz.szazalek && modusz.szazalek.length ? modusz.szazalek.map(formatSzazalek).join(', ') : '—', modusz.pont && modusz.pont.length ? modusz.pont.map(formatPont).join(', ') : '—', modusz.jegy && modusz.jegy.length ? modusz.jegy.map(formatPont).join(', ') : '—'],
      ['Saját eltérés az átlagtól', avg.szazalek === null || avg.szazalek === undefined || sajatSzazalek === null ? '—' : `${sajatSzazalek >= avg.szazalek ? '+' : ''}${Number(((sajatSzazalek - avg.szazalek) * 100).toFixed(2))} százalékpont`, avg.pont === null || avg.pont === undefined || sajatPont === null ? '—' : `${sajatPont >= avg.pont ? '+' : ''}${formatPont(sajatPont - avg.pont)} pt`, avg.jegy === null || avg.jegy === undefined || sajatJegy === null ? '—' : `${sajatJegy >= avg.jegy ? '+' : ''}${formatPont(sajatJegy - avg.jegy)} jegypont`],
      ['Átlagos abszolút eltérés', formatSzazalek(abs.szazalek), `${formatPont(abs.pont)} pt`, formatPont(abs.jegy)],
      ['Kvartilis-távolság (IQR)', kvartilis.szazalek ? formatSzazalek((kvartilis.szazalek[3] || 0) - (kvartilis.szazalek[1] || 0)) : '—', kvartilis.pont ? `${formatPont(kvartilis.pont[3] - kvartilis.pont[1])} pt` : '—', kvartilis.jegy ? formatPont(explicitJegySzam(kvartilis.jegy[3]) - explicitJegySzam(kvartilis.jegy[1])) : '—'],
      ['Szórás', variancia.szazalek === null || variancia.szazalek === undefined ? '—' : `${Number((100 * Math.sqrt(Math.max(0, variancia.szazalek))).toFixed(2))}%`, variancia.pont === null || variancia.pont === undefined ? '—' : `${formatPont(Math.sqrt(Math.max(0, variancia.pont)))} pt`, variancia.jegy === null || variancia.jegy === undefined ? '—' : formatPont(Math.sqrt(Math.max(0, variancia.jegy)))],
    ];

    rows.forEach((row) => {
      const tr = document.createElement('tr');
      row.forEach((value, column) => {
        const cell = document.createElement(column === 0 ? 'th' : 'td');
        if (column === 0) cell.scope = 'row';
        cell.textContent = String(value);
        tr.appendChild(cell);
      });
      torzs.appendChild(tr);
    });
  }

  try {
    drawGraph(adatok.ponthatar || {}, stat.IQR_grafikon || []);
  } catch (error) {
    console.error('A csoportközép-grafikon rajzolása sikertelen:', error);
    setText('csoport-grafikon-leiras', 'A csoportközép-grafikon nem rajzolható, de a saját eredmények és a boxplotok elérhetők.');
  }
}

async function main() {
  const hiddenCsoport = document.getElementById('a_csoport');
  const hiddenSlug = document.getElementById('a_dolgozatslug');
  const hiddenUser = document.getElementById('a_user');
  const state = document.getElementById('api-allapot');

  const initial = document.getElementById('dolgozat-adatok');
  if (initial) {
    try {
      oldal_kitoltese_json_alapjan(JSON.parse(initial.textContent));
    } catch (error) {
      console.error('A szerveroldali alapadatok feldolgozása sikertelen:', error);
      if (state) state.textContent = 'A szerveroldali alapadatok feldolgozása sikertelen.';
    }
  }

  if (!hiddenCsoport || !hiddenSlug || !hiddenUser) return;
  const url = `${window.location.origin}/naplo/api/post/dolgozat/read/${encodeURIComponent(hiddenCsoport.value)}/${encodeURIComponent(hiddenSlug.value)}/${encodeURIComponent(hiddenUser.value)}/`;

  let retryCount = 0;
  const betolt = async () => {
    if (state) state.textContent = retryCount ? 'Újrapróbálás…' : 'Betöltés…';
    try {
      const adatok = await olvaso_fetch(url);
      oldal_kitoltese_json_alapjan(adatok);
    } catch (error) {
      console.error('A dolgozat adatainak betöltése sikertelen:', error);
      if (state) {
        state.textContent = '';
        const span = document.createElement('span');
        span.textContent = error.message;
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = 'Újrapróbálás';
        button.addEventListener('click', () => { retryCount++; betolt(); });
        state.append(span, document.createTextNode(' '), button);
      }
    }
  };

  betolt();
}

let mainIndult = false;

function main_inditasa() {
  if (mainIndult) return;
  mainIndult = true;
  main().catch((error) => {
    console.error('Az oldal inicializálása sikertelen:', error);
    setText('api-allapot', 'Az oldal betöltése sikertelen.');
  });
}

// A defer scriptek (a drawGraph-ot tartalmazó is) a DOMContentLoaded előtt lefutnak.
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', main_inditasa);
else main_inditasa();
