function deleteAlert(button) {
    const deleteURL = button.getAttribute('data-delete-url');

    Swal.fire({
        title: "USUWANIE",
        text: "Czy na pewno chcesz to usunąć? Ta operacja jest nieodwracalna.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Usuń",
        cancelButtonText: "Anuluj",
        customClass: {
            popup: 'swal__popup',
            confirmButton: 'confirm__button',
            cancelButton: 'cancel__button'
        },
        color: '#d7d7d7',
        backdrop: 'rgba(0,0,0,0.8)'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = deleteURL;
        }
    });

    const confirmButton = document.querySelector('.swal2-confirm');
    confirmButton.style.background = 'linear-gradient(to right, #541698, #ba0fcc)';

    const cancelButton = document.querySelector('.swal2-cancel');
    cancelButton.style.background = '#595b5c';
}