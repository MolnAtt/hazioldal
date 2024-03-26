const csrftoken = getCookie('csrftoken');

ovatos_esemenykapcsolas('#mentoralt', 'change', frissites_feladat);
ovatos_esemenykapcsolas('#feladat', 'change', frissites_biralat);

mentoralt.value = -1;
biralat.value = -1;

//////////////////////////////////////
// DOM-kezelés

async function frissites_feladat(){
    feladat.innerHTML = "<option selected disabled hidden>Válassz feladatot!</option>";
    
    let a_feladatok = await read_mentoralt_feladatai(mentoralt.value);
    for (const a_feladat of a_feladatok) {
        let option = document.createElement('option');
        option.innerHTML = a_feladat.nev;
        option.value = a_feladat.id;
        feladat.appendChild(option);
    }
}

async function frissites_biralat(){
    biralat.innerHTML = "<option selected disabled hidden>Válassz bírálatot!</option>";
    
    let a_biralatok = await read_feladat_biralatai(mentoralt.value, feladat.value);
    for (const a_biralat of a_biralatok) {
        let option = document.createElement('option');
        option.innerHTML = a_biralat.nev;
        option.value = a_biralat.id;
        biralat.appendChild(option);
    }
}


//////////////////////////////////////
// TEMA API

// READ
async function read_mentoralt_feladatai(mentoraltid){
    let url = `${window.location.origin}/${hazioldalurl()}/api/get/haladek/feladatlekeres/${mentoraltid}/`;
    return await olvaso_fetch(url);
}

async function read_feladat_biralatai(mentoraltid, feladatid){
    let url = `${window.location.origin}/${hazioldalurl()}/api/get/haladek/feladatlekeres/${mentoraltid}/${feladatid}/`;
    return await olvaso_fetch(url);
}