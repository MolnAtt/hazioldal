const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    ovatos_esemenykapcsolas('#aktivizalas', 'click', update_active);
    ovatos_esemenykapcsolas('#passzivizalas', 'click', update_active);
    ovatos_esemenykapcsolas('#gitprofiles', 'click', create_git);
    ovatos_esemenykapcsolas('#osztalymentoralas', 'click', update_mentoral_tanar);
    ovatos_esemenykapcsolas('#mentoramnesztia', 'click', mentoramnesztia);
    ovatos_esemenykapcsolas('#hfamnesztia', 'click', hfamnesztia);
}



//////////////////////////////////////
// UPDATE MENTORAL

async function update_mentoral_tanar(e){
    let url = `${window.location.origin}/api/post/mentoral/create/tanar/`;
    let szotar = { 'csoport': document.querySelector('#groupselect').value };
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}

//////////////////////////////////////
// GIT API

async function create_git(e){
    let url = `${window.location.origin}/api/post/git/create/all/`;
    let szotar = {};
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}


// UPDATE: ACTIVITY
async function update_active(e){
    let url = `${window.location.origin}/api/post/user/update/activity/`;
    let szotar = {'active': e.target.id=="aktivizalas"};
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}

async function mentoramnesztia(e){
    let url = `${window.location.origin}/api/post/amnesztia/mentor/`;
    let szotar = {};
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}

async function hfamnesztia(e){
    let url = `${window.location.origin}/api/post/amnesztia/hf/`;
    let szotar = {};
    let res = await kuldo_fetch(url, szotar);
    alert(res);
}

