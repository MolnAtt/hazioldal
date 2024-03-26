const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);
document.addEventListener("DOMContentLoaded", checkbox);

function main(){
    ovatos_esemenykapcsolas('#update', 'click', update_git);
}

//////////////////////////////////////

// UPDATE
async function update_git() {
    let url = `${window.location.origin}/${hazioldalurl()}/api/post/git/update/`;
    let szotar = {
        'username': document.querySelector('#gitusername').value,
    };
    try {
        let res = await kuldo_fetch(url, szotar);
        if (res && !res.title && res.message) {
            openModal('Response', res.message);
        } else if (res && res.title && res.message) {
            openModal(res.title, res.message);
        } else if (res && res.title && !res.message) {
            openModal(res.title, "Hiba az üzenet megjelnítése során");
        } else {
            throw new Error('Invalid response from server');
        }
    } catch (error) {
        console.error('Error occurred while updating Git:', error);
        openModal('Error', 'An error occurred while updating Git');
    }
}

function openModal(title, message) {
    var modal = document.getElementById('modal');
    var modalTitle = document.getElementById('modal-title');
    var modalMessage = document.getElementById('modal-message');

    modalTitle.textContent = title;
    modalMessage.textContent = message;
    modal.style.display = 'block';
    document.getElementById('modal-overlay').style.display = 'block';
    document.body.classList.add('modal-open');
}

document.addEventListener('click', function(event) {
    if (event.target && event.target.id === 'close-modal-btn') {
        closeModal();
    }
});

function closeModal() {
    var modal = document.getElementById('modal');
    var overlay = document.getElementById('modal-overlay');

    modal.style.display = 'none';
    overlay.style.display = 'none';
    document.body.classList.remove('modal-open');
}


function CommitChange(){
    var elem = document.getElementById('check1');
    if (elem.checked){
        localStorage.setItem("ShowCommitHistory", "on");
        console.info("ShowCommitHistory changed to: on");
    }
    else
    {
        localStorage.setItem("ShowCommitHistory", "off");
        console.info("ShowCommitHistory changed to: off");
    }
}

function checkbox(){
    var checked = localStorage.getItem("ShowCommitHistory");
    if (checked =="on"){
        document.getElementById("check1").checked = true;
    }
    else{
        document.getElementById("check1").checked = false;
    }
}
