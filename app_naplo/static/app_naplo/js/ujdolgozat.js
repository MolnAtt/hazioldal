const csrftoken = getCookie('csrftoken');
const kezdoCsv = document.getElementById('feladatok').value;
let csvMod = false;

main();

function main() {
    document.getElementById('kuld').addEventListener('click', dolgozat_intezese);
    document.getElementById('ujfeladat').addEventListener('click', () => {
        const sor = feladatsor_hozzaadasa('', '1');
        sor.querySelector('.feladatnev').focus();
    });
    document.getElementById('modvalto').addEventListener('click', modvaltas);
    document.getElementById('feladatlista').addEventListener('input', () => hibauzenet_torlese());
    document.getElementById('feladatok').addEventListener('input', () => hibauzenet_torlese());

    csv_betoltese_listaba(kezdoCsv);
}

////////////////////////////////
// Feladatlista

function feladatsor_hozzaadasa(nev, maxpont) {
    const sor = document.createElement('div');
    sor.className = 'feladatsor';

    const nevInput = document.createElement('input');
    nevInput.type = 'text';
    nevInput.className = 'feladatnev';
    nevInput.placeholder = 'Feladat neve';
    nevInput.setAttribute('aria-label', 'Feladat neve');
    nevInput.value = nev;

    const pontInput = document.createElement('input');
    pontInput.type = 'number';
    pontInput.className = 'feladatmax';
    pontInput.min = '0';
    pontInput.step = 'any';
    pontInput.placeholder = 'Max';
    pontInput.setAttribute('aria-label', 'Maximális pontszám');
    pontInput.value = maxpont;

    const torles = document.createElement('button');
    torles.type = 'button';
    torles.className = 'torles';
    torles.textContent = '🗑';
    torles.title = 'Feladat törlése';
    torles.setAttribute('aria-label', 'Feladat törlése');
    torles.addEventListener('click', () => {
        sor.remove();
        hibauzenet_torlese();
    });

    sor.append(nevInput, pontInput, torles);
    document.getElementById('feladatlista').appendChild(sor);
    return sor;
}

function listabol_feladatok() {
    return [...document.querySelectorAll('#feladatlista .feladatsor')].map((sor) => ({
        nev: sor.querySelector('.feladatnev').value.trim(),
        maxpont: sor.querySelector('.feladatmax').value.trim(),
        sor,
    }));
}

function csv_feladatok(csv) {
    return csv.split('\n')
        .filter((sor) => sor.trim() !== '')
        .map((sor) => {
            const resz = sor.split(';');
            return { nev: (resz[0] || '').trim(), maxpont: (resz[1] || '').trim(), mezok: resz.length };
        });
}

function csv_betoltese_listaba(csv) {
    document.getElementById('feladatlista').replaceChildren();
    csv_feladatok(csv).forEach((f) => feladatsor_hozzaadasa(f.nev, f.maxpont));
}

function feladatok_csvbe(feladatok) {
    return feladatok.map((f) => `${f.nev};${f.maxpont}`).join('\n');
}

function modvaltas() {
    if (csvMod) {
        const sorok = csv_feladatok(document.getElementById('feladatok').value);
        if (sorok.some((f) => f.mezok !== 2)) {
            hibauzenet_mutatasa('A CSV-ben minden sorban pontosan egy ";" lehet (feladatnév;maxpont).');
            return;
        }
        csv_betoltese_listaba(document.getElementById('feladatok').value);
    } else {
        document.getElementById('feladatok').value = feladatok_csvbe(listabol_feladatok());
    }
    csvMod = !csvMod;
    document.getElementById('csv-nezet').hidden = !csvMod;
    document.getElementById('feladatlista-nezet').hidden = csvMod;
    document.getElementById('modvalto').textContent = csvMod ? 'Szerkesztés listaként' : 'Szerkesztés CSV-ként';
    hibauzenet_torlese();
}

function aktualis_feladatok() {
    return csvMod ? csv_feladatok(document.getElementById('feladatok').value) : listabol_feladatok();
}

////////////////////////////////
// Ellenőrzés

function hibauzenet_mutatasa(szoveg) {
    const elem = document.getElementById('hibauzenet');
    elem.textContent = szoveg;
    elem.hidden = false;
}

function hibauzenet_torlese() {
    document.getElementById('hibauzenet').hidden = true;
    document.querySelectorAll('.hibas').forEach((e) => e.classList.remove('hibas'));
}

function feladatok_ellenorzese(feladatok) {
    document.querySelectorAll('.hibas').forEach((e) => e.classList.remove('hibas'));
    if (feladatok.length === 0) return 'Legalább egy feladatot meg kell adni!';

    const jelol = (f, osztaly = '.feladatnev') => { if (f.sor) f.sor.querySelector(osztaly).classList.add('hibas'); };
    const latott = new Map();

    for (const f of feladatok) {
        if (f.nev === '') { jelol(f); return 'Minden feladatnak kell nevet adni!'; }
        if (f.nev.includes(';')) { jelol(f); return `A feladat neve nem tartalmazhat pontosvesszőt: ${f.nev}`; }
        const max = Number(f.maxpont);
        if (f.maxpont === '' || !Number.isFinite(max) || max < 0) {
            jelol(f, '.feladatmax');
            return `A(z) "${f.nev}" feladat maximális pontszáma nem érvényes (nemnegatív szám kell)!`;
        }
    }

    for (const f of feladatok) {
        if (latott.has(f.nev)) {
            jelol(f);
            jelol(latott.get(f.nev));
            return `Két feladatnak nem lehet ugyanaz a neve: "${f.nev}"!`;
        }
        latott.set(f.nev, f);
    }
    return null;
}

////////////////////////////////
// Küldés

async function dolgozat_intezese() {
    hibauzenet_torlese();
    const feladatok = aktualis_feladatok();
    const hiba = feladatok_ellenorzese(feladatok);
    if (hiba) {
        hibauzenet_mutatasa(hiba);
        return;
    }

    try {
        const [res, siker] = await create_dolgozat(feladatok);
        const uzenet = typeof res === 'string' ? res : res.uzenet;
        console.log(uzenet);
        if (!siker) {
            hibauzenet_mutatasa(uzenet);
            return;
        }
        alert(uzenet);
        document.getElementById('tovabblink').href =
            `/naplo/${res.ev}/csoport/${document.getElementById('csoportnev').value}/${document.getElementById('dolgozatslug').value}/`;
    } catch (error) {
        console.error('A dolgozat létrehozása sikertelen:', error);
        hibauzenet_mutatasa('A dolgozat létrehozása sikertelen.');
    }
}

async function create_dolgozat(feladatok) {
    const ertek = (id) => document.getElementById(id).value;

    if (ertek('dolgozatnev') == '') return ['Nincs kitöltve a dolgozat neve!', false];
    if (ertek('dolgozatslug') == '') return ['Nincs kitöltve a dolgozat slug!', false];
    if (ertek('csoportnev') == '') return ['Nincs kitöltve a csoport!', false];
    if (ertek('suly') == '') return ['Nincs kitöltve a súly!', false];
    if (ertek('datum') == '') return ['Nincs kitöltve a dátum!', false];

    let url = `${window.location.origin}/naplo/api/post/dolgozat/create/`;
    let szotar = {
        'dolgozat_nev': ertek('dolgozatnev'),
        'dolgozat_slug': ertek('dolgozatslug'),
        'csoport_nev': ertek('csoportnev'),
        'ponthatar2': ertek('ponthatar2'),
        'ponthatar3': ertek('ponthatar3'),
        'ponthatar4': ertek('ponthatar4'),
        'ponthatar5': ertek('ponthatar5'),
        'ponthatar55': ertek('ponthatar55'),
        'ponthatar12': ertek('ponthatar12'),
        'ponthatar23': ertek('ponthatar23'),
        'ponthatar34': ertek('ponthatar34'),
        'ponthatar45': ertek('ponthatar45'),
        'feladatcsv': feladatok_csvbe(feladatok),
        'suly': ertek('suly'),
        'datum': ertek('datum'),
    };
    let res = await kuldo_fetch(url, szotar);
    const siker = typeof res === 'object' && res !== null && 'uzenet' in res;
    return [res, siker];
}
