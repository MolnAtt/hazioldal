const csrftoken = getCookie('csrftoken');

main();

function main(){
    document.addEventListener('keydown', billentyukezelo);
    ponthatargomb.addEventListener('click', ponthatarfrissites);
    sulyvektor_kerekites();
}

function sulyvektor_kerekites(){
    for (let inputelem of document.querySelectorAll(".sulyinput")) {
        inputelem.value = parseFloat(inputelem.value);
    }
}

function valtoztatas_mentese(e){
    if (e.classList.contains('pontinput')){
        pont_mentese(e);
    } else if (e.classList.contains('sulyinput')){
        suly_mentese(e);
    }

}

function oszlopindex(td){
    return Array.from(td.parentElement.children).indexOf(td);
}

function szomszed_kijelolese(td,billentyu){
    switch (billentyu) {
        case 'ArrowRight':
            if (td.nextElementSibling){
                td.nextElementSibling.firstElementChild.select();
            }
            break;
        case 'ArrowLeft':
            if (td.previousElementSibling){ 
                td.previousElementSibling.firstElementChild.select();
            }
            break;
        case 'Enter':
        case 'ArrowDown':
            if (!td.parentElement.nextElementSibling.classList.contains('feladatmaximumok')){
                td.parentElement.nextElementSibling.children[oszlopindex(td)].firstElementChild.select();
            }
            break;
        case 'ArrowUp':
            if (!td.parentElement.previousElementSibling.classList.contains('feladatnevek')){
                td.parentElement.previousElementSibling.children[oszlopindex(td)].firstElementChild.select();
            }
            break;
        case 'Home':
            td.parentElement.children[5].firstElementChild.select();
            break;
        case 'End':
            td.parentElement.lastElementChild.firstElementChild.select();
            break;
    }
}

function billentyukezelo(e){
    if (['Tab', 'Enter', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
        valtoztatas_mentese(e.target);
    }
    szomszed_kijelolese(e.target.parentElement, e.key);
}

////////////////////////////////
// PONT API

async function pont_mentese(elem){
    let url = `${window.location.origin}/naplo/api/post/pont/write/${osztaly_name.value}/${dolgozat_slug.value}/`;
    let szotar = { 
        'i_tanulo': elem.dataset.tanulo,
        'j_feladat': elem.dataset.feladat,
        'ertek':elem.value,
    };
    let res = await kuldo_fetch(url, szotar);
    console.log(res);
}


////////////////////////////////
// SÚLY API


async function suly_mentese(elem){
    let url = `${window.location.origin}/naplo/api/post/suly/write/${osztaly_name.value}/${dolgozat_slug.value}/`;
    let szotar = { 
        'sorszam': elem.dataset.sorszam,
        'ertek':elem.value,
    };

    let res = await kuldo_fetch(url, szotar);
    console.log(res);
}


////////////////////////////////
// DÁTUM API

const HONAPNEVEK = ['január', 'február', 'március', 'április', 'május', 'június', 'július', 'augusztus', 'szeptember', 'október', 'november', 'december'];

async function datum_mentese(elem){
    const allapot = document.getElementById('datumallapot');
    if (!elem.value) return;
    let url = `${window.location.origin}/naplo/api/post/datum/write/${osztaly_name.value}/${dolgozat_slug.value}/`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {'Content-type': 'application/json', 'X-CSRFToken': csrftoken},
            body: JSON.stringify({'datum': elem.value}),
        });
        if (!response.ok) throw new Error(await response.text());
        const [ev, honap, nap] = elem.value.split('-').map(Number);
        document.getElementById('datumszoveg').textContent = `${ev}. ${HONAPNEVEK[honap - 1]} ${nap}.`;
        allapot.textContent = 'Mentve.';
    } catch (error) {
        console.error('A dátum mentése sikertelen:', error);
        allapot.textContent = 'A dátum mentése sikertelen.';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const datumelem = document.getElementById('dolgozatdatum');
    if (datumelem) datumelem.addEventListener('change', () => datum_mentese(datumelem));
});

////////////////////////////////
// PONTHATÁR API

async function ponthatarfrissites(elem){

    let url = `${window.location.origin}/naplo/api/post/ponthatar/write/${osztaly_name.value}/${dolgozat_slug.value}/`;
    let szotar = { 
        '2': ponthatar_2.value,
        '3': ponthatar_3.value,
        '4': ponthatar_4.value,
        '5': ponthatar_5.value,
        '12': ponthatar_12.value,
        '23': ponthatar_23.value,
        '34': ponthatar_34.value,
        '45': ponthatar_45.value,
        '55': ponthatar_55.value,
        'dolgozatsuly': dolgozatsuly.value,
    };
    let res = await kuldo_fetch(url, szotar);
    console.log(res);
}
