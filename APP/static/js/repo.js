const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    esemenykapcsolas('update', 'click', update_repo);
    repolink_frissitese();
}

//////////////////////////////////////
// DOM-kezelés

function esemenykapcsolas(idstr, eventstr, func){document.getElementById(idstr).addEventListener(eventstr, func);}
function hfid()  { return document.getElementsByName('hfid')[0]; }
function repoid()  { return document.getElementsByName('repoid')[0]; }
function repourl() { return document.getElementsByName('repo_url')[0]; }

async function repolink_frissitese(){
    szotar = await get_repo(repoid().value);
    document.getElementById('githublink').setAttribute("href", szotar['repo_url']);
}

//////////////////////////////////////
// API

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

async function modositsd_ezt_igy(id, igy){
    let url = `http://127.0.0.1:8000/api/post/repo/update/${id}/`;
    let res = await kuldo_fetch(url, igy);
    return res;
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
