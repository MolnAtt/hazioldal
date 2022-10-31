const csrftoken = getCookie('csrftoken');
main()

function main(){
    document.querySelector('#create_user').addEventListener('click', create_user);
}


////////////////////////////////
// USER API

async function create_user(){
    alert("küldöm");
    let url = `${window.location.origin}/naplo/api/post/user/create/`;
    let szotar = {
        'szoveg':document.querySelector('#input').value,
    };
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}
