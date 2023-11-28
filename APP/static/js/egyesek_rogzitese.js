egyesek_rogzitese.addEventListener("click", click_egyesek_rogzitese);

async function click_egyesek_rogzitese(e){
    let csoportnev = csoport.dataset.csoportnev;
    let elozetes_visszajelzes_szovege = await biztos_e(csoportnev);
    if (confirm(elozetes_visszajelzes_szovege)){
        alert(await send_egyesek_rogzitese(csoportnev));
    }
}

async function biztos_e(csoportnev){
    let url = `${window.location.origin}/${hazioldalurl()}/api/get/egyes/${csoportnev}/mennyilenne/`;
    let szotar = await olvaso_fetch(url);
    console.log(szotar.szoveg);
    return 'Ezek a házik kapnának egyest (teljes lista a konzolon): \n -----------------\n' + szotar.szoveg + '\n-----------------\nBiztos, hogy beírjunk mindegyikre egy egyest?';
}

async function send_egyesek_rogzitese(csoportnev){
    let url = `${window.location.origin}/${hazioldalurl()}/api/post/egyes/${csoportnev}/create/`;
    let szotar = await kuldo_fetch(url,{});
    console.log(szotar.szoveg);
    return 'A következő házik kaptak most egyest (teljes lista a konzolon): \n -----------------\n' + szotar.szoveg;
}


