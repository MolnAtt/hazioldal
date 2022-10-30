function hazioldalurl(){ return 'hazioldal'; }

function getCookie(name) {
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return null;
}


function ovatos_esemenykapcsolas(idstr, eventstr, func){ 
    let elem = document.querySelector(idstr);
    if (elem!=null){
        elem.addEventListener(eventstr, func); 
    }
}

function ovatos_esemenykapcsolasok(idstr, eventstr, func){ 
    for (const elem of document.querySelectorAll(idstr)) {
        elem.addEventListener(eventstr, func); 
    }
}
