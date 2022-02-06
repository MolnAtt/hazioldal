const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    ovatos_esemenykapcsolas('vagolap', 'click', vagolapra);
    ovatos_esemenykapcsolas('create', 'click', create_repo);
    ovatos_esemenykapcsolas('update', 'click', update_repo);
    // ovatos_esemenykapcsolas('delete', 'click', delete_repo);
    if (repoid().value=="") {
        rejteskapcsolas(['vagolap', 'githublink', 'update', 'delete']);
    } else {
        rejteskapcsolas(['create']);
        repolink_frissitese();
    }
}

///////////////////////////////
// DOM-kezelés

function rejteskapcsolas(lista){
    for (const iterator of lista) {
        document.getElementById(iterator).classList.toggle("rejtett");
    }
}

function ovatos_esemenykapcsolas(idstr, eventstr, func){
    let elem = document.getElementById(idstr)
    if (elem!=null){
        elem.addEventListener(eventstr, func);
    }
}

function hfid()  { return document.getElementsByName('hfid')[0]; }
function repoid()  { return document.getElementsByName('repoid')[0]; }
function repourl() { return document.getElementsByName('repo_url')[0]; }

/////////////////////////////////
// Eseménykezelés

function vagolapra(){
    let copyText = document.getElementsByName('repo_url')[0];
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
}

async function repolink_frissitese(){
    szotar = await get_repo(repoid().value);
    repo_url = szotar['repo_url']
    repo_id = szotar['repo_id']
    repourl().value = repo_url;
    document.getElementById('githublink').setAttribute("href", repo_url);
    document.getElementById('bead').setAttribute("href", `http://127.0.0.1:8000/hf/repo/${repo_id}/mo/`);
}

//////////////////////////////////////
// API

// CREATE
async function create_repo(){
    let res = await create_repo_by({
        'url':repourl().value,
    }, hfid().value);
    repoid().value = res['repoid'];
    repolink_frissitese();
    rejteskapcsolas(['create', 'vagolap', 'githublink', 'update', 'delete']);
}


async function create_repo_by(szotar, hfid){
    let url = `http://127.0.0.1:8000/api/post/repo/create/${hfid}/`;
    let res = await kuldo_fetch(url, szotar);
    return res;
}


// READ
async function get_repo(id){
    let url = `http://127.0.0.1:8000/api/get/repo/get/${id}/`;
    return json_promise = await olvaso_fetch(url);
}


// UPDATE
async function update_repo(){
    let res = await modositsd_ezt_igy(repoid().value, {'repo_url': repourl().value});
    repolink_frissitese();
}

async function modositsd_ezt_igy(id, igy = {'szoveg':'ezt feccsel hoztam létre'}){
    let url = `http://127.0.0.1:8000/api/post/repo/update/${id}/`;
    let res = await kuldo_fetch(url, igy);
    return res;
}

// DELETE

async function delete_repo(){
    torold_ezt(repoid().value);
}

function torold_ezt(id){ 
    let url = `http://127.0.0.1:8000/api/delete/repo/delete/${id}/`;
    torlo_fetch(url);
}

// Fetchek

async function olvaso_fetch(url){
    const response = await fetch(url);
    const json_promise = await response.json();
    return json_promise;
}


async function kuldo_fetch(url, szotar){
//    console.log(`${url} --> `);
//    console.log(szotar)
    const response = await fetch(url, {
        method:'POST',
        headers:{
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify(szotar)
    }
    );
    const json_promise = await response.json();
    return json_promise;
}

function torlo_fetch(url){
    fetch(url, { 
        method:'DELETE',
        headers:{
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken,
        }
     }); 
}

// csrf-token miatt kell!
// forrás: https://docs.djangoproject.com/en/3.2/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
