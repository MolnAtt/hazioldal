const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    ovatos_esemenykapcsolas('#kituz', 'click', create_kituzes);
    ovatos_esemenykapcsolas('#tema', 'change', frissites_feladat);
    ovatos_esemenykapcsolas("#temaadd", 'click', create_temakor);
    ovatos_esemenykapcsolas("#feladatadd", 'click', create_feladat);

}

//////////////////////////////////////
// DOM-kezelés

async function frissites_feladat(){
    let a_feladat_select = document.querySelector('#feladat');
    a_feladat_select.innerHTML = "<option selected disabled hidden>Válassz feladatot!</option>";
    
    let a_tema_select = document.querySelector('#tema');
    let a_feladatok = await read_tema_feladatai(a_tema_select.value);
    for (const a_feladat of a_feladatok) {
        let option = document.createElement('option');
        option.innerHTML = a_feladat.nev;
        option.value = a_feladat.id;
        a_feladat_select.appendChild(option);
    }
}


//////////////////////////////////////
// TEMA API

// READ
async function read_tema_feladatai(temaid){
    let url = `${window.location.origin}/${hazioldalurl()}/api/get/feladat/read/tema/${temaid}/`;
    return await olvaso_fetch(url);
}



//////////////////////////////////////
// KITUZES API

// CREATE
async function create_kituzes(){
    let url = `${window.location.origin}/${hazioldalurl()}/api/post/kituzes/create/`;
    let szotar = {
        'temaid':document.querySelector('#tema').value,
        'feladatid':document.querySelector('#feladat').value,
        'csoportid':document.querySelector('#csoport').value,
        'hatarido':document.querySelector('#hatarido').value,
    };
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}

async function create_temakor(){
    let url = `${window.location.origin}/${hazioldalurl()}/api/post/temakor/create/`;
    let szotar = {
        'nev':document.querySelector('#ujtema').value,
        'sorrend':document.querySelector('#ujtemaorder').value,
    };
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}

async function create_feladat(){
    let url = `${window.location.origin}/${hazioldalurl()}/api/post/feladat/create/`;
    let szotar = {
        'nev':ujfeladat.value,
        'url':ujfeladatURL.value,
        'temaid':ujfeladattemakore.value,
    };
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}