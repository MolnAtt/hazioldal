const csrftoken = getCookie('csrftoken');
document.addEventListener('keydown', tabkatt);

function tabkatt(event){
    let code = event.keyCode || event.which;
    if (code === 9) {
        if (event.target.dataset.melyik=='egyes')
            egyes_sulyanak_modositasa(event.target);
        else
            dolgozat_sulyvektoranak_modositasa(event.target);
    }
}

async function dolgozat_sulyvektoranak_modositasa(elem){
    let url = `${window.location.origin}/naplo/api/post/suly/write/${osztaly_name.value}/${elem.dataset.slug}/`;
    let szotar = { 
        'sorszam': elem.dataset.sorszam,
        'ertek':elem.value,
    };

    let res = await kuldo_fetch(url, szotar);
    console.log(res);
}