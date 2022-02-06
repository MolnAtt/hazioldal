const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    console.log("betöltött a DOM");
    let copy_gomb = document.getElementById('vagolap');
    let update_gomb = document.getElementById('update');
    let delete_gomb = document.getElementById('delete');
    copy_gomb.addEventListener('click', vagolapra);
    update_gomb.addEventListener('click', update_repo);
    delete_gomb.addEventListener('click', delete_repo);
    repolink_frissitese();
}

function vagolapra(){
    let copyText = document.getElementsByName('repo_url')[0];
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
}

async function repolink_frissitese(){
    szotar = await get_repo(repoid());
    repo_url = szotar['repo_url']
    console.log(repo_url);
    document.getElementsByName('repo_url')[0].value = repo_url;
    document.getElementById('githublink').setAttribute("href", repo_url);
}

// READ THIS
async function get_repo(id){
    let url = `http://127.0.0.1:8000/api/get/repo/get/${id}/`;
    const response = await fetch(url);
    const json_promise = await response.json();
    return json_promise;
}

async function update_repo(){
    let res = await modositsd_ezt_igy(repoid(), {'repo_url': repourl()});
    repolink_frissitese();
}

function repoid(){
    return document.getElementsByName('repoid')[0].value;
}

function repourl(){
    return document.getElementsByName('repo_url')[0].value;
}

async function delete_repo(){
    torold_ezt(repoid());
}

// UPDATE
async function modositsd_ezt_igy(id, igy = {'szoveg':'ezt feccsel hoztam létre'}){
    let url = `http://127.0.0.1:8000/api/post/repo/update/${id}/`;
    console.log("van itt egyaltalan valami?")
    console.log(igy);
    let res = await kuld(url, igy);
    return res;
}

// DELETE
function torold_ezt(id){ 
    let url = `http://127.0.0.1:8000/api/delete/repo/delete/${id}/`;
    torlo_fetch(url);
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

// POST
async function kuld(url, szotar){
    console.log(`${url} --> `);
    console.log(szotar)
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
