// open modal by id
function openModal(id) {
    document.getElementById(id).classList.add('open');
    document.body.classList.add('delete-collection-modal-open');
}

// close currently open modal
function closeModal() {
    document.querySelector('.delete-collection-modal.open').classList.remove('open');
    document.body.classList.remove('delete-collection-modal-open');
}

window.addEventListener('load', function() {
    // close modals on background click
    document.addEventListener('click', event => {
        if (event.target.classList.contains('delete-collection-modal')) {
            closeModal();
        }
    });
});