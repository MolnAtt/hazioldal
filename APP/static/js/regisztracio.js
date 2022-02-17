const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    document.getElementById('create_user').addEventListener('click', create_user);
    document.getElementById('create_mentoral').addEventListener('click', create_mentoral);
}


////////////////////////////////
// USER API

async function create_user(){
    let url = `http://127.0.0.1:8000/api/post/user/create/`;
    let szotar = {
        'szoveg':document.getElementById('tabla').value,
    };
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}


////////////////////////////////
// MENTORAL API

async function create_mentoral(){
    let url = `http://127.0.0.1:8000/api/post/mentoral/create/`;
    let szotar = {
        'szoveg':document.getElementById('tabla').value,
    };
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}


