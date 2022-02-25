const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    ovatos_esemenykapcsolas('#update', 'click', update_hf);
    ovatos_esemenykapcsolas('#bead', 'click', create_mo);
    ovatos_esemenykapcsolas('#biral', 'click', create_biralat);
    ovatos_esemenykapcsolasok('.biralatot_torol', 'click', delete_biralat);
    frissites();
}

//////////////////////////////////////
// DOM-kezelés


async function frissites(){
    let a_hf = await get_hf(hfid());
    document.querySelector('#githublink').setAttribute("href", a_hf.url);
}


function hfid(){ return window.location.href.split("/").at(-2); }

//////////////////////////////////////
// HF API

// READ
async function get_hf(){
    let url = `${window.location.origin}/api/get/hf/read/${hfid()}/`;
    return await olvaso_fetch(url);
}

// UPDATE
async function update_hf(){
    let url = `${window.location.origin}/api/post/hf/update/${hfid()}/`;
    let szotar = {
        'url': document.querySelector('#input_url').value,
    };
    let res = await kuldo_fetch(url, szotar);
    frissites();
}


//////////////////////////////////////
// MO API

// CREATE
async function create_mo(){
    let url = `${window.location.origin}/api/post/mo/create/hf/${hfid()}/`;
    let szotar = {
        'szoveg':document.querySelector('#mo-editor-textarea').value,
    };
    let res = await kuldo_fetch(url, szotar);
    location.reload();
}

//////////////////////////////////////
// BIRALAT API

// CREATE
async function create_biralat(){
    let url = `${window.location.origin}/api/post/biralat/create/hf/${hfid()}/`;
    let szotar = {
        'szoveg' : document.querySelector('#bi-editor-textarea').value, 
        'itelet' : document.querySelector('#bi-itelet-select').value,
    };
    let res = await kuldo_fetch(url, szotar);
    location.reload();
}

// DELETE
async function delete_biralat(e){
    if (confirm("Biztos, hogy törlöd ezt a bírálatot?")) 
    {
        let bid = e.target.value;
        let url = `${window.location.origin}/api/delete/biralat/${bid}/`;
        let res = await torlo_fetch(url);
        location.reload();
    }
}

