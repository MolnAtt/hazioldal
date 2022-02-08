const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    esemenykapcsolas('create', 'click', create_repo);
}

//////////////////////////////////////
// DOM-kezelés

function esemenykapcsolas(idstr, eventstr, func) {document.getElementById(idstr).addEventListener(eventstr, func);}
function hfid()  { return document.getElementsByName('hfid')[0]; }
function repourl() { return document.getElementsByName('repo_url')[0]; }

//////////////////////////////////////
// API

// CREATE
async function create_repo(){
    let res = await create_repo_by({'url':repourl().value,}, hfid().value);
    location.replace(`http://127.0.0.1:8000/repo/${res['repoid']}/`)
}

async function create_repo_by(szotar, hfid){
    let url = `http://127.0.0.1:8000/api/post/repo/create/${hfid}/`;
    let res = await kuldo_fetch(url, szotar);
    return res;
}

// Fetchek

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

///////////////////////////////////////////////////////////
// csrf-token
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
