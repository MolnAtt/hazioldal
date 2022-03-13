const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    ovatos_esemenykapcsolas('#update', 'click', update_git);
}

//////////////////////////////////////
// GIT API

// UPDATE
async function update_git(){
    let url = `${window.location.origin}/api/post/git/update/`;
    let szotar = {
        'username':document.querySelector('#gitusername').value,       
    };
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}

