// debug-hoz egyelőre itt hagyom

const data = {
  nev: "Igazságtáblázatok",
  slug: "igazsagtablazatok",
  csoport: "22f-szt-bertok",
  tanar: "mattila",
  datum: "2022-11-01T15:23:39Z",
  suly: 1.0,
  ertekeles: {
    pont: 5.0,
    szazalek: 0.8333333333333334,
    jegy: "4/5",
  },
  ponthatar: {
    "1/2": 28.0,
    2: 33.0,
    "2/3": 45.0,
    3: 50.0,
    "3/4": 61.0,
    4: 66.0,
    "4/5": 82.0,
    5: 87.0,
    "5*": 100.0,
  },
  feladatonkent: {
    Formulafa: {
      pont: 0.0,
      maxpont: 1.0,
      atlag: 1.0,
      modusz: [1.0],
      kvartilis: [1.0, 1.0, 1.0, 1.0, 1.0],
      "boxplot-min": 1.0,
      "boxplot-max": 1.0,
      outliers: [],
      extreme_outliers: [],
    },
    Kétváltozós: {
      pont: 1.0,
      maxpont: 1.0,
      atlag: 1.0,
      modusz: [1.0],
      kvartilis: [1.0, 1.0, 1.0, 1.0, 1.0],
      "boxplot-min": 1.0,
      "boxplot-max": 1.0,
      outliers: [],
      extreme_outliers: [],
    },
    Háromváltozós: {
      pont: 2.0,
      maxpont: 2.0,
      atlag: 1.89,
      modusz: [2.0],
      kvartilis: [1.0, 2.0, 2.0, 2.0, 2.0],
      "boxplot-min": 2.0,
      "boxplot-max": 2.0,
      outliers: [1.0, 1.0],
      extreme_outliers: [1.0, 1.0],
    },
    Következtetés: {
      pont: 2.0,
      maxpont: 2.0,
      atlag: 1.56,
      modusz: [2.0],
      kvartilis: [1.0, 1.0, 2.0, 2.0, 2.0],
      "boxplot-min": 1.0,
      "boxplot-max": 2.0,
      outliers: [],
      extreme_outliers: [],
    },
  },
  statisztika: {
    atlag: {
      pont: 4.28,
      szazalek: 0.71,
      jegy: 3.97,
    },
    kvartilis: {
      pont: [2.0, 4.0, 4.0, 5.0, 6.0],
      szazalek: [0.3333333333333333, 0.6666666666666666, 0.6666666666666666, 0.8333333333333334, 1.0],
      jegy: [2, 4, 4.0, 4.5, 5],
    },
    modusz: {
      pont: [4.0, 5.0],
      szazalek: [0.6666666666666666, 0.8333333333333334],
      jegy: [4, 4.5],
    },
    atlagos_abszolut_elteres: {
      pont: 0.7533333333333331,
      szazalek: 0.12518518518518526,
      jegy: 0.5477777777777773,
    },
    szorasnegyzet: {
      pont: 0.867288888888889,
      szazalek: 0.024100000000000003,
      jegy: 0.6242333333333331,
    },
    IQR_grafikon: [
      0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666,
      0.8333333333333334, 0.8333333333333334, 0.8333333333333334, 0.8333333333333334, 0.8333333333333334, 0.8333333333333334, 0.8333333333333334,
    ],
  },
};




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

async function main() {
   let url = `${ window.location.origin}/naplo/api/post/dolgozat/read/${a_csoport.value}/${a_dolgozatslug.value}/`;
  /** /
  const adatok = data; 
  /*/
  const adatok = await olvaso_fetch(url);
  /**/
  console.log('itt vannak az adatok:');
  console.log(adatok);

  // console.log("ezek az adatok jöttek vissza:");
  // console.log(adatok);
  console.log(url);
  console.log("ha szeretnéd, látogasd meg, kipróbálhatod, hogy működik az ellenőrző-API. Viszont be kell legyél jelentkezve hozzá.")
  oldal_kitoltese_json_alapjan(adatok);
}

function kerekit_tizhatvannyal(tizhatvany, szam){ return Math.round(szam*tizhatvany)/tizhatvany; }
function kerekit(tizedesjegy, szam){ return kerekit_tizhatvannyal(10**2, szam).toFixed(tizedesjegy); }
function szepdatum(d){ return `${d.substring(0, 4)}.${d.substring(5, 7)}.${d.substring(8, 10)}.`;}
function hamegirta(megirta, ertek){ return megirta?ertek:"-";}


function oldal_kitoltese_json_alapjan(adatok){
  let megirta = 0 <= adatok.ertekeles.pont;

  // HEADER
  
  h1.innerHTML = adatok.nev;
  datum.innerHTML = szepdatum(adatok.datum);
  
  // ÉRTÉKELÉS
  
  ertekeles_pont.innerHTML = hamegirta(megirta, adatok.ertekeles.pont);
  ertekeles_maxpont.innerHTML = Object.entries(adatok.feladatonkent).map((x) => x[1].maxpont).reduce((s,e) => s+e, 0);
  ertekeles_szazalek.innerHTML = hamegirta(megirta, `${kerekit(2, 100*adatok.ertekeles.szazalek)}%`);
  ertekeles_jegy.innerHTML = hamegirta(megirta, adatok.ertekeles.jegy);
  ertekeles_suly.innerHTML = kerekit(1,adatok.suly);
  
  // PONTHATÁROK
  
  for (const key in adatok.ponthatar) {
    let jegyelem = document.querySelector("#jegy" + key.replace("/", "").replace("*", "5"));
    jegyelem.innerHTML = " " + adatok.ponthatar[key] + "%";
  }
  
  // STATISZTIKAI MUTATÓK: GRID/TÁBLÁZAT
  
  atlag_szazalek.innerHTML = `${kerekit(2, 100*adatok.statisztika.atlag.szazalek)}%`;
  atlag_pont.innerHTML = `${adatok.statisztika.atlag.pont} pt`;
  atlag_jegy.innerHTML = adatok.statisztika.atlag.jegy;
  
  median_szazalek.innerHTML += `${kerekit(2,adatok.statisztika.kvartilis.szazalek[2])}%`;
  median_pont.innerHTML +=`${adatok.statisztika.kvartilis.pont[2]} pt`;
  median_jegy.innerHTML += adatok.statisztika.kvartilis.jegy[2];
  
  // modusz_szazalek.innerHTML += adatok.statisztika.modusz.szazalek.map(x => `${kerekit(2, 100*x)}%`).join(", ");
  // modusz_pont.innerHTML += adatok.statisztika.modusz.pont.map(x => `${x} pt`).join(", ");
  modusz_jegy.innerHTML += adatok.statisztika.modusz.jegy.join(", ");
  
  atlagtol_valo_elteres_szazalek.innerHTML = hamegirta(megirta, `${kerekit(2, Math.abs(adatok.statisztika.atlag.szazalek - adatok.ertekeles.szazalek)*100)}%`); 
  atlagtol_valo_elteres_pont.innerHTML = hamegirta(megirta, `${kerekit(2, Math.abs(adatok.statisztika.atlag.pont - adatok.ertekeles.pont))} pt`);
  atlagtol_valo_elteres_jegy.innerHTML = hamegirta(megirta, kerekit(2, Math.abs(adatok.statisztika.atlag.jegy - adatok.ertekeles.jegy.replace('/', '.'))));
  
  atlagos_abszolut_elteres_szazalek.innerHTML = `${kerekit(2, 100*adatok.statisztika.atlagos_abszolut_elteres.szazalek)}%`;
  atlagos_abszolut_elteres_pont.innerHTML = `${kerekit(2, adatok.statisztika.atlagos_abszolut_elteres.pont)} pt`;
  atlagos_abszolut_elteres_jegy.innerHTML = kerekit(2, adatok.statisztika.atlagos_abszolut_elteres.jegy);
  
  IQR_szazalek.innerHTML = `${kerekit(2, 100*(adatok.statisztika.kvartilis.szazalek[3] - adatok.statisztika.kvartilis.szazalek[1]))}%`;
  IQR_pont.innerHTML = `${kerekit(2, adatok.statisztika.kvartilis.pont[3] - adatok.statisztika.kvartilis.pont[1])} pt`;
  IQR_jegy.innerHTML = kerekit(2, adatok.statisztika.kvartilis.jegy[3] - adatok.statisztika.kvartilis.jegy[1]);
  
  szoras_szazalek.innerHTML = `${kerekit(2, Math.sqrt(100*adatok.statisztika.szorasnegyzet.szazalek))}%`;
  szoras_pont.innerHTML = `${kerekit(2, Math.sqrt(adatok.statisztika.szorasnegyzet.pont))} pt`
  szoras_jegy.innerHTML = kerekit(2, Math.sqrt(adatok.statisztika.szorasnegyzet.jegy));
  
  // CSOPORTKÖZÉP ELOSZLÁSA: (DaPa svg-je)
  drawGraph(adatok.ponthatar, adatok.statisztika.IQR_grafikon);
  
  // FELADATONKÉNTI STATISZTIKÁK: BOXPLOTOK

  console.log('futok az oldal kitöltésével');
  
  console.log(boxplot_svg);

  uj_feladatstatisztikák_svgbe(boxplot_svg, 400, 40, adatok.feladatonkent);


}

main();