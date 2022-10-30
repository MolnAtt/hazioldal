const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    document.querySelector('#create_user').addEventListener('click', create_user);
    document.querySelector('#create_mentoral').addEventListener('click', create_mentoral);
}


////////////////////////////////
// USER API

async function create_user(){
    let url = `${window.location.origin}/api/post/user/create/`;
    let szotar = {
        'szoveg':document.querySelector('#tabla').value,
    };
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}


////////////////////////////////
// MENTORAL API

async function create_mentoral(){
    let url = `${window.location.origin}/api/post/mentoral/create/tsv/`;
    let szotar = {
        'szoveg':document.querySelector('#tabla').value,
    };
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}


