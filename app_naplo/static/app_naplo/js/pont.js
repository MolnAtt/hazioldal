const csrftoken = getCookie('csrftoken');

main();

function main(){
    document.addEventListener('keydown', tabkatt);
    ponthatargomb.addEventListener('click', ponthatarfrissites);
    szazalekrendezes();
    sulyvektor_kerekites();
}

function sulyvektor_kerekites(){
    for (let inputelem of document.querySelectorAll(".sulyinput")) {
        inputelem.value = parseFloat(inputelem.value);
    }
}

function szazalekrendezes(){
    for (const elem of document.querySelectorAll('.harmadikoszlop')) {
        if (elem.innerHTML!= '-' && elem.innerHTML!= ''){
            elem.innerHTML = `${Math.round(parseFloat(elem.innerHTML)*10000)/100}%`;
        }
    }
}


function tabkatt(event){
    let code = event.keyCode || event.which;
    if (code === 9) {
        if (event.target.classList.contains('pontinput')){
            pont_mentese(event.target);
        } else if (event.target.classList.contains('sulyinput')){
            suly_mentese(event.target);
        }
    }
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
        'suly': dolgozatsuly.value,
    };
    let res = await kuldo_fetch(url, szotar);
    console.log(res);
}

