const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    ovatos_esemenykapcsolas('#update', 'click', update_hf);
    ovatos_esemenykapcsolas('#bead', 'click', create_mo);
    ovatos_esemenykapcsolas('#biral', 'click', create_biralat);
    ovatos_esemenykapcsolasok('.biralatot_torol', 'click', delete_biralat);
    frissites();
}

function torol(){
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
    location.reload();
}


//////////////////////////////////////
// MO API

// CREATE
async function create_mo(){
    if (document.querySelector('#mo-editor-textarea').value.length>5){
        let url = `${window.location.origin}/api/post/mo/create/hf/${hfid()}/`;
        let szotar = {
            'szoveg':document.querySelector('#mo-editor-textarea').value,
        };
        let res = await kuldo_fetch(url, szotar);
        location.reload();
    }
    else
        alert('Az üzenethez nem írtál semmit, vagy túl rövid!')
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

function szinezes(){
    if ($('#bi-itelet-select')[0].value == "Hiányos")
        $('#bi-itelet-select').css('color','rgb(253 208 74)');
    if ($('#bi-itelet-select')[0].value == "Elfogadva")
        $('#bi-itelet-select').css('color','#0bc30b');
    if ($('#bi-itelet-select')[0].value == "Értékelhetetlen")
        $('#bi-itelet-select').css('color','rgb(255 68 68)');
    if ($('#bi-itelet-select')[0].value == "Hibás")
        $('#bi-itelet-select').css('color','rgb(253 208 74)');
}

function betolt(){
    spanszin();
    updateScroll();
    var setThis = $('.dobozok')[0].offsetHeight; 
    var height = screen.height - $('header')[0].offsetHeight - $('.forumcim')[0].offsetHeight - $('.separator')[0].offsetHeight - $('.repo-doboz')[0].offsetHeight -$('.separator')[1].offsetHeight -170;

    $('.dobozok')[0].style.height =height+"px";
    if (screen.height>940)
    {
        $('.dobozok')[0].style.height =height/2+50+"px";
    }
}

function spanszin(){

    for (var i =0; i<$('.itelet').length;i++)
    {
        if ($('.itelet')[i].innerText == "Értékelhetetlen")
            $('.itelet')[i].style.color ="rgb(255 68 68)"
        if ($('.itelet')[i].innerText == "Hiányos" || $('.itelet')[i].innerText == "Hibás")
            $('.itelet')[i].style.color ="rgb(253 208 74)"
        if ($('.itelet')[i].innerText == "Elfogadva")
            $('.itelet')[i].style.color ="#0bc30b"

    }

}
function updateScroll() {
    var element = $('.dobozok')[0];
    var elementHeight = element.scrollHeight;
    element.scrollTop = elementHeight;
}

