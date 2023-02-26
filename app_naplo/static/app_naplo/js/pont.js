const csrftoken = getCookie('csrftoken');

let osztay_name = ""
let dolgozat_slug = "";

main();

function main(){
    document.addEventListener('keydown', tabkatt);
    // let osztalyinput = document.querySelector('#osztaly_name');
    // osztaly_name.value;
    // let dolgozatinput = document.querySelector('#dolgozat_slug');
    // dolgozat_slug.value;
}

function tabkatt(event){
    let code = event.keyCode || event.which;
    if (code === 9 && event.target.classList.contains('pontinput')) {
        pont_mentese(event.target);
    }
}

////////////////////////////////
// PONT API

async function pont_mentese(elem){
    let par = elem.id.split("-");
    let i_tanulo = par[0];
    let j_feladat = par[1];

    let url = `${window.location.origin}/naplo/api/post/pont/write/${osztaly_name.value}/${dolgozat_slug.value}/`;
    let szotar = { 
        'i_tanulo': i_tanulo,
        'j_feladat': j_feladat,
        'ertek':elem.value,
    };
    let res = await kuldo_fetch(url, szotar);
    console.log(res);
}


////////////////////////////////
// PONT API

async function pont_mentese(elem){
    let par = elem.id.split("-");
    let i_tanulo = par[0];
    let j_feladat = par[1];

    let url = `${window.location.origin}/naplo/api/post/pont/write/${osztaly_name.value}/${dolgozat_slug.value}/`;
    let szotar = { 
        'i_tanulo': i_tanulo,
        'j_feladat': j_feladat,
        'ertek':elem.value,
    };
    let res = await kuldo_fetch(url, szotar);
    console.log(res);
}

