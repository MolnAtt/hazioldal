const csrftoken = getCookie('csrftoken');

main();

function main(){
    document.addEventListener('keydown', billentyukezelo);
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



function valtoztatas_mentese(e){
    if (e.classList.contains('pontinput')){
        pont_mentese(e);
    } else if (e.classList.contains('sulyinput')){
        suly_mentese(e);
    }

}

function szomszed_kijelolese(o,irany){
    let parent_td = o.parentElement;
    switch (irany) {
        case 'jobbra':
            if (o.parentElement.nextElementSibling){
                console.log(o.parentElement.nextElementSibling.firstElementChild);
                o.parentElement.nextElementSibling.firstElementChild.select();
            }
            break;
        case 'balra':
            if (o.parentElement.previousElementSibling){ 
                console.log(o.parentElement.previousElementSibling.firstElementChild);
                o.parentElement.previousElementSibling.firstElementChild.select();
            }
            break;
        case 'le':
            let i = Array.from(parent_td.parentElement.children).indexOf(parent_td);
            console.log(i);
            if (parent_td.nextElementSibling){
                console.log(parent_td.nextElementSibling.children[i].firstElementChild);
                parent_td.nextElementSibling.children[i].firstElementChild.select();
            }
            break;
        case 'fel':
            let j = Array.from(parent_td.parentElement.children).indexOf(parent_td);
            if (parent_td.previousElementSibling){
                console.log(parent_td.previousElementSibling.children[i].firstElementChild);
                parent_td.previousElementSibling.children[i].firstElementChild.select();
            }
            break;
    }
}

function billentyukezelo(e){
    console.log(e.key);
    switch (e.key) {
        case 'Tab':
            valtoztatas_mentese(e.target);
            break;
        case 'Enter':
        case 'ArrowDown':
            valtoztatas_mentese(e.target);
            szomszed_kijelolese(e.target, 'le');
            console.log('lemozog');
            break;
        case 'ArrowUp':
            valtoztatas_mentese(e.target);
            szomszed_kijelolese(e.target, 'fel');
            console.log('felmozog');
            break;
        case 'ArrowRight':
            valtoztatas_mentese(e.target);
            szomszed_kijelolese(e.target, 'jobbra');
            console.log('jobbra mozog');
            break;
        case 'ArrowLeft':
            valtoztatas_mentese(e.target);
            szomszed_kijelolese(e.target, 'balra');
            console.log('balra mozog');
            break;
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
        'dolgozatsuly': dolgozatsuly.value,
    };
    let res = await kuldo_fetch(url, szotar);
    console.log(res);
}

