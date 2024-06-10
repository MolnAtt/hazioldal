const csrftoken = getCookie('csrftoken');
document.addEventListener("DOMContentLoaded", main);
document.addEventListener("DOMContentLoaded", checkbox);

function main(){
    ovatos_esemenykapcsolas('#update', 'click', update_git);
}

//////////////////////////////////////

// UPDATE
async function update_git() {
    var commithistoryCheckbox = document.getElementById("check1");
    var gittokenfield = document.getElementById("gittokenfield");
    if (commithistoryCheckbox.checked && gittokenfield.value.trim() == "") {
        openModal("Form hiba", "Bekapcsoltad a commit historyt, de nem adtál meg github tokent")
    } else {

        let url = `${window.location.origin}/${hazioldalurl()}/api/post/git/update/`;
        let szotar = {
            'username': document.querySelector('#gitusername').value,
            'commithistory': document.querySelector('#check1').checked,
            'githubtoken': document.querySelector("#gittokenfield").value,
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
}

function openModal(title, message) {
    var modal = document.querySelector('.modal');
    var modalTitle = document.querySelector('.modal-title');
    var modalMessage = document.querySelector('.modal-message');

    modalTitle.textContent = title;
    modalMessage.textContent = message;
    modal.style.display = 'block';
    document.querySelector('.modal-overlay').style.display = 'block';
    document.body.classList.add('modal-open');
}

document.addEventListener('click', function(event) {
    if (event.target && event.target.classList.contains('close-modal-btn')) {
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

function commithistoryTrigger() {
    var commithistoryCheckbox = document.getElementById("check1");
    var githubtoken = document.getElementById("githubtoken");
    if (commithistoryCheckbox.checked){
        githubtoken.classList.remove("hidden");
        }
    else
    {
        githubtoken.classList.add("hidden");
        }
}

function checkbox() {
    var checkbox = document.getElementById("check1");
    var githubtoken = document.getElementById("githubtoken");
    if (githubtoken.classList.contains("hidden")) {
        checkbox.checked = false;
    } else {
        checkbox.checked = true;
    }
}