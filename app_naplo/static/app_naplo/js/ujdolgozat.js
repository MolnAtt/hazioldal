const csrftoken = getCookie('csrftoken');
main()

function main(){
    kuld.addEventListener('click', dolgozat_intezese);
}

async function dolgozat_intezese(){
    let [res, siker] = await create_dolgozat();
    console.log(res.uzenet);
    alert(res.uzenet);
    if(siker){
        tovabblink.href=`/naplo/${res.ev}/csoport/${csoportnev.value}/${dolgozatslug.value}/`;
    }
}


////////////////////////////////
// USER API


async function create_dolgozat(){

    if(dolgozatnev.value=='') return ['Nincs kitöltve a dolgozat neve!', false];
    if(dolgozatslug.value=='') return ['Nincs kitöltve a dolgozat slug!', false];
    if(csoportnev.value=='') return ['Nincs kitöltve a csoport!', false];
    if(suly.value=='') return ['Nincs kitöltve a súly!', false];
    if(datum.value=='') return ['Nincs kitöltve a dátum!', false];

    let url = `${window.location.origin}/naplo/api/post/dolgozat/create/`;
    let szotar = {
        'dolgozat_nev':dolgozatnev.value,
        'dolgozat_slug':dolgozatslug.value,
        'csoport_nev':csoportnev.value,
        'ponthatar2':ponthatar2.value,
        'ponthatar3':ponthatar3.value,
        'ponthatar4':ponthatar4.value,
        'ponthatar5':ponthatar5.value,
        'ponthatar55':ponthatar55.value,
        'ponthatar12':ponthatar12.value,
        'ponthatar23':ponthatar23.value,
        'ponthatar34':ponthatar34.value,
        'ponthatar45':ponthatar45.value,
        'feladatcsv':feladatok.value,
        'suly':suly.value,
        'datum':datum.value,
    };
    let res = await kuldo_fetch(url, szotar);
    return [res, true];
}
