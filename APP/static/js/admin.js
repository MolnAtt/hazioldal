const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    ovatos_esemenykapcsolas('#aktivizalas', 'click', update_active);
    ovatos_esemenykapcsolas('#passzivizalas', 'click', update_active);
    ovatos_esemenykapcsolas('#gitprofiles', 'click', create_git);
    ovatos_esemenykapcsolas('#osztalymentoralas', 'click', update_mentoral_tanar);
    ovatos_esemenykapcsolas('#hfamnesztia', 'click', amnesztia);
}



//////////////////////////////////////
// UPDATE MENTORAL

async function update_mentoral_tanar(e){
    let url = `${window.location.origin}/${hazioldalurl()}/api/post/mentoral/create/tanar/`;
    let szotar = { 'csoport': document.querySelector('#groupselect').value };
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}

//////////////////////////////////////
// GIT API

async function create_git(e){
    let url = `${window.location.origin}/${hazioldalurl()}/api/post/git/create/all/`;
    let szotar = {};
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}


// CREATE: AMNESZTIA
async function amnesztia(e){
    let url = `${window.location.origin}/${hazioldalurl()}/api/post/amnesztia/`;
    let szotar = {};
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}


// UPDATE: ACTIVITY
async function update_active(e){
    let url = `${window.location.origin}/${hazioldalurl()}/api/post/user/update/activity/`;
    let szotar = {'active': e.target.id=="aktivizalas"};
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}