document.addEventListener('keydown', tabkatt);

function tabkatt(event){
    let code = event.keyCode || event.which;
    if (code === 9) {
        if (event.target.classList.contains('jegy')){
            jegy_lezaras_mentese(event.target);
        } else if (event.target.classList.contains('szoveg')){
            szoveges_ertekeles_mentese(event.target);
        }
    }
}


async function jegy_lezaras_mentese(elem){
    let url = `${window.location.origin}/naplo/api/post/lezaras/write/jegy/${osztaly_name.value}/`;
    let szotar = { 
        'sorszam': elem.dataset.sorszam,
        'ertek':elem.value,
    };
    console.log("ezt küldöm:")
    console.log(szotar)
    let res = await kuldo_fetch(url, szotar);
    console.log(res);
}


async function szoveges_ertekeles_mentese(elem){
    let url = `${window.location.origin}/naplo/api/post/lezaras/write/szoveg/${osztaly_name.value}/`;
    let szotar = { 
        'sorszam': elem.dataset.sorszam,
        'ertek':elem.value,
    };
    console.log("ezt küldöm:")
    console.log(szotar)
    let res = await kuldo_fetch(url, szotar);
    console.log(res);
}

