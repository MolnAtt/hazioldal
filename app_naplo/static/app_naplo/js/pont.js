const csrftoken = getCookie('csrftoken');
main()

function main(){
    document.addEventListener('keydown', tabkatt);
}

function tabkatt(event){
    let code = event.keyCode || event.which;
    if (code === 9) {  
        // alert("Megpróbálom elmenteni");
        pont_mentese(event.target);
    }
}

////////////////////////////////
// PONT API

async function pont_mentese(elem){
    let par = elem.id.split("-");
    let tanuloid = par[0];
    let feladatid = par[1];
    // alert(tanuloid);
    // alert(feladatid);
    let url = `${window.location.origin}/naplo/api/post/pont/write/`;
    let szotar = { 
        'tanuloid': tanuloid,
        'feladatid': feladatid,
        'ertek':elem.value,
    };
    let res = await kuldo_fetch(url, szotar);
    console.log(res);
}

