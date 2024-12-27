const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);

function main(){
    ovatos_esemenykapcsolas('#update', 'click', update_hf);
    ovatos_esemenykapcsolas('#bead', 'click', create_mo);
    ovatos_esemenykapcsolas('#biral', 'click', create_biralat);
    ovatos_esemenykapcsolas('#mentorcopy', 'click', mentors2clipboard);
    ovatos_esemenykapcsolas('#mentoremailcopy', 'click', mentoremails2clipboard);
    ovatos_esemenykapcsolasok('.biralatot_torol', 'click', delete_biralat);
    // frissites();
}

function exists(elem){ return elem!=undefined; }

async function mentors2clipboard(){
    let szoveg = await get_mentors();
    navigator.clipboard.writeText(szoveg);
    alert("clipboardra kimásolva:\n" + szoveg);
}

async function mentoremails2clipboard(){
    let szoveg = await get_mentoremails();
    navigator.clipboard.writeText(szoveg);
    alert("clipboardra kimásolva:\n" + szoveg);
}


function torol(){}

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
    let url = `${window.location.origin}/${hazioldalurl()}/api/get/hf/read/${hfid()}/`;
    return await olvaso_fetch(url);
}

// UPDATE
async function update_hf(){
    let url = `${window.location.origin}/${hazioldalurl()}/api/post/hf/update/${hfid()}/`;
    let szotar = {
        'url': document.querySelector('#input_url').value,
    };
    let res = await kuldo_fetch(url, szotar);
    frissites();
    location.reload();
}


//////////////////////////////////////
// MENTORAL API

// READ
async function get_mentors(){
    let url = `${window.location.origin}/${hazioldalurl()}/api/get/mentoral/username/read/`;
    return await olvaso_fetch(url);
}

async function get_mentoremails(){
    let url = `${window.location.origin}/${hazioldalurl()}/api/get/mentoral/email/read/`;
    return await olvaso_fetch(url);
}


//////////////////////////////////////
// MO API

// CREATE
async function create_mo(){
    if (document.querySelector('#mo-editor-textarea').value.length>5){
        let url = `${window.location.origin}/${hazioldalurl()}/api/post/mo/create/hf/${hfid()}/`;
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
    let url = `${window.location.origin}/${hazioldalurl()}/api/post/biralat/create/hf/${hfid()}/`;
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
        let bid = e.currentTarget.getAttribute('data-id');
        let url = `${window.location.origin}/${hazioldalurl()}/api/delete/biralat/${bid}/`;
        let res = await torlo_fetch(url);
        location.reload();
    }
}

function szinezes(){
    if (exists($('#bi-itelet-select')[0])) {
        if ($('#bi-itelet-select')[0].value == "Hiányos")
            $('#bi-itelet-select').css('color','rgb(253 208 74)');
        if ($('#bi-itelet-select')[0].value == "Elfogadva")
            $('#bi-itelet-select').css('color','#0bc30b');
        if ($('#bi-itelet-select')[0].value == "Értékelhetetlen")
            $('#bi-itelet-select').css('color','rgb(255 68 68)');
        if ($('#bi-itelet-select')[0].value == "Hibás")
            $('#bi-itelet-select').css('color','rgb(253 208 74)');
    }
}

function betolt(){
    spanszin();
    updateScroll();
    alignButton();
    if (exists($('.separator')[1]))
    { 
        var height = screen.height - $('header')[0].offsetHeight - $('.forumcim')[0].offsetHeight - $('.separator')[0].offsetHeight - $('.repo-doboz')[0].offsetHeight -$('.separator')[1].offsetHeight -170;

        // Telefonon
        if (screen.width<=940)
        {
            if ($('#uzenet')[0].offsetHeight <5)
            {
                $('.dobozok')[0].style.height =height-50+"px";
            }
            else{
                $('.dobozok')[0].style.height =height-30+"px";
            }
            return;
        }
        if ($('#uzenet')[0].offsetHeight <5)
        {
            $('.dobozok')[0].style.height =height/2+90+"px";
            return;
        }
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
    if (exists(element))
    {
        var elementHeight = element.scrollHeight;
        element.scrollTop = elementHeight;
    }
}
function alignButton(){
    if (exists($('.bi-torol')[0]))
    {
        var elem = $('.bi-torol')[0].parentElement.children[0];
        var height = elem.children[0].offsetHeight + elem.children[1].offsetHeight + elem.children[2].offsetHeight + 26 - 6;
        $('.bi-torol')[0].style.height = height+"px";
    }

}

// ujhf

document.querySelectorAll('.retract-details-landscape').forEach(button => {
    button.addEventListener('click', () => {
        document.querySelector('.hf-details').classList.toggle('retracted');
    });
});


szinezes();