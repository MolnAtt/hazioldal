function openModal(title, message) {
    var modal = document.querySelector('.modal');
    var modalTitle = document.querySelector('.modal-title');
    var modalMessage = document.querySelector('.modal-message');

    modalTitle.textContent = title;
    modalMessage.innerHTML = message;
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
    var modal = document.querySelector('.modal');
    var overlay = document.querySelector('.modal-overlay');

    modal.style.display = 'none';
    overlay.style.display = 'none';
    document.body.classList.remove('modal-open');
}


function openCreditsModal() {
    var creditsModalTitle = "Credits";
    var credits = [
        "Molnár Attila",
        "Hargitai Bence",
        "Balla Botond",
        "Magyar Kende Ákos",
        "Varga Zénó Zoltán",
        "Varga Benedek",
        "Patkó Dániel"
    ];

    // Shuffle the credits array
    for (let i = credits.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [credits[i], credits[j]] = [credits[j], credits[i]];
    }

    var creditsModalMessage = `
    <div style="text-align: center;">
        <div style="font-size: 18px; text-align: center;">
            ${credits.map(name => `<p style="margin-bottom: 10px;"><small>${name}</small></p>`).join('')}
        </div>
    </div>
`;



    openModal(creditsModalTitle, creditsModalMessage);
}