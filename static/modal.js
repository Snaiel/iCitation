let can_close = true

// open modal by id
function openModal(id, can_close_modal) {
    document.getElementById(id).classList.add('open');
    document.body.classList.add('modal-open');
    can_close = can_close_modal;
}

// close currently open modal
function closeModal() {
    document.querySelector('.modal.open').classList.remove('open');
    document.body.classList.remove('modal-open');
}

window.addEventListener('load', function() {
    // close modals on background click
    document.addEventListener('click', event => {
        if (event.target.classList.contains('modal') && can_close) {
            closeModal();
        }
    });
});