function deleteAlert(button) {
    const deleteURL = button.getAttribute('data-delete-url');

    Swal.fire({
        title: "USUWANIE",
        text: "Czy na pewno chcesz usunąć ten kontakt?",
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

document.getElementById('open-form-popup').addEventListener('click', function() {
    const formContent = document.getElementById('form-popup').innerHTML;
        Swal.fire({
        title: 'DODAWANIE NOWEGO KONTAKTU',
        html: formContent,
        showConfirmButton: false,
          customClass: {
            popup: 'swal__popup',
            title: 'swal__title'
          },
        color: '#d7d7d7',
        backdrop: 'rgba(0,0,0,0.8)',
        width: '800px'
  });
        const swal__title = document.querySelector('.swal2-title');
        swal__title.style.fontSize = '3rem';
});
