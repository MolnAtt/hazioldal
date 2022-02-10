const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    console.log("betöltött a DOM");
    let creategomb = document.getElementById('creategomb');
    creategomb.addEventListener('click', mennyi_bigyo);
    ujgomb.addEventListener('click', gombos_uj_bigyo);
}

async function mennyi_bigyo(e){
    adatok = await kerem_mindet();
    console.log(adatok);
    alert(`Ennyi bigyó van: ${adatok.length} db`);
}


function gombos_uj_bigyo(e){ uj_bigyo(); }

// CREATE
function uj_bigyo(igy={'szoveg':'ezt feccsel hoztam létre'}){
    let url = 'http://127.0.0.1:8000/api/post/create/';
    kuld(url, igy);
}

// READ ALL

async function kerem_mindet(){
    const url = 'http://127.0.0.1:8000/api/get/model-object/all/';
    // await-ekkel
    const response = await fetch(url);
    const json_promise = await response.json();
    return json_promise;
}


// READ THIS
async function kerem_ezt(id){
    let url = `http://127.0.0.1:8000/api/get/model-object/this/${id}`;
    let result = null;
    // .then-ekkel
    fetch(url)
    .then((resp) => resp.json())
    .then((data) => {result = data;});
    return await result;
}

// UPDATE
function modositsd_ezt(id, igy = {'szoveg':'ezt feccsel hoztam létre'}){
    let url = `http://127.0.0.1:8000/api/post/update/${id}/`;
    kuld(url, igy);
}

// DELETE
function torold_ezt(id){ 
    let url = `http://127.0.0.1:8000/api/delete/${id}`;
    fetch(url, { method:'DELETE' }); 
}

// POST
function kuld(url,szotar){
    console.log(`${url} --> `);
    console.log(szotar)
    fetch(url, {
        method:'POST',
        headers:{
        headers:{
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify(szotar)
    }
    );
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
