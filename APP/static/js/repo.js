const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    esemenykapcsolas('update', 'click', update_repo);
    ovatos_esemenykapcsolas('bead', 'click', create_mo);
    ovatos_esemenykapcsolas('biral', 'click', create_biralat);
    repolink_frissitese();
}

//////////////////////////////////////
// DOM-kezelés

function esemenykapcsolas(idstr, eventstr, func){ document.getElementById(idstr).addEventListener(eventstr, func); }
function ovatos_esemenykapcsolas(idstr, eventstr, func){ 
    let elem = document.getElementById(idstr);
    if (elem!=null){
        elem.addEventListener(eventstr, func); 
    }
}
function hfid()  { return document.getElementsByName('hfid')[0]; }
function repoid()  { return document.getElementsByName('repoid')[0]; }
function repourl() { return document.getElementsByName('repo_url')[0]; }

async function repolink_frissitese(){
    szotar = await get_repo(repoid().value);
    document.getElementById('githublink').setAttribute("href", szotar['repo_url']);
}


//////////////////////////////////////
// MO API

// CREATE
async function create_mo(){
    let rid = repoid().value;
    let url = `http://127.0.0.1:8000/api/post/mo/create/repo/${rid}/`;
    let szotar = {
        'szoveg':document.getElementById('mo-editor-textarea').value,
    };
    let res = await kuldo_fetch(url, szotar);
    location.replace(`http://127.0.0.1:8000/repo/${rid}/`);
}


//////////////////////////////////////
// REPO API

// READ
async function get_repo(id){
    let url = `http://127.0.0.1:8000/api/get/repo/get/${id}/`;
    return json_promise = await olvaso_fetch(url);
}

// UPDATE
async function update_repo(){
    let url = `http://127.0.0.1:8000/api/post/repo/update/${repoid().value}/`;
    let szotar = {
        'repo_url': repourl().value,
    };
    let res = await kuldo_fetch(url, szotar);
    repolink_frissitese();
}

//////////////////////////////////////
// BIRALAT API

// CREATE
async function create_biralat(){
    let rid = repoid().value;
    let url = `http://127.0.0.1:8000/api/post/biralat/create/repo/${rid}/`;
    let szotar = {
        'szoveg' : document.getElementById('bi-editor-textarea').value, 
        'itelet' : document.getElementById('bi-itelet-select').value,
    };
    let res = await kuldo_fetch(url, szotar);
    location.replace(`http://127.0.0.1:8000/repo/${rid}/`);
}



//////////////////////////////////////
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

// csrf-token miatt kell!
// forrás: https://docs.djangoproject.com/en/3.2/ref/csrf/
function getCookie(name) {
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return null;
}
