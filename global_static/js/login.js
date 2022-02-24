document.addEventListener("DOMContentLoaded", main);

function main(){
    document.getElementsByClassName('submitter')[0].addEventListener('click', kuld);
}


function kuld(e){
    formok = document.getElementsByTagName('form');
    if (formok.length > 0) {
        formok[0].submit();
    }
}