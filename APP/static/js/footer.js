function openModal(title, message) {
    var modal = document.getElementById('modal');
    var modalTitle = document.getElementById('modal-title');
    var modalMessage = document.getElementById('modal-message');

    modalTitle.textContent = title;
    modalMessage.innerHTML = message;
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


function openCreditsModal() {
    var creditsModalTitle = "Credits";
    var creditsModalMessage = `
    <div style="text-align: center;">
        <div style="font-size: 18px; text-align: left;">
            <p style="margin-bottom: 10px;"><strong>Vezetőfejlesztő:</strong> <span style="color: #336699; transition: color 0.3s;" onmouseover="this.style.color='#ff9900'" onmouseout="this.style.color='#336699'">Molnár Attila</span></p>
            <p style="margin-bottom: 10px;"><strong>Frontend:</strong> <span style="color: #336699; transition: color 0.3s;" onmouseover="this.style.color='#ff9900'" onmouseout="this.style.color='#336699'">Hargitai Bence</span>, <span style="color: #336699; transition: color 0.3s;" onmouseover="this.style.color='#ff9900'" onmouseout="this.style.color='#336699'">Balla Botond</span>, <span style="color: #336699; transition: color 0.3s;" onmouseover="this.style.color='#ff9900'" onmouseout="this.style.color='#336699'">Magyar Kende Ákos</span></p>
            <p style="margin-bottom: 10px;"><strong>Backend:</strong> <span style="color: #336699; transition: color 0.3s;" onmouseover="this.style.color='#ff9900'" onmouseout="this.style.color='#336699'">Molnár Attila</span>, <span style="color: #336699; transition: color 0.3s;" onmouseover="this.style.color='#ff9900'" onmouseout="this.style.color='#336699'">Balla Botond</span>, <span style="color: #336699; transition: color 0.3s;" onmouseover="this.style.color='#ff9900'" onmouseout="this.style.color='#336699'">Varga Zénó Zoltán</span>, <span style="color: #336699; transition: color 0.3s;" onmouseover="this.style.color='#ff9900'" onmouseout="this.style.color='#336699'">Varga Benedek</span>, <span style="color: #336699; transition: color 0.3s;" onmouseover="this.style.color='#ff9900'" onmouseout="this.style.color='#336699'">Patkó Dániel</span></p>
        </div>
        <p style="font-size: 12px; margin-top: 20px;">Based on contributions to Git</p>
    </div>
`;



    openModal(creditsModalTitle, creditsModalMessage);
}