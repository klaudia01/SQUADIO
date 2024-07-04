function redirectAlert(link) {
    Swal.fire({
        title: 'OSTRZEŻENIE',
        text: 'Czy na pewno chcesz opuścić tę stronę?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Kontynuuj',
        cancelButtonText: 'Anuluj',
        customClass: {
            popup: 'swal__popup',
            confirmButton: 'confirm__button',
            cancelButton: 'cancel__button'
        },
        color: '#d7d7d7',
        backdrop: 'rgba(0,0,0,0.8)',
        width: '550px',
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = link;
        }
    });
    const confirmButton = document.querySelector('.swal2-confirm');
    confirmButton.style.background = 'linear-gradient(to right, #541698, #ba0fcc)';

    const cancelButton = document.querySelector('.swal2-cancel');
    cancelButton.style.background = '#595b5c';

}
